# One-time Windows setup for the all-local Voice Label Printer deployment.
#
#   • Always: creates a Startup-folder shortcut so both apps launch at login.
#   • Optional (-Firewall): opens Windows Firewall for ports 5001/5000.
#
# The auto-start shortcut needs no special rights, so the default run does NOT
# prompt for admin. The firewall step is opt-in because most setups don't need
# it — Windows usually prompts to allow Python on first run, or your Private
# network already permits LAN traffic. Only add the rules if another device
# (e.g. your phone) genuinely can't reach the apps.
#
# Usage:
#   Right-click -> "Run with PowerShell"                     (auto-start only)
#   powershell -ExecutionPolicy Bypass -File setup-windows.ps1 -Firewall   (also firewall)

param([switch]$Firewall)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path

# ── Firewall (opt-in; needs admin, so self-elevate only when requested) ───────
if ($Firewall) {
    $admin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
             ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if (-not $admin) {
        Write-Host "Re-launching elevated for the firewall rules..."
        Start-Process powershell "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -Firewall" -Verb RunAs
        exit
    }
    foreach ($r in @(
        @{ Name = "Voice Label Server (5001)"; Port = 5001 },
        @{ Name = "Voice Label Client (5000)"; Port = 5000 }
    )) {
        Get-NetFirewallRule -DisplayName $r.Name -ErrorAction SilentlyContinue |
            Remove-NetFirewallRule -ErrorAction SilentlyContinue
        New-NetFirewallRule -DisplayName $r.Name -Direction Inbound -Action Allow `
            -Protocol TCP -LocalPort $r.Port -Profile Private | Out-Null
        Write-Host "Firewall: allowed inbound TCP $($r.Port)  ($($r.Name))"
    }
}

# ── Auto-start shortcut (per-user Startup folder; no admin needed) ────────────
$startup = [Environment]::GetFolderPath('Startup')
$lnkPath = Join-Path $startup 'Voice Label Printer.lnk'
$target  = Join-Path $root 'run-all.bat'

$wsh = New-Object -ComObject WScript.Shell
$lnk = $wsh.CreateShortcut($lnkPath)
$lnk.TargetPath       = $target
$lnk.WorkingDirectory = $root
$lnk.WindowStyle      = 7          # minimized — no console window lingering
$lnk.Description      = 'Start Voice Label Printer server + client at login'
$lnk.Save()
Write-Host "Auto-start: created shortcut -> $lnkPath"

Write-Host ""
if (-not $Firewall) {
    Write-Host "Firewall rules were NOT added (not usually needed)."
    Write-Host "If another device can't reach the apps, re-run with:  -Firewall"
}
Write-Host "Done. Reboot (or run start-all.bat now) to launch both apps."
Write-Host "Server setup page: http://localhost:5001/   Client UI: http://localhost:5000/"
Read-Host "Press Enter to close"
