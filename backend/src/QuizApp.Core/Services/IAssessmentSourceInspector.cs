using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public interface IAssessmentSourceInspector
{
    AssessmentSourceInspection Inspect(string content, string extension, string? sourcePath = null);
}
