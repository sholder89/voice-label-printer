# Keep the label printer's watchdog running, by registering a scheduled task.
#
# The watchdog restarts app.py when it crashes or hangs, but nothing restarted
# the watchdog: anything that ended it (a process started from a session that
# later closed, a crash) left the printer down until the next sign-in.
#
# The task starts watchdog.py at sign-in and then tries again every 5 minutes.
# The watchdog holds a single-instance mutex, so while one is running the extra
# starts exit at once; if it has died, the next one takes over within 5 minutes.
#
# Per-user, runs only while you're signed in (the tray icon needs a desktop),
# needs no admin. Run it again any time; it replaces the existing task.
#
#   powershell -ExecutionPolicy Bypass -File client\install-watchdog-task.ps1
#   powershell -ExecutionPolicy Bypass -File client\install-watchdog-task.ps1 -Remove

param([switch]$Remove)

$name   = 'Voice Label Printer Watchdog'
$client = Split-Path -Parent $MyInvocation.MyCommand.Path

if ($Remove) {
    Unregister-ScheduledTask -TaskName $name -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Removed scheduled task '$name'."
    return
}

$python = (Get-Command python.exe -ErrorAction Stop).Source
$pythonw = Join-Path (Split-Path -Parent $python) 'pythonw.exe'
if (-not (Test-Path $pythonw)) { $pythonw = $python }

$user    = "$env:USERDOMAIN\$env:USERNAME"
$action  = New-ScheduledTaskAction -Execute $pythonw -Argument 'watchdog.py --no-browser' -WorkingDirectory $client
$logon   = New-ScheduledTaskTrigger -AtLogOn -User $user
# A daily trigger that repeats every 5 minutes for a day re-arms itself each
# day, which is how you get "every 5 minutes, indefinitely" out of the cmdlets.
$every5  = New-ScheduledTaskTrigger -Daily -At '00:00'
$every5.Repetition = (New-ScheduledTaskTrigger -Once -At '00:00' `
    -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 1)).Repetition
# The cmdlet defaults this to true, which would end the running watchdog (and
# the app under it) every midnight when the day's repetition window closes.
$every5.Repetition.StopAtDurationEnd = $false
# No execution time limit: the default is 72 hours, after which Task Scheduler
# would kill the watchdog.
$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -MultipleInstances IgnoreNew `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -StartWhenAvailable
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $name -Action $action -Trigger $logon, $every5 `
    -Settings $settings -Principal $principal -Force `
    -Description 'Starts the Voice Label Printer watchdog, which keeps app.py running. Extra starts exit immediately.' | Out-Null

Write-Host "Registered scheduled task '$name' (at sign-in, then every 5 minutes)."
Write-Host "  $pythonw watchdog.py --no-browser  in  $client"
