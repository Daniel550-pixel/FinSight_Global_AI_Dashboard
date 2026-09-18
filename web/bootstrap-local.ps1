# FinSight Quant Terminal — local bootstrap
$ErrorActionPreference="Stop"
$repo="https://github.com/Daniel550-pixel/FinSight_Global_AI_Dashboard.git"
$root=Join-Path $HOME "Downloads"
$dir=Join-Path $root "FinSight_Global_AI_Dashboard"
if(!(Test-Path $dir)){git clone $repo $dir}
Set-Location $dir
git fetch origin
if((git branch --format="%(refname:short)") -contains "feature/quant-terminal-web"){git switch feature/quant-terminal-web}else{git switch --track origin/feature/quant-terminal-web}
git pull --ff-only origin feature/quant-terminal-web
Set-Location .\web
npm install
npm run dev
