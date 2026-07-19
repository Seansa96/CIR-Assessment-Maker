$files = Get-ChildItem -Path c:\Users\SeanS\Downloads\cir_app\data\assessments\*.yaml
foreach ($file in $files) {
    $path = $file.FullName
    $lines = Get-Content $path
    $newLines = @()
    $inSymbolic = $false
    $hasEquiv = $false
    $modified = $false
    
    for ($i = 0; $i -lt $lines.Length; $i++) {
        $line = $lines[$i]
        
        if ($line -match "^\s*type:\s*symbolicResponse") {
            $inSymbolic = $true
            $hasEquiv = $false
        } elseif ($line -match "^\s*type:\s*") {
            $inSymbolic = $false
        }
        
        if ($inSymbolic -and $line -match "^\s*equivalenceMode:") {
            $hasEquiv = $true
        }
        
        $newLines += $line
        
        if ($inSymbolic -and (-not $hasEquiv) -and $line -match "^(\s+)expectedLatex:") {
            $indent = $matches[1]
            # peek ahead to see if equivalenceMode exists in the next few lines
            $foundEquiv = $false
            for ($j = $i + 1; $j -lt $i + 6 -and $j -lt $lines.Length; $j++) {
                if ($lines[$j] -match "^\s*equivalenceMode:") {
                    $foundEquiv = $true
                    break
                }
                if ($lines[$j] -match "^\s*- id:" -or $lines[$j] -match "^\s*type:") {
                    break
                }
            }
            if (-not $foundEquiv) {
                $newLines += $indent + "equivalenceMode: expression"
                $newLines += $indent + "tolerance: 0.0"
                $hasEquiv = $true
                $modified = $true
            }
        }
    }
    if ($modified) {
        Set-Content -Path $path -Value $newLines
        Write-Output "Updated $($file.Name)"
    }
}
