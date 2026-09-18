$ErrorActionPreference = "Stop"
$repo = "https://github.com/Daniel550-pixel/FinSight_Global_AI_Dashboard.git"
$root = Join-Path $HOME "Downloads"
$dir = Join-Path $root "FinSight_Global_AI_Dashboard"
if (!(Test-Path $dir)) { git clone $repo $dir }
Set-Location $dir
git fetch origin
git checkout feature/quant-terminal-web
git pull origin feature/quant-terminal-web
Set-Location (Join-Path $dir "web")
if (!(Test-Path "node_modules")) { npm install }
Write-Host ""
Write-Host "FinSight Quant Terminal starting on http://localhost:8504" -ForegroundColor Cyan
Write-Host "Keep this terminal open." -ForegroundColor DarkGray
npm run dev
