[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$RepositoryPath
)

$ErrorActionPreference = 'Stop'
$repositoryRoot = (Resolve-Path -LiteralPath $RepositoryPath).Path
$records = & git -C $repositoryRoot worktree list --porcelain
if ($LASTEXITCODE -ne 0) { throw 'Unable to list Git worktrees.' }

$worktrees = @()
$current = $null
foreach ($record in $records) {
    if ($record.StartsWith('worktree ')) {
        if ($null -ne $current) { $worktrees += [pscustomobject]$current }
        $current = @{ Path = $record.Substring(9); Head = ''; Branch = '' }
    }
    elseif ($null -ne $current -and $record.StartsWith('HEAD ')) { $current.Head = $record.Substring(5) }
    elseif ($null -ne $current -and $record.StartsWith('branch ')) { $current.Branch = $record.Substring(7).Replace('refs/heads/', '') }
}
if ($null -ne $current) { $worktrees += [pscustomobject]$current }

foreach ($worktree in $worktrees) {
    $status = (& git -C $worktree.Path status --short 2>$null)
    $upstream = (& git -C $worktree.Path rev-parse --abbrev-ref '@{upstream}' 2>$null)
    if ($LASTEXITCODE -ne 0) { $upstream = '(none)' }
    $lockPath = (& git -C $worktree.Path rev-parse --git-path index.lock 2>$null)
    $lockState = if ($LASTEXITCODE -eq 0 -and (Test-Path -LiteralPath $lockPath)) { $lockPath } else { '(none)' }
    [pscustomobject]@{
        Path = $worktree.Path
        Branch = $worktree.Branch
        Head = $worktree.Head.Substring(0, [Math]::Min(12, $worktree.Head.Length))
        Dirty = if ($status) { 'yes' } else { 'no' }
        Upstream = $upstream
        IndexLock = $lockState
    }
}
