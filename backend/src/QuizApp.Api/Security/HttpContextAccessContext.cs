using System.Security.Claims;
using QuizApp.Core.Services;

namespace QuizApp.Api.Security;

public sealed class HttpContextAccessContext : IAccessContext
{
    private readonly IHttpContextAccessor accessor;

    public HttpContextAccessContext(IHttpContextAccessor accessor)
    {
        this.accessor = accessor;
    }

    public bool IsAuthenticated => accessor.HttpContext?.User?.Identity?.IsAuthenticated ?? false;

    public string? SessionId => accessor.HttpContext?.User?.FindFirstValue("SessionId");
}
