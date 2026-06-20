$ErrorActionPreference = "Stop"
$ProjectRoot = "C:\Users\SeanS\Downloads\cir_app"
$env:CIR_BIND_URL = "https://0.0.0.0:5443"
$env:CIR_PUBLIC_ORIGIN = "https://192.168.0.189:5443"
$env:CIR_DATA_ROOT = "C:\Users\SeanS\Downloads\cir_app\data"
$env:CIR_KEY_RING_PATH = "C:\Users\SeanS\keyring"
$env:CIR_ACCESS_TOKEN_HASH = "oa4iDyxavLnrsYChO7mETWNxgQRi4xudyxXBMhAig74="
$env:CIR_ACCESS_TOKEN_SALT = "HgxgP/kZ5lV++TOU8XiylQ=="
$env:CIR_CERTIFICATE_PATH = "C:\Users\SeanS\Certificates\cir_app\localhost+2.p12"
$env:CIR_CERTIFICATE_PASSWORD = "changeit"

Write-Host "Starting CIR LAN Server..." -ForegroundColor Cyan

$scriptPath = $MyInvocation.MyCommand.Path
$dir = Split-Path $scriptPath
$repoRoot = Resolve-Path "$dir\.."
$serverDir = Join-Path $repoRoot "artifacts\lan-server"
$executable = Join-Path $serverDir "QuizApp.Api.exe"

if (-not (Test-Path $executable)) {
    Write-Host "Error: Server executable not found at $executable" -ForegroundColor Red
    Write-Host "Did you run publish_lan_server.ps1?"
    exit 1
}

# Verify required environment variables
$requiredEnvVars = @(
    "CIR_ACCESS_TOKEN_HASH",
    "CIR_ACCESS_TOKEN_SALT",
    "CIR_BIND_URL",
    "CIR_DATA_ROOT"
)

$missing = @()
foreach ($env in $requiredEnvVars) {
    if (-not [Environment]::GetEnvironmentVariable($env)) {
        $missing += $env
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Error: The following required environment variables are not set:" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host "  - $_" }
    Write-Host "Please configure them before starting the server."
    exit 1
}

Write-Host "Starting server on $([Environment]::GetEnvironmentVariable('CIR_BIND_URL'))..."
Write-Host "Data root: $([Environment]::GetEnvironmentVariable('CIR_DATA_ROOT'))"

Set-Location $serverDir
& $executable
