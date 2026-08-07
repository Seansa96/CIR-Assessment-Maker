using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;

var root = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..", "data"));
var repo = new FileAssessmentRepository(new FileStorageOptions { DataRoot = root }, new AssessmentValidator());
foreach (var id in args)
{
    try
    {
        var assessment = await repo.GetByIdAsync(id);
        Console.WriteLine($"OK {id}: {assessment?.Questions.Count}");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"FAIL {id}\n{ex}");
    }
}
