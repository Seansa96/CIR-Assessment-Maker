$ErrorActionPreference = "Stop"

Write-Host "CIR LAN Server - Access Token Configuration" -ForegroundColor Cyan
Write-Host "This script hashes a shared token using PBKDF2 to store securely."

$token = Read-Host -AsSecureString "Enter the new shared access token (at least 20 random characters recommended)"
$tokenPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($token))

if ([string]::IsNullOrWhiteSpace($tokenPlain) -or $tokenPlain.Length -lt 8) {
    Write-Host "Error: Token is too short or empty." -ForegroundColor Red
    exit 1
}

# Generate salt
$saltBytes = New-Object byte[] 16
$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
$rng.GetBytes($saltBytes)
$saltBase64 = [Convert]::ToBase64String($saltBytes)

# We use the same PBKDF2 parameters as the C# code:
# HMACSHA256, 100,000 iterations, 32-byte hash
$iterations = 100000
$hashBytes = New-Object byte[] 32
$rfc2898 = New-Object System.Security.Cryptography.Rfc2898DeriveBytes($tokenPlain, $saltBytes, $iterations, [System.Security.Cryptography.HashAlgorithmName]::SHA256)
$hashBytes = $rfc2898.GetBytes(32)
$hashBase64 = [Convert]::ToBase64String($hashBytes)

Write-Host ""
Write-Host "Success! Use the following environment variables for your LAN server:" -ForegroundColor Green
Write-Host "CIR_ACCESS_TOKEN_HASH=$hashBase64"
Write-Host "CIR_ACCESS_TOKEN_SALT=$saltBase64"
Write-Host ""
Write-Host "Store these securely and never commit them to source control." -ForegroundColor Yellow
