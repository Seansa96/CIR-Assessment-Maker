$base = "data/assessments"
$retired_dir = "$base/retired"

$to_retire = @(
    'physics-work-energy-worked-examples.yaml',
    'physics-work-kinetic-energy-recall.yaml',
    'physics-work-kinetic-energy-quiz.yaml',
    'physics-springs-stiffness-concept-worked-example.yaml',
    'physics-springs-series-extension-worked-example.yaml',
    'physics-springs-shared-force-worked-example.yaml',
    'physics-springs-potential-energy-worked-example.yaml',
    'physics-springs-parallel-forces-worked-example.yaml',
    'physics-springs-keq-worked-example.yaml',
    'physics-springs-fbd-worked-example.yaml',
    'physics-springs-equilibrium-worked-example.yaml',
    'physics-springs-energy-gravity-worked-example.yaml'
)

foreach ($f in $to_retire) {
    if (Test-Path "$base/$f") {
        Write-Host "Retiring $f"
        Move-Item -Path "$base/$f" -Destination $retired_dir -Force
    }
}
