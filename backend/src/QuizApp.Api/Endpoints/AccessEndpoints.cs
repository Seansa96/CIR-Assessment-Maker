using System.Security.Claims;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Mvc;
using QuizApp.Api.Security;

namespace QuizApp.Api.Endpoints;

public static class AccessEndpoints
{
    public static void MapAccessEndpoints(this IEndpointRouteBuilder routes)
    {
        var group = routes.MapGroup("/api/access");

        group.MapGet("/status", (HttpContext context) =>
        {
            return Results.Ok(new { isAuthenticated = context.User.Identity?.IsAuthenticated ?? false });
        }).AllowAnonymous();

        group.MapPost("/login", async ([FromBody] LoginRequest request, HttpContext context, SharedTokenAuthenticator authenticator) =>
        {
            if (string.IsNullOrWhiteSpace(request.Token))
            {
                return Results.Text("Access token was not accepted.", statusCode: 401);
            }

            if (!authenticator.VerifyToken(request.Token))
            {
                // Note: The plan says "return 429 without indicating whether the token was close or malformed"
                // But that's only for rate limiting. Here we just return 401 generic error.
                return Results.Text("Access token was not accepted.", statusCode: 401);
            }

            var sessionId = Guid.NewGuid().ToString("n");
            var claims = new List<Claim>
            {
                new Claim("SessionId", sessionId)
            };

            var identity = new ClaimsIdentity(claims, CookieAuthenticationDefaults.AuthenticationScheme);
            var principal = new ClaimsPrincipal(identity);

            await context.SignInAsync(CookieAuthenticationDefaults.AuthenticationScheme, principal, new AuthenticationProperties
            {
                IsPersistent = false,
                ExpiresUtc = DateTimeOffset.UtcNow.AddHours(12)
            });

            return Results.Ok(new { success = true });
        })
        .RequireRateLimiting("LoginLimiter")
        .AllowAnonymous();

        group.MapPost("/logout", async (HttpContext context) =>
        {
            await context.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
            return Results.Ok(new { success = true });
        }).AllowAnonymous();

        routes.MapGet("/health/live", () => Results.Ok(new { status = "Healthy" })).AllowAnonymous();
    }
}

public sealed class LoginRequest
{
    public string? Token { get; set; }
}
