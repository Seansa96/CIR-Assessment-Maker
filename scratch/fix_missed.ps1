$base = "data/assessments"

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

$files = Get-ChildItem -Path $base -Filter "*.yaml"

foreach ($file in $files) {
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
Write-Host "Done fixing missing files."
