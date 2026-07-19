$files = @(
    "calc2-parametric-polar-cumulative-hard-test.yaml",
    "calc2-polar-calculus-easy-quiz.yaml",
    "calc2-polar-calculus-hard-quiz.yaml",
    "calc2-polar-curves-easy-quiz.yaml"
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
