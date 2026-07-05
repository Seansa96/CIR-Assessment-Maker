$files = @(
    "calc2-polar-curves-easy-test.yaml",
    "calc2-polar-curves-hard-quiz.yaml",
    "calc2-polar-curves-hard-test.yaml",
    "precalculus-conic-sections-easy-quiz.yaml",
    "precalculus-conic-sections-easy-test.yaml",
    "precalculus-conic-sections-hard-quiz.yaml",
    "precalculus-conic-sections-hard-test.yaml"
)

foreach ($file in $files) {
    $path = "c:\Users\SeanS\Downloads\cir_app\data\assessments\$file"
    $lines = Get-Content $path
    $newLines = @()
    
    foreach ($line in $lines) {
        $newLines += $line
        if ($line -match "^(\s+)expectedLatex: ") {
            $indent = $matches[1]
            $newLines += $indent + "equivalenceMode: expression"
            $newLines += $indent + "tolerance: 0.0"
        }
    }
    Set-Content -Path $path -Value $newLines
    Write-Output "Updated $file"
}
