$ProjectRoot = "C:\Users\SeanS\Downloads\cir_app"
$env:CIR_BIND_URL = "https://0.0.0.0:5443"
$env:CIR_PUBLIC_ORIGIN = "https://cir-study.lan:5443"
$env:CIR_DATA_ROOT = "C:\Users\SeanS\Downloads\cir_app\data"
$env:CIR_KEY_RING_PATH = "C:\Users\SeanS\keyring"
$env:CIR_ACCESS_TOKEN_HASH = "oa4iDyxavLnrsYChO7mETWNxgQRi4xudyxXBMhAig74="
$env:CIR_ACCESS_TOKEN_SALT = "HgxgP/kZ5lV++TOU8XiylQ=="
$env:CIR_CERTIFICATE_PATH = "C:\Users\SeanS\Certificates\cir_app\localhost+2.p12"
$env:CIR_CERTIFICATE_PASSWORD = "changeit"

Write-Host "Starting backend..."

$backend = Start-Process `
    -FilePath "dotnet" `
    -ArgumentList "run --project backend/src/QuizApp.Api --urls http://localhost:5000" `
    -WorkingDirectory $ProjectRoot `
    -PassThru `
    -WindowStyle Hidden

Write-Host "Starting frontend..."

$frontend = Start-Process `
    -FilePath "npm" `
    -ArgumentList "run dev -- --port 4321" `
    -WorkingDirectory "$ProjectRoot\frontend" `
    -PassThru `
    -WindowStyle Hidden
@{
    BackendPid  = $backend.Id
    FrontendPid = $frontend.Id
} | ConvertTo-Json | Set-Content "$ProjectRoot\.cir-processes.json"

Write-Host "Backend PID: $($backend.Id)"
Write-Host "Frontend PID: $($frontend.Id)"
Write-Host "CIR started."