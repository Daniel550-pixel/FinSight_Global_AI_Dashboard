"""# Windows installation helper for Sovereign AI Watch using NSSM (recommended)
# Usage:
# 1) Download nssm (https://nssm.cc/) and place nssm.exe on PATH or set $nssmPath.
# 2) Run this script in an elevated PowerShell prompt:
#    .\install_service.ps1 -InstallPath "C:\opt\sovereign-ai-watch" -PythonExe "C:\Python39\python.exe"
param(
    [Parameter(Mandatory=$true)]
    [string] $InstallPath,

    [Parameter(Mandatory=$true)]
    [string] $PythonExe,

    [string] $ServiceName = "SovereignAIWatch",

    [string] $NssmPath = "nssm"  # assume nssm on PATH
)

$script = Join-Path $InstallPath "sovereign_ai_watch.py"

if (-not (Test-Path $script)) {
    Write-Error "Cannot find $script — ensure the repository content is at InstallPath"
    exit 1
}

# Install with nssm
& $NssmPath install $ServiceName $PythonExe $script
& $NssmPath set $ServiceName AppDirectory $InstallPath
& $NssmPath set $ServiceName AppStdout "C:\ProgramData\SovereignAIWatch\stdout.log"
& $NssmPath set $ServiceName AppStderr "C:\ProgramData\SovereignAIWatch\stderr.log"
& $NssmPath set $ServiceName AppRestartDelay 5000

Write-Host "Service '$ServiceName' installed. Start it with: nssm start $ServiceName"""