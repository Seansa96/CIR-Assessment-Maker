namespace QuizApp.Core.Services;

public interface IAccessContext
{
    bool IsAuthenticated { get; }
    string? SessionId { get; }
}
