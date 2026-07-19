$files = Get-ChildItem -Path c:\Users\SeanS\Downloads\cir_app\data\assessments\*.yaml
foreach ($file in $files) {
    $content = Get-Content $file.FullName
    $newContent = $content -replace 'physics-momentum-collisions-collisions', 'physics-momentum-collisions'
    
    if ($file.Name -eq 'chem-bohr-model-quiz.yaml') { $newContent = $newContent -replace 'chem-atomic-structure', 'chem-bohr-model' }
    if ($file.Name -eq 'chem-electron-configs-quiz.yaml') { $newContent = $newContent -replace 'chem-atomic-structure', 'chem-electron-configs' }
    if ($file.Name -eq 'chem-em-spectrum-quiz.yaml') { $newContent = $newContent -replace 'chem-atomic-structure', 'chem-em-spectrum' }
    if ($file.Name -eq 'chem-ionic-covalent-distinction-quiz.yaml') { $newContent = $newContent -replace 'chem-bonds', 'chem-ionic-covalent-distinction' }
    if ($file.Name -eq 'chem-ions-quiz.yaml') { $newContent = $newContent -replace 'chem-atoms-molecules-ions', 'chem-ions' }
    if ($file.Name -eq 'chem-lewis-symbols-quiz.yaml') { $newContent = $newContent -replace 'chem-bonds', 'chem-lewis-symbols' }
    if ($file.Name -eq 'chem-periodic-trends-quiz.yaml') { $newContent = $newContent -replace 'chem-periodic-table', 'chem-periodic-trends' }
    if ($file.Name -eq 'chem-quantum-model-quiz.yaml') { $newContent = $newContent -replace 'chem-atomic-structure', 'chem-quantum-model' }
    if ($file.Name -eq 'chemistry-binary-ionic-type-i-naming-quiz.yaml') { $newContent = $newContent -replace 'chem-nomenclature', 'chemistry-compounds' }
    if ($file.Name -eq 'chemistry-binary-ionic-type-ii-naming-quiz.yaml') { $newContent = $newContent -replace 'chem-nomenclature', 'chemistry-compounds' }

    if ($content -ne $newContent) {
        Set-Content -Path $file.FullName -Value $newContent
        Write-Output "Updated $($file.Name)"
    }
}
