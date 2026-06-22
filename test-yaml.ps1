Add-Type -Path 'backend\tests\QuizApp.Tests\bin\Debug\net8.0\YamlDotNet.dll'
$deserializer = [YamlDotNet.Serialization.DeserializerBuilder]::new().Build()
$yaml = Get-Content 'data\assessments\chemistry-binary-ionic-type-i-naming-quiz.yaml' -Raw
try {
    $deserializer.Deserialize($yaml) | Out-Null
    Write-Host "Success"
} catch {
    Write-Host $_.Exception.ToString()
}
