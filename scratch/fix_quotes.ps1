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
        $modified = $false
        foreach ($line in $lines) {
            # Find lines that start with some spaces, a property name, and then a double-quoted string containing a backslash
            if ($line -match '^(\s*[a-zA-Z0-9_]+:\s*)"(.*\\.*)"\s*$') {
                $prop = $matches[1]
                $val = $matches[2]
                # Replace inner double quotes with nothing (or escape them), but usually these don't have inner quotes
                $val = $val -replace '"', "'"
                $newLine = $prop + "'" + $val + "'"
                $newLines += $newLine
                $modified = $true
            } else {
                $newLines += $line
            }
        }
        if ($modified) {
            Set-Content -Path $path -Value $newLines
            Write-Output "Fixed double quotes in $file"
        }
    }
}
