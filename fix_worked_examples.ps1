$files = @(
    "aops-olympiad-alg-worked-example.yaml",
    "aops-olympiad-geometry-worked-example.yaml",
    "aops-olympiad-trig-worked-example.yaml",
    "calc2-parametric-curves-basics-worked-example.yaml",
    "calc2-parametric-derivatives-worked-example.yaml",
    "calc2-parametric-integrals-worked-example.yaml",
    "calc2-polar-calculus-worked-example.yaml",
    "calc2-polar-curves-worked-example.yaml",
    "precalculus-conic-sections-worked-example.yaml"
)

foreach ($file in $files) {
    $path = "c:\Users\SeanS\Downloads\cir_app\data\assessments\$file"
    $lines = Get-Content $path
    $newLines = @()
    $stepCount = 1
    
    foreach ($line in $lines) {
        $newLines += $line
        
        if ($line -match "^  title: ") {
            $newLines += "  problem: 'Analyze and solve the steps for this problem.'"
        }
        
        if ($line -match "^  - id: ") {
            $newLines += "    title: 'Step $stepCount'"
            $stepCount++
        }
    }
    Set-Content -Path $path -Value $newLines
    Write-Output "Updated $file"
}
