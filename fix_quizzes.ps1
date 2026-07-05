$files = Get-ChildItem -Path c:\Users\SeanS\Downloads\cir_app\data\assessments\*.yaml

foreach ($file in $files) {
    $path = $file.FullName
    $lines = Get-Content $path
    $newLines = @()
    $currentType = ""
    $modified = $false
    
    foreach ($line in $lines) {
        if ($line -match "^\s+type: (.*)") {
            $currentType = $matches[1]
        }
        
        # Replace options with choices
        if ($line -match "^(\s+)options:\s*$") {
            $line = $matches[1] + "choices:"
            $modified = $true
        }
        
        $newLines += $line
        
        # If we see expectedLatex inside answer and type is symbolicResponse, add equivalenceMode and tolerance
        if ($currentType -eq "symbolicResponse" -and $line -match "^(\s+)expectedLatex: ") {
            $indent = $matches[1]
            $newLines += $indent + "equivalenceMode: expression"
            $newLines += $indent + "tolerance: 0.0"
            $modified = $true
        }
    }
    
    if ($modified) {
        Set-Content -Path $path -Value $newLines
        Write-Output "Updated $($file.Name)"
    }
}
