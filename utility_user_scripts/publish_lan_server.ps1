$ErrorActionPreference = "Stop"

# Set paths
$repoRoot = Resolve-Path "$PSScriptRoot\.."
$frontendDir = Join-Path $repoRoot "frontend"
$backendApiDir = Join-Path $repoRoot "backend\src\QuizApp.Api"
$publishDir = Join-Path $repoRoot "artifacts\lan-server"
$wwwrootDir = Join-Path $backendApiDir "wwwroot"

Write-Host "Publishing LAN Server..." -ForegroundColor Cyan

# 1. Build frontend
Write-Host "Building frontend..."
Set-Location $frontendDir
npm ci
npm run build

# 2. Copy frontend to API wwwroot
Write-Host "Copying frontend to API wwwroot..."
if (Test-Path $wwwrootDir) {
    Remove-Item -Recurse -Force $wwwrootDir
}
New-Item -ItemType Directory -Path $wwwrootDir | Out-Null
Copy-Item -Recurse -Force "$frontendDir\dist\*" $wwwrootDir

# 3. Publish backend
Write-Host "Publishing backend..."
Set-Location $backendApiDir
if (Test-Path $publishDir) {
    Remove-Item -Recurse -Force $publishDir
}
dotnet publish -c Release -o $publishDir

Write-Host "Publish complete! Output at: $publishDir" -ForegroundColor Green
