[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$RepositoryPath
)

$ErrorActionPreference = 'Stop'
$repositoryRoot = (Resolve-Path -LiteralPath $RepositoryPath).Path
$parentDirectory = Split-Path -Parent $repositoryRoot
$layouts = @(
    @{ Path = (Join-Path $parentDirectory 'cir_app_integration'); Branch = 'develop'; Base = 'origin/main' },
    @{ Path = (Join-Path $parentDirectory 'cir_app_chatgpt'); Branch = 'agent/chatgpt'; Base = 'develop' },
    @{ Path = (Join-Path $parentDirectory 'cir_app_antigravity'); Branch = 'agent/antigravity'; Base = 'develop' }
)

function Invoke-RepositoryGit([string[]]$Arguments) {
    & git -C $repositoryRoot @Arguments
    if ($LASTEXITCODE -ne 0) { throw "git $($Arguments -join ' ') failed." }
}

function Test-Branch([string]$Branch) {
    & git -C $repositoryRoot show-ref --verify --quiet "refs/heads/$Branch"
    return $LASTEXITCODE -eq 0
}

foreach ($layout in $layouts) {
    if (Test-Path -LiteralPath $layout.Path) {
        $branch = (& git -C $layout.Path branch --show-current 2>$null).Trim()
        if ($LASTEXITCODE -ne 0 -or $branch -ne $layout.Branch) {
            throw "Refusing to use '$($layout.Path)': it exists but is not the expected '$($layout.Branch)' worktree."
        }
        Write-Host "Validated $($layout.Branch): $($layout.Path)"
        continue
    }

    if (Test-Branch $layout.Branch) {
        Invoke-RepositoryGit @('worktree', 'add', $layout.Path, $layout.Branch)
    }
    else {
        Invoke-RepositoryGit @('worktree', 'add', '-b', $layout.Branch, $layout.Path, $layout.Base)
    }
    Write-Host "Created $($layout.Branch): $($layout.Path)"
}

Invoke-RepositoryGit @('worktree', 'list')
