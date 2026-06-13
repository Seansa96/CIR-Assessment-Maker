$ProjectRoot = "C:\Users\SeanS\Downloads\cir_app"

Write-Host "Starting backend..."

$backend = Start-Process `
    -FilePath "dotnet" `
    -ArgumentList "run --project backend/src/QuizApp.Api --urls http://localhost:5000" `
    -WorkingDirectory $ProjectRoot `
    -PassThru

Write-Host "Starting frontend..."

$frontend = Start-Process `
    -FilePath "npm" `
    -ArgumentList "run dev -- --port 4321" `
    -WorkingDirectory "$ProjectRoot\frontend" `
    -PassThru

@{
    BackendPid = $backend.Id
    FrontendPid = $frontend.Id
} | ConvertTo-Json | Set-Content "$ProjectRoot\.cir-processes.json"

Write-Host "Backend PID: $($backend.Id)"
Write-Host "Frontend PID: $($frontend.Id)"
Write-Host "CIR started."