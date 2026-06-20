using System.Security.Cryptography;
using Microsoft.AspNetCore.Cryptography.KeyDerivation;

namespace QuizApp.Api.Security;

public sealed class SharedTokenAuthenticator
{
    private readonly string? expectedHash;
    private readonly byte[]? expectedSalt;

    public SharedTokenAuthenticator(IConfiguration configuration)
    {
        expectedHash = configuration["CIR_ACCESS_TOKEN_HASH"];
        var saltBase64 = configuration["CIR_ACCESS_TOKEN_SALT"];
        
        if (!string.IsNullOrWhiteSpace(saltBase64))
        {
            try
            {
                expectedSalt = Convert.FromBase64String(saltBase64);
            }
            catch
            {
                expectedSalt = null;
            }
        }
    }

    public bool IsConfigured => !string.IsNullOrWhiteSpace(expectedHash) && expectedSalt is not null;

    public bool VerifyToken(string token)
    {
        if (!IsConfigured || expectedSalt is null || string.IsNullOrWhiteSpace(expectedHash))
        {
            return false;
        }

        try
        {
            var hash = HashToken(token, expectedSalt);
            return CryptographicOperations.FixedTimeEquals(
                Convert.FromBase64String(hash),
                Convert.FromBase64String(expectedHash));
        }
        catch
        {
            return false;
        }
    }

    public static string HashToken(string token, byte[] salt)
    {
        // Use PBKDF2 with HMACSHA256, 100,000 iterations, 32-byte hash
        var hashBytes = KeyDerivation.Pbkdf2(
            password: token,
            salt: salt,
            prf: KeyDerivationPrf.HMACSHA256,
            iterationCount: 100000,
            numBytesRequested: 32);

        return Convert.ToBase64String(hashBytes);
    }
}
