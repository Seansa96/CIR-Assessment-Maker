$files = @(
    "aops-olympiad-alg-concept-lesson.yaml",
    "aops-olympiad-geometry-concept-lesson.yaml",
    "aops-olympiad-trig-concept-lesson.yaml",
    "calc2-parametric-curves-basics-concept-lesson.yaml",
    "calc2-parametric-derivatives-concept-lesson.yaml",
    "calc2-parametric-integrals-concept-lesson.yaml",
    "calc2-polar-calculus-concept-lesson.yaml",
    "calc2-polar-curves-concept-lesson.yaml",
    "precalculus-conic-sections-concept-lesson.yaml"
)

foreach ($file in $files) {
    $path = "c:\Users\SeanS\Downloads\cir_app\data\assessments\$file"
    $lines = Get-Content $path
    $newLines = @()
    $inSections = $false
    
    foreach ($line in $lines) {
        if ($line -match "^sections:") {
            $inSections = $true
            $newLines += "lesson:"
            $newLines += "  introduction: 'Review the fundamental concepts and principles below.'"
            $newLines += "  sections:"
        } elseif ($inSections) {
            $newLines += "  $line"
        } else {
            $newLines += $line
        }
    }
    Set-Content -Path $path -Value $newLines
    Write-Output "Updated $file"
}
