$files = Get-ChildItem -Path c:\Users\SeanS\Downloads\cir_app\data\assessments\*.yaml

foreach ($file in $files) {
    $path = $file.FullName
    $content = [System.IO.File]::ReadAllText($path)
    
    # Remove the exact insertions made by the previous script
    # Matches \r\n or \n for newline, followed by indentation, equivalenceMode, newline, indentation, tolerance
    $pattern = "(?m)^[ \t]+equivalenceMode: expression\r?\n[ \t]+tolerance: 0\.0\r?\n"
    
    if ($content -match $pattern) {
        $content = $content -replace $pattern, ""
        [System.IO.File]::WriteAllText($path, $content)
        Write-Output "Reverted bad insertions in $($file.Name)"
    }
}
