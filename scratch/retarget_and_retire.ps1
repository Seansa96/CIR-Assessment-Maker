$base = "data/assessments"
$retired_dir = "$base/retired"

if (!(Test-Path $retired_dir)) {
    New-Item -ItemType Directory -Force -Path $retired_dir | Out-Null
}

$topic_map = @{
    'physics-simple-harmonic-motion' = 'physics-oscillations-shm'
    'physics-shm-energy' = 'physics-oscillations-shm'
    'physics-shm-circular-motion' = 'physics-oscillations-shm'
    'physics-pendulums' = 'physics-oscillations-shm'
    'physics-damped-oscillations' = 'physics-damped-forced-oscillations'
    'physics-forced-oscillations' = 'physics-damped-forced-oscillations'
    'physics-traveling-waves' = 'physics-wave-mechanics'
    'physics-wave-mathematics' = 'physics-wave-mechanics'
    'physics-stretched-string-wave-speed' = 'physics-wave-mechanics'
    'physics-standing-waves-resonance' = 'physics-wave-mechanics'
    'physics-sound-waves' = 'physics-acoustics'
    'physics-speed-of-sound' = 'physics-acoustics'
    'physics-sound-intensity' = 'physics-acoustics'
    'physics-standing-sound-modes' = 'physics-acoustics'
    'physics-musical-sound-sources' = 'physics-acoustics'
    'physics-beats' = 'physics-acoustics'
    'physics-doppler-effect' = 'physics-acoustics'
    'physics-shock-waves' = 'physics-acoustics'
}

$stubs_to_retire = @()
foreach ($key in $topic_map.Keys) {
    $stubs_to_retire += "$key-glossary.yaml"
    $stubs_to_retire += "$key-recall-drill.yaml"
}

$concept_tests = @(
    'physics-angular-momentum-concept-test.yaml', 'physics-dynamics-concept-test.yaml',
    'physics-energy-momentum-concept-test.yaml', 'physics-fixed-axis-rotation-concept-test.yaml',
    'physics-fluid-mechanics-concept-test.yaml', 'physics-gravitation-concept-test.yaml',
    'physics-kinematics-concept-test.yaml', 'physics-oscillations-waves-acoustics-concept-test.yaml',
    'physics-properties-of-matter-concept-test.yaml'
)

$files_to_retire = $stubs_to_retire + $concept_tests

$files = Get-ChildItem -Path $base -Filter "physics-*.yaml"

foreach ($file in $files) {
    if ($files_to_retire -contains $file.Name) {
        Write-Host "Retiring: $($file.Name)"
        Move-Item -Path $file.FullName -Destination $retired_dir -Force
        continue
    }
    
    if ($file.Name -eq 'physics-terminal-velocity-derivation-worked-example.yaml' -or $file.Name -eq 'physics-linear-drag-velocity-derivation-worked-example.yaml') {
        $content = Get-Content $file.FullName
        $newContent = $content -replace '^topicId:.*', 'topicId: physics-calculus-derivations'
        Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
        Write-Host "Retargeting $($file.Name) to physics-calculus-derivations"
        continue
    }

    $content = Get-Content $file.FullName
    $modified = $false
    foreach ($key in $topic_map.Keys) {
        if ($content -match "^topicId:\s*$key`$") {
            $newTopic = $topic_map[$key]
            $content = $content -replace "^topicId:\s*$key`$", "topicId: $newTopic"
            $modified = $true
            Write-Host "Retargeting $($file.Name) to $newTopic"
            break
        }
    }
    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
    }
}
Write-Host "Done phase 3 and 4."
