param(
    [string]$DataRoot = (Join-Path $PSScriptRoot "..\data"),
    [switch]$Apply
)

$ErrorActionPreference = "Stop"

function Get-Unquoted([string]$Value) {
    return $Value.Trim().Trim("'", '"')
}

function Get-CategoryTopics([string]$Root) {
    $topics = @{}
    Get-ChildItem (Join-Path $Root "categories") -Filter *.yaml | ForEach-Object {
        $categoryId = $null
        $currentTopic = $null
        foreach ($line in Get-Content $_.FullName) {
            if ($line -match '^id:\s*(.+)$' -and -not $categoryId) { $categoryId = Get-Unquoted $Matches[1] }
            elseif ($line -match '^  - id:\s*(.+)$') { $currentTopic = Get-Unquoted $Matches[1] }
            elseif ($currentTopic -and $line -match '^    title:\s*(.+)$') {
                $topics[$currentTopic] = Get-Unquoted $Matches[1]
                $currentTopic = $null
            }
        }
    }
    return $topics
}

function Get-TopicId([string[]]$Lines) {
    $start = [Array]::FindIndex($Lines, [Predicate[string]]{ param($line) $line -match '^topicId:\s*(.+)$' })
    if ($start -lt 0) { return [PSCustomObject]@{ Id = $null; End = -1 } }
    $value = Get-Unquoted (($Lines[$start] -replace '^topicId:\s*', ''))
    return [PSCustomObject]@{ Id = $value; End = $start }
}

function Get-Activity([string]$AssessmentType) {
    switch ($AssessmentType.ToLowerInvariant()) {
        'workedexample' { return @('learn', 'guidedWorkedExample') }
        'conceptlesson' { return @('learn', 'conceptLesson') }
        'glossary' { return @('learn', 'glossary') }
        'interactiveexploration' { return @('learn', 'interactiveExploration') }
        'directedproject' { return @('practice', 'directedProject') }
        'guidedproject' { return @('evaluate', 'guidedProject') }
        'sandbox' { return @('apply', 'sandbox') }
        'test' { return @('evaluate', 'formalTest') }
        'recalldrill' { return @('recall', 'mixedRecallSet') }
        default { return @('practice', 'focusedPractice') }
    }
}

function Insert-At([System.Collections.Generic.List[string]]$Lines, [int]$Index, [string[]]$NewLines) {
    for ($i = $NewLines.Count - 1; $i -ge 0; $i--) { $Lines.Insert($Index, $NewLines[$i]) }
}

function Add-MissingListValues([System.Collections.Generic.List[string]]$Lines, [int]$Start, [string]$Indent, [string[]]$Values) {
    $end = $Start
    $existing = @()
    for ($i = $Start + 1; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -notmatch ("^" + [regex]::Escape($Indent) + "-\s*(.+)$")) { break }
        $existing += (Get-Unquoted $Matches[1]).ToLowerInvariant()
        $end = $i
    }
    $missing = @($Values | Where-Object { $existing -notcontains $_.ToLowerInvariant() })
    if ($missing.Count -gt 0) { Insert-At $Lines ($end + 1) ($missing | ForEach-Object { "$Indent- $_" }) }
    return $missing.Count -gt 0
}

function Quote-SkillScalars([System.Collections.Generic.List[string]]$Lines) {
    $changed = $false
    $start = [Array]::FindIndex($Lines.ToArray(), [Predicate[string]]{ param($line) $line -match '^skills:' })
    if ($start -lt 0) { return $false }
    for ($i = $start + 1; $i -lt $Lines.Count -and $Lines[$i] -match '^-\s*(.+)$'; $i++) {
        $value = $Matches[1]
        if ($value -match ':' -and -not ($value.StartsWith("'") -or $value.StartsWith('"'))) {
            $Lines[$i] = "- '" + $value.Replace("'", "''") + "'"
            $changed = $true
        }
    }
    return $changed
}

function Remove-DuplicateListValues([System.Collections.Generic.List[string]]$Lines, [int]$Start, [string]$Indent) {
    if ($Start -lt 0) { return $false }
    $seen = @{}
    $changed = $false
    for ($i = $Start + 1; $i -lt $Lines.Count;) {
        if ($Lines[$i] -notmatch ("^" + [regex]::Escape($Indent) + "-\s*(.+)$")) { break }
        $key = (Get-Unquoted $Matches[1]).ToLowerInvariant()
        if ($seen.ContainsKey($key)) {
            $Lines.RemoveAt($i)
            $changed = $true
            continue
        }
        $seen[$key] = $true
        $i++
    }
    return $changed
}

function Normalize-NavigationTags([System.Collections.Generic.List[string]]$Lines, [int]$NavigationStart, [string[]]$RequiredTags) {
    $tagStart = [Array]::FindIndex($Lines.ToArray(), $NavigationStart, [Predicate[string]]{ param($line) $line -match '^  tags:' })
    if ($tagStart -lt 0) { return $false }
    $tagEnd = $tagStart + 1
    $values = @()
    for ($i = $tagStart + 1; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -match '^\S' -or ($Lines[$i] -match '^  [A-Za-z][A-Za-z0-9]*:')) { break }
        if ($Lines[$i] -match '^\s+-\s*(.+)$') { $values += Get-Unquoted $Matches[1] }
        $tagEnd = $i + 1
    }
    $combined = @($RequiredTags + $values)
    $unique = [System.Collections.Generic.List[string]]::new()
    foreach ($value in $combined) {
        if (-not [string]::IsNullOrWhiteSpace($value) -and -not ($unique | Where-Object { $_.Equals($value, [StringComparison]::OrdinalIgnoreCase) })) { $unique.Add($value) }
    }
    $replacement = @('  tags:') + @($unique | ForEach-Object { "  - $_" })
    $current = $Lines.GetRange($tagStart, $tagEnd - $tagStart)
    if (($current -join "`n") -eq ($replacement -join "`n")) { return $false }
    for ($i = $tagEnd - 1; $i -ge $tagStart; $i--) { $Lines.RemoveAt($i) }
    Insert-At $Lines $tagStart $replacement
    return $true
}

$topicTitles = Get-CategoryTopics $DataRoot
$changed = 0; $skipped = 0
Get-ChildItem (Join-Path $DataRoot "assessments") -Filter *.yaml -Recurse | ForEach-Object {
    $raw = [System.IO.File]::ReadAllText($_.FullName)
    if ($raw -notmatch '(?m)^id:' -or $raw -notmatch '(?m)^categoryId:' -or $raw -notmatch '(?m)^topicId:\s*\S+') { $skipped++; return }
    $lines = [System.Collections.Generic.List[string]]::new([string[]]($raw -split "`r?`n"))
    $categoryLine = $lines | Where-Object { $_ -match '^categoryId:' } | Select-Object -First 1
    $typeLine = $lines | Where-Object { $_ -match '^assessmentType:' } | Select-Object -First 1
    $categoryId = Get-Unquoted (($categoryLine -replace '^categoryId:\s*', ''))
    $assessmentType = Get-Unquoted (($typeLine -replace '^assessmentType:\s*', ''))
    $topicBlock = Get-TopicId $lines.ToArray()
    $topicId = $topicBlock.Id
    $topicEnd = $topicBlock.End
    if ($topicEnd -lt 0 -or [string]::IsNullOrWhiteSpace($topicId)) { $skipped++; return }
    $topicTitle = $topicTitles[$topicId]
    if ([string]::IsNullOrWhiteSpace($topicTitle)) { $topicTitle = $topicId }
    $skillValues = @("Apply $topicTitle")
    if ($skillValues.Count -eq 0) { $skillValues = @("Apply $categoryId concepts") }
    $tagValues = @($categoryId, $topicId)
    $activity = Get-Activity $assessmentType
    $fileChanged = $false

    if (-not ($lines | Where-Object { $_ -match '^skills:' } | Select-Object -First 1)) {
        Insert-At $lines ($topicEnd + 1) (@('skills:') + ($skillValues | ForEach-Object { "- $_" }))
        $fileChanged = $true
    }
    $skillsIndex = [Array]::FindIndex($lines.ToArray(), [Predicate[string]]{ param($line) $line -match '^skills:' })
    if (Add-MissingListValues $lines $skillsIndex '' $skillValues) { $fileChanged = $true }
    if (Quote-SkillScalars $lines) { $fileChanged = $true }
    if (Remove-DuplicateListValues $lines $skillsIndex '') { $fileChanged = $true }

    $navigationIndex = [Array]::FindIndex($lines.ToArray(), [Predicate[string]]{ param($line) $line -match '^navigation:' })
    if ($navigationIndex -lt 0) {
        $skillsIndex = [Array]::FindIndex($lines.ToArray(), [Predicate[string]]{ param($line) $line -match '^skills:' })
        $skillsEnd = $skillsIndex
        for ($i = $skillsIndex + 1; $i -lt $lines.Count -and $lines[$i] -match '^-\s+'; $i++) { $skillsEnd = $i }
        Insert-At $lines ($skillsEnd + 1) (@('navigation:', "  learningGoal: $($activity[0])", "  activityType: $($activity[1])", '  tags:') + ($tagValues | ForEach-Object { "  - $_" }))
        $fileChanged = $true
    } else {
        $navigationEnd = $navigationIndex
        for ($i = $navigationIndex + 1; $i -lt $lines.Count; $i++) { if ($lines[$i] -match '^\S') { break }; $navigationEnd = $i }
        if (-not ($lines[$navigationIndex..$navigationEnd] | Where-Object { $_ -match '^  learningGoal:' })) {
            Insert-At $lines ($navigationIndex + 1) @("  learningGoal: $($activity[0])"); $navigationEnd++; $fileChanged = $true
        }
        if (-not ($lines[$navigationIndex..$navigationEnd] | Where-Object { $_ -match '^  activityType:' })) {
            Insert-At $lines ($navigationIndex + 1) @("  activityType: $($activity[1])"); $navigationEnd++; $fileChanged = $true
        }
        if ($assessmentType -eq 'quiz') {
            $goalIndex = [Array]::FindIndex($lines.ToArray(), $navigationIndex, [Predicate[string]]{ param($line) $line -match '^  learningGoal: evaluate\s*$' })
            $activityIndex = [Array]::FindIndex($lines.ToArray(), $navigationIndex, [Predicate[string]]{ param($line) $line -match '^  activityType: focusedPractice\s*$' })
            if ($goalIndex -ge 0 -and $activityIndex -ge 0) {
                $lines[$goalIndex] = '  learningGoal: practice'
                $fileChanged = $true
            }
        }
        if (-not ($lines[$navigationIndex..$navigationEnd] | Where-Object { $_ -match '^  tags:' })) {
            Insert-At $lines ($navigationEnd + 1) (@('  tags:') + ($tagValues | ForEach-Object { "  - $_" })); $fileChanged = $true
        } else {
            $tagIndex = [Array]::FindIndex($lines.ToArray(), $navigationIndex, [Predicate[string]]{ param($line) $line -match '^  tags:' })
            if (Add-MissingListValues $lines $tagIndex '  ' $tagValues) { $fileChanged = $true }
        }
    }

    $navigationIndex = [Array]::FindIndex($lines.ToArray(), [Predicate[string]]{ param($line) $line -match '^navigation:' })
    if ($navigationIndex -ge 0) {
        $tagIndex = [Array]::FindIndex($lines.ToArray(), $navigationIndex, [Predicate[string]]{ param($line) $line -match '^  tags:' })
        if (Remove-DuplicateListValues $lines $tagIndex '  ') { $fileChanged = $true }
        if (Normalize-NavigationTags $lines $navigationIndex $tagValues) { $fileChanged = $true }
    }

    if ($fileChanged) {
        $changed++
        if ($Apply) { [System.IO.File]::WriteAllText($_.FullName, ($lines -join [Environment]::NewLine).TrimEnd() + [Environment]::NewLine) }
    }
}
Write-Output "Metadata normalization $(if ($Apply) { 'applied' } else { 'preview' }): $changed file(s) would change; $skipped file(s) skipped."
