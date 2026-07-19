$files = Get-ChildItem -Path c:\Users\SeanS\Downloads\cir_app\data\assessments\*worked-example*.yaml

foreach ($file in $files) {
    $path = $file.FullName
    $lines = Get-Content $path
    $newLines = @()
    $inCheck = $false
    
    foreach ($line in $lines) {
        if ($line -match "^    check:\s*$") {
            $inCheck = $true
            continue
        }
        
        if ($inCheck -and $line -match "^ {6,}") {
            $unindented = $line.Substring(2)
            if ($unindented -match "^    id:\s*we-check") {
                continue
            }
            if ($unindented -match "^    options:\s*$") {
                $unindented = "    choices:"
            }
            $newLines += $unindented
        } elseif ($inCheck -and $line.Trim() -eq "") {
            $newLines += $line
        } else {
            $inCheck = $false
            $newLines += $line
        }
    }
    Set-Content -Path $path -Value $newLines
    Write-Output "Updated $($file.Name)"
}
