$files = @(
    "physics-gravitational-energy-application-quiz.yaml",
    "physics-impulse-momentum-application-quiz.yaml",
    "physics-linear-drag-velocity-application-quiz.yaml",
    "physics-spring-energy-application-quiz.yaml",
    "physics-springs-comprehensive-test.yaml",
    "physics-system-momentum-application-quiz.yaml",
    "physics-system-momentum-derivation-worked-example.yaml",
    "physics-variable-force-work-application-quiz.yaml",
    "physics-work-energy-application-quiz.yaml"
)

foreach ($file in $files) {
    $path = "c:\Users\SeanS\Downloads\cir_app\data\assessments\$file"
    if (Test-Path $path) {
        $lines = Get-Content $path
        $newLines = @()
        foreach ($line in $lines) {
            # Find lines that I incorrectly converted to single quotes
            if ($line -match '^(\s*[a-zA-Z0-9_]+:\s*)''(.*\\.*)''\s*$') {
                $prop = $matches[1]
                $val = $matches[2]
                
                # Unescape what I did or fix the format
                $val = $val -replace '\\n', "`n"
                $val = $val -replace '\\\\', '\'
                
                $newLines += $prop + '|'
                $indent = "  "
                if ($prop -match '^(\s+)') {
                    $indent += $matches[1]
                }
                
                $valLines = $val -split "`n"
                foreach ($vl in $valLines) {
                    $newLines += $indent + $vl
                }
            } else {
                $newLines += $line
            }
        }
        Set-Content -Path $path -Value $newLines
        Write-Output "Fixed block scalar in $file"
    }
}
