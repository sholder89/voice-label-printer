"""Keep the label printer running: start app.py, health-check it, restart it.

    pythonw watchdog.py

start.bat and run-all.bat launch this instead of app.py. It restarts the app
when it

  • exits for any reason other than the tray's Quit
  • stops answering /status on the web UI
  • stops pumping window messages (what Windows reports as "not responding")

Before killing a hung app it saves every thread's stack to hang-stacks.log, so
the next hang says where it was stuck. Restarts are logged to watchdog.log
beside the settings, and the relaunched app posts a Telegram message saying
why, when Telegram is configured. Standard library only, so it still runs if
a dependency of the app is broken.
"""
import ctypes
import ctypes.wintypes as wt
import logging
import logging.handlers
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime

APP_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("LABEL_DATA_DIR") or os.path.join(
    os.environ.get("APPDATA", os.path.expanduser("~")), "LabelPrinter")

CHECK_EVERY   = 15      # seconds between health checks
GRACE         = 45      # seconds after launch before the first check
FAILS_TO_KILL = 4       # consecutive failed checks (~1 minute) before a restart
HTTP_TIMEOUT  = 10
BACKOFF_MIN, BACKOFF_MAX = 5, 300
QUICK_CRASH   = 60      # dying sooner than this after launch counts towards backoff

# The scheduled task passes this: it may be bringing the watchdog back hours
# into the day, when a browser tab popping up out of nowhere would be odd.
NO_BROWSER = "--no-browser" in sys.argv[1:]

EXIT_QUIT    = 0        # tray Quit: the user meant it, so stop too
EXIT_RESTART = 3        # tray Restart: relaunch straight away (see app.py)

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

log = logging.getLogger("watchdog")


def _setup_logging():
    os.makedirs(DATA_DIR, exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(
        os.path.join(DATA_DIR, "watchdog.log"), maxBytes=512 * 1024, backupCount=2,
        encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s  %(message)s", "%Y-%m-%d %H:%M:%S"))
    log.addHandler(handler)
    log.setLevel(logging.INFO)


def _single_instance():
    """Hold a named mutex for our lifetime. False if another watchdog has it."""
    _single_instance.handle = kernel32.CreateMutexW(None, False, "Local\\VoiceLabelPrinterWatchdog")
    return kernel32.GetLastError() != 183          # ERROR_ALREADY_EXISTS


def _ui_port():
    try:
        with open(os.path.join(DATA_DIR, "ui-port")) as fh:
            return int(fh.read().strip())
    except (OSError, ValueError):
        return 5000


def _get(path, port=None, timeout=HTTP_TIMEOUT):
    url = f"http://127.0.0.1:{port or _ui_port()}{path}"
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.status, r.read()


def _healthy_http():
    try:
        status, body = _get("/status")
        return status == 200 and b'"polling"' in body
    except Exception:
        return False


def _windows_of(pid):
    found = []

    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def each(hwnd, _):
        owner = wt.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(owner))
        if owner.value == pid:
            found.append(hwnd)
        return True

    user32.EnumWindows(each, 0)
    return found


def _windows_hung(pid):
    """True if any of the app's windows has stopped processing messages."""
    return any(user32.IsHungAppWindow(h) for h in _windows_of(pid))


def _save_stacks(reason):
    """Ask the app what every thread is doing, before it's killed."""
    try:
        _, body = _get("/debug/stacks", timeout=10)
        text = body.decode("utf-8", "replace")
    except Exception as e:
        text = (f"(couldn't fetch /debug/stacks: {e!r}. If no Python thread could "
                f"run, the app's own stall detector should have written stacks "
                f"just above.)")
    try:
        with open(os.path.join(DATA_DIR, "hang-stacks.log"), "a", encoding="utf-8") as fh:
            fh.write(f"\n=== {datetime.now().isoformat(timespec='seconds')} "
                     f"watchdog restart: {reason}\n{text}\n")
    except OSError:
        pass


def _listening_pid(port):
    """PID listening on a local TCP port, from netstat (no psutil here)."""
    try:
        out = subprocess.run(["netstat", "-ano", "-p", "TCP"], capture_output=True,
                             text=True, timeout=15,
                             creationflags=subprocess.CREATE_NO_WINDOW).stdout
    except Exception:
        return None
    for line in out.splitlines():
        m = re.match(rf"\s*TCP\s+\S+:{port}\s+\S+\s+LISTENING\s+(\d+)", line)
        if m:
            return int(m.group(1))
    return None


def _take_over_unsupervised():
    """An app started without us (an old launcher, a manual start) would hold
    the UI port and push ours onto a fallback. Replace it, so there's one
    instance and it's watched."""
    for port in {5000, _ui_port()}:
        try:
            status, body = _get("/status", port=port, timeout=5)
            if status != 200 or b'"polling"' not in body:
                continue
        except Exception:
            continue
        pid = _listening_pid(port)
        if pid and pid != os.getpid():
            log.info("found an unsupervised label printer (PID %s, port %s); replacing it",
                     pid, port)
            subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True,
                           creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(2)


def _pythonw():
    candidate = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    return candidate if os.path.exists(candidate) else sys.executable


def _launch(reason=None):
    env = os.environ.copy()
    env["LABEL_PRINTER_SUPERVISED"] = "1"
    env.pop("LABEL_PRINTER_WATCHDOG_REASON", None)
    if NO_BROWSER:
        env["LABEL_PRINTER_RESTART"] = "1"
    if reason:
        env["LABEL_PRINTER_RESTART"] = "1"          # no browser tab on a relaunch
        if reason != "restarted from the tray":
            env["LABEL_PRINTER_WATCHDOG_REASON"] = reason
    proc = subprocess.Popen([_pythonw(), os.path.join(APP_DIR, "app.py")], cwd=APP_DIR, env=env)
    log.info("started app (PID %s)%s", proc.pid, f" — {reason}" if reason else "")
    return proc


def _wait(proc, secs):
    """Sleep, but wake as soon as the app exits."""
    try:
        proc.wait(timeout=secs)
    except subprocess.TimeoutExpired:
        pass


def _supervise(proc):
    """Watch one app process. Returns (reason to restart, or None to stop)."""
    started = time.time()
    _wait(proc, GRACE)
    http_fails = hung = 0
    while True:
        code = proc.poll()
        if code is not None:
            if code == EXIT_QUIT:
                log.info("app quit from the tray; watchdog stopping")
                return None, started
            if code == EXIT_RESTART:
                return "restarted from the tray", started
            if code >= 2 ** 31:                     # Windows reports exit codes unsigned
                code -= 2 ** 32
            return f"app exited unexpectedly (code {code})", started

        http_fails = 0 if _healthy_http() else http_fails + 1
        hung       = hung + 1 if _windows_hung(proc.pid) else 0
        if http_fails == 1 or hung == 1:
            log.info("check failed (web UI fails=%d, window hung=%d)", http_fails, hung)

        reason = None
        if http_fails >= FAILS_TO_KILL:
            reason = f"web UI stopped answering for ~{http_fails * CHECK_EVERY}s"
        elif hung >= FAILS_TO_KILL:
            reason = f"app stopped responding to Windows for ~{hung * CHECK_EVERY}s"
        if reason:
            log.info("%s; saving stacks and killing PID %s", reason, proc.pid)
            _save_stacks(reason)
            proc.kill()
            try:
                proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                pass
            return reason, started
        _wait(proc, CHECK_EVERY)


def main():
    _setup_logging()
    if not _single_instance():
        log.info("another watchdog is already running; exiting")
        return
    log.info("watchdog started (PID %s)", os.getpid())
    _take_over_unsupervised()

    backoff = BACKOFF_MIN
    reason  = None
    while True:
        proc = _launch(reason)
        reason, started = _supervise(proc)
        if reason is None:
            return
        if reason == "restarted from the tray":
            continue
        # Crash loops (a broken install, a bad config) back off instead of spinning.
        if time.time() - started < GRACE + QUICK_CRASH:
            log.info("restarting in %ss", backoff)
            time.sleep(backoff)
            backoff = min(backoff * 2, BACKOFF_MAX)
        else:
            backoff = BACKOFF_MIN


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log.exception("watchdog crashed")
        raise
