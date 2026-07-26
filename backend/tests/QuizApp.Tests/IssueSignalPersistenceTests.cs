using QuizApp.Core.Domain;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Tests;

public sealed class IssueSignalPersistenceTests
{
    [Fact]
    public void Mapper_round_trips_question_choice_and_part_issue_signals()
    {
        var dto = FileFormat.ReadFromString<AssessmentFileDto>("""
            schemaVersion: 1
            id: signal-test
            title: Signal test
            assessmentType: quiz
            categoryId: calculus-2
            topicId: integration-techniques
            questions:
              - id: q1
                type: multipart
                prompt: Prompt
                issueSignals:
                  - id: integration-by-parts-misapplied
                parts:
                  - id: a
                    type: multipleChoice
                    prompt: Part
                    choices:
                      - id: wrong
                        text: Wrong
                        issueSignals:
                          - id: partial-fraction-decomposition-error
                    answer: { choiceId: wrong }
                  - id: b
                    type: numericResponse
                    prompt: Part two
                    answer: { value: 1, tolerance: 0.1 }
            """)!;

        var roundTripped = dto.ToDomain().ToDto();
        var question = Assert.Single(roundTripped.Questions!);
        Assert.Equal("integration-by-parts-misapplied", Assert.Single(question.IssueSignals!).Id);
        Assert.Equal("partial-fraction-decomposition-error", Assert.Single(question.Parts![0].Choices![0].IssueSignals!).Id);
    }

    [Fact]
    public async Task Catalog_rejects_unknown_and_wrong_domain_signals()
    {
        var root = Path.Combine(Path.GetTempPath(), "issue-signal-tests", Guid.NewGuid().ToString("n"));
        Directory.CreateDirectory(root);
        await File.WriteAllTextAsync(Path.Combine(root, "issue-signals.yaml"), "- id: calculus-only\n  domains: [calculus-2]\n");
        var seed = TestData.Assessment();
        var assessment = seed with
        {
            CategoryId = "physics-1",
            Questions = new[]
            {
                seed.Questions[0] with { IssueSignals = new[] { new IssueSignal("calculus-only", Array.Empty<string>()), new IssueSignal("missing", Array.Empty<string>()) } }
            }
        };

        var issues = await new IssueSignalCatalog(new FileStorageOptions { DataRoot = root }).ValidateAsync(assessment);

        Assert.Contains(issues, issue => issue.Code == "ISSUE_SIGNAL_DOMAIN_MISMATCH");
        Assert.Contains(issues, issue => issue.Code == "UNKNOWN_ISSUE_SIGNAL");
    }
}
