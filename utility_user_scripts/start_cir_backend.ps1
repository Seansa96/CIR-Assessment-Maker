$ProjectRoot = "C:\Users\SeanS\Downloads\cir_app"
$StatusPath = "$ProjectRoot\.cir-processes.json"

function Write-CirStatus {
    param(
        [string]$BackendState,
        [Nullable[int]]$BackendPid,
        [string]$BackendMessage,
        [string]$SidecarState = "unknown",
        [Nullable[int]]$SidecarPid = $null
    )

    @{
        schemaVersion = 1
        updatedAt = (Get-Date).ToUniversalTime().ToString("o")
        backend = @{
            state = $BackendState
            pid = $BackendPid
            url = "http://localhost:5000"
            lastMessage = $BackendMessage
            startedAt = $null
            exitedAt = $null
            exitCode = $null
        }
        frontend = @{
            state = "unknown"
            pid = $null
            url = "http://127.0.0.1:4321"
            lastMessage = "backend-only launcher did not start frontend"
            startedAt = $null
            exitedAt = $null
            exitCode = $null
        }
        sidecar = @{
            state = $SidecarState
            pid = $SidecarPid
            url = "http://127.0.0.1:4789"
        }
    } | ConvertTo-Json -Depth 5 | Set-Content $StatusPath
}

Write-CirStatus -BackendState "building" -BackendPid $null -BackendMessage "dotnet run is about to start"

Write-Host "Starting dev status sidecar..."

$sidecar = Start-Process `
    -FilePath "node" `
    -ArgumentList "tools/dev-status-sidecar.mjs" `
    -WorkingDirectory $ProjectRoot `
    -PassThru `
    -WindowStyle Hidden

Write-Host "Starting backend..."

$backend = Start-Process `
    -FilePath "dotnet" `
    -ArgumentList "run --project backend/src/QuizApp.Api --urls http://localhost:5000" `
    -WorkingDirectory $ProjectRoot `
    -PassThru `
    -WindowStyle Hidden

Write-CirStatus -BackendState "starting" -BackendPid $backend.Id -BackendMessage "dotnet run launched; backend may still be building/importing" -SidecarState "running" -SidecarPid $sidecar.Id

Write-Host "Backend PID: $($backend.Id)"
Write-Host "Sidecar PID: $($sidecar.Id)"
