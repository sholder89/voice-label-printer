"""Windows launcher for the Voice Label relay server.

Runs the SAME Flask app the Docker deployment uses (app.py), but adds
Windows-friendly niceties:
  • a system-tray icon (Open setup page / Health check / Restart / Quit)
  • a "/" setup landing page that shows the webhook URL + Siri instructions
  • stores the SQLite DB in %APPDATA%\\LabelPrinter so OneDrive won't sync it

This file is additive and Windows-only — it does not modify app.py, so the
Docker/gunicorn deployment is completely unaffected.

Run it via start-local.bat, or directly:  pythonw run_local.py
"""
import html
import os
import socket
import subprocess
import sys
import threading
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)


# ── Environment ───────────────────────────────────────────────────────────────
# app.py reads LABEL_TOKEN / DB_PATH / etc. at import time, so any .env loading
# and DB_PATH defaulting MUST happen before the `from app import ...` below.

def _load_env(path):
    """Minimal KEY=VALUE .env loader. Existing env vars win (setdefault)."""
    if not os.path.isfile(path):
        return
    try:
        with open(path, encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                if " #" in val:                       # strip inline comments
                    val = val.split(" #", 1)[0]
                os.environ.setdefault(key.strip(), val.strip())
    except OSError:
        pass


# Shared root .env (the client loads this too) takes precedence, then server/.env
_load_env(os.path.join(_ROOT, ".env"))
_load_env(os.path.join(_HERE, ".env"))

# Keep the job database out of the OneDrive-synced project folder
_DATA_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "LabelPrinter")
os.makedirs(_DATA_DIR, exist_ok=True)
os.environ.setdefault("DB_PATH", os.path.join(_DATA_DIR, "jobs.db"))

PORT = int(os.environ.get("PORT", "5001"))

# Import the real app AFTER the environment is prepared
from flask import request  # noqa: E402
from app import app as flask_app, TOKEN, MAX_TEXT_LEN  # noqa: E402


# ── Helpers ───────────────────────────────────────────────────────────────────

def _local_ip():
    """Best-effort LAN IP (the address Siri/other devices should POST to)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))      # no packets sent; just picks the iface
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


# ── Setup / info landing page (local convenience only) ────────────────────────

@flask_app.route("/")
def _local_info():
    ip      = _local_ip()
    # Only reveal the secret token to the local machine; hide it from other
    # devices on the LAN that happen to open this page. html.escape() guards
    # against any HTML-special characters in the token breaking the page.
    is_local = request.remote_addr in ("127.0.0.1", "::1")
    webhook  = html.escape(f"http://{ip}:{PORT}/webhook")
    token    = html.escape(TOKEN) if is_local else "(open this page on the PC to reveal)"
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Voice Label Server</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 640px;
         margin: 2rem auto; padding: 0 1rem; line-height: 1.55; }}
  h1 {{ font-size: 1.4rem; margin-bottom: .2rem; }}
  .ok {{ color: #16a34a; font-weight: 600; }}
  code, .url {{ font-family: ui-monospace, Consolas, monospace; }}
  .url {{ display: flex; gap: .5rem; align-items: center; flex-wrap: wrap;
          background: rgba(127,127,127,.12); padding: .6rem .8rem;
          border-radius: .5rem; font-size: 1rem; word-break: break-all; }}
  button {{ font: inherit; padding: .35rem .7rem; border-radius: .45rem;
            border: 1px solid rgba(127,127,127,.4); cursor: pointer;
            background: rgba(127,127,127,.12); }}
  ol {{ padding-left: 1.2rem; }}
  .card {{ border: 1px solid rgba(127,127,127,.25); border-radius: .75rem;
           padding: 1rem 1.25rem; margin: 1rem 0; }}
  .muted {{ opacity: .7; font-size: .9rem; }}
</style></head><body>
  <h1>🏷️ Voice Label Server</h1>
  <p class="ok">● Running locally on port {PORT}</p>

  <div class="card">
    <h2 style="font-size:1.05rem">Webhook endpoint</h2>
    <p>Point your Siri Shortcut (or IFTTT) at this URL:</p>
    <div class="url"><span id="hook">{webhook}</span>
      <button onclick="navigator.clipboard.writeText(document.getElementById('hook').textContent)">Copy</button>
    </div>
    <p class="muted">Method <code>POST</code> · header <code>X-Token: {token}</code> ·
       JSON body <code>{{"value1": "your label text"}}</code> · max {MAX_TEXT_LEN} chars.</p>
  </div>

  <div class="card">
    <h2 style="font-size:1.05rem">Siri Shortcut setup</h2>
    <p>In the <b>Shortcuts</b> app, tap <b>+</b> to create a new shortcut and add
       these two actions <b>in order</b>:</p>
    <ol>
      <li><b>Add action → “Ask for Input”.</b> Tap <b>Input Type</b> and set it to
          <b>Text</b>. Set the prompt to something like
          <i>“What should the label say?”</i> — this is what Siri asks you out loud.</li>
      <li><b>Add action → “Get Contents of URL”,</b> then tap <b>Show More</b> and set:
        <ul>
          <li><b>URL:</b> <code>{webhook}</code></li>
          <li><b>Method:</b> <code>POST</code></li>
          <li><b>Headers:</b> add one — key <code>X-Token</code>, value <code>{token}</code></li>
          <li><b>Request Body:</b> <code>JSON</code></li>
          <li>Under Request Body add a field — key <code>value1</code>, type <b>Text</b>,
              and for the value tap the variable button and pick
              <b>Provided Input</b> (the result of step 1).</li>
        </ul>
      </li>
    </ol>
    <p class="muted">Then rename the shortcut (e.g. <i>“Print a label”</i>) — that name
       is the phrase you say. “Hey Siri, Print a label” → Siri asks what to print →
       you speak → the label prints.</p>
    <p class="muted">Tip: “Dictate Text” works instead of “Ask for Input” if you want
       speech only. Plain HTTP is fine on your home network — no certificate needed,
       but your phone must be on the same Wi-Fi as this PC.</p>
  </div>

  <p class="muted">The Windows <b>client</b> (its own tray app) polls this server and
     does the actual printing — make sure it’s running too.</p>
</body></html>"""


# ── System tray ───────────────────────────────────────────────────────────────

def _make_tray_image():
    """Draw a small server-stack icon (distinct from the client's printer icon)."""
    from PIL import Image, ImageDraw
    sz  = 64
    img = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
    d   = ImageDraw.Draw(img)
    # Two stacked "server" units
    for top in (10, 36):
        d.rounded_rectangle([8, top, 56, top + 18], radius=4, fill="#4338ca")
        # status light + vent slots
        d.ellipse([13, top + 6, 19, top + 12], fill="#22c55e")
        for x in (40, 45, 50):
            d.rectangle([x, top + 6, x + 2, top + 12], fill="#c7d2fe")
    return img


def _run_tray():
    """Run the tray icon (blocks — must own the main thread on Windows)."""
    import webbrowser
    try:
        import pystray
    except ImportError:
        return  # caller handles the no-pystray fallback

    def on_open(icon, item):
        webbrowser.open(f"http://localhost:{PORT}/")

    def on_health(icon, item):
        webbrowser.open(f"http://localhost:{PORT}/health")

    def on_restart(icon, item):
        py_dir  = os.path.dirname(sys.executable)
        pythonw = os.path.join(py_dir, "pythonw.exe")
        if not os.path.exists(pythonw):
            pythonw = sys.executable
        env = os.environ.copy()
        env["LABEL_SERVER_RESTART"] = "1"   # skip browser auto-open on restart
        subprocess.Popen([pythonw, os.path.join(_HERE, "run_local.py")],
                         cwd=_HERE, env=env)
        icon.stop()
        os._exit(0)

    def on_quit(icon, item):
        icon.stop()
        os._exit(0)

    menu = pystray.Menu(
        pystray.MenuItem("Open setup page", on_open, default=True),
        pystray.MenuItem("Health check", on_health),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Restart", on_restart),
        pystray.MenuItem("Quit", on_quit),
    )
    pystray.Icon("label_server", _make_tray_image(), "Voice Label Server", menu).run()


# ── Entry point ───────────────────────────────────────────────────────────────

def _serve():
    flask_app.run(host="0.0.0.0", port=PORT, debug=False,
                  use_reloader=False, threaded=True)


if __name__ == "__main__":
    threading.Thread(target=_serve, daemon=True).start()
    time.sleep(0.8)   # let Flask bind before we open a browser

    try:
        import pystray  # noqa: F401 — availability probe
        import webbrowser
        if not os.environ.get("LABEL_SERVER_RESTART"):
            webbrowser.open(f"http://localhost:{PORT}/")
        _run_tray()     # blocks until Quit
    except ImportError:
        # No pystray — run headless in the console
        print(f"Voice Label Server → http://localhost:{PORT}/")
        print(f"Webhook for Siri    → http://{_local_ip()}:{PORT}/webhook")
        print(f"DB: {os.environ['DB_PATH']}")
        print("Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            pass
