$files = Get-ChildItem -Path c:\Users\SeanS\Downloads\cir_app\data\assessments\*.yaml
foreach ($file in $files) {
    $path = $file.FullName
    $lines = Get-Content $path
    $newLines = @()
    $modified = $false
    
    for ($i = 0; $i -lt $lines.Length; $i++) {
        $line = $lines[$i]
        if ($line -match "^equivalenceMode: expression$") {
            $modified = $true
            continue
        }
        if ($line -match "^tolerance: 0\.0$") {
            $modified = $true
            continue
        }
        $newLines += $line
    }
    
    if ($modified) {
        Set-Content -Path $path -Value $newLines
        Write-Output "Cleaned $($file.Name)"
    }
}
