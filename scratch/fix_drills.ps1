$fric = "c:\Users\SeanS\Downloads\cir_app\data\assessments\phys-fric-force-id-drill.yaml"
$m2d = "c:\Users\SeanS\Downloads\cir_app\data\assessments\phys-m2d-frame-id-drill.yaml"
$n2 = "c:\Users\SeanS\Downloads\cir_app\data\assessments\phys-n2-force-id-drill.yaml"

$files = @($fric, $m2d, $n2)

foreach ($path in $files) {
    $content = Get-Content $path
    $newContent = @()
    foreach ($line in $content) {
        $line = $line -replace "learningGoal: recall", "learningGoal: practice"
        $line = $line -replace "activityType: formalTest", "activityType: focusedPractice"
        $line = $line -replace "activityType: drill", "activityType: focusedPractice"
        $line = $line -replace "assessmentType: recallDrill", "assessmentType: quiz"
        $line = $line -replace "^items:", "questions:"
        $newContent += $line
    }
    Set-Content -Path $path -Value $newContent
    Write-Output "Updated $path"
}
