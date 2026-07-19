using QuizApp.Infrastructure.Files;

namespace QuizApp.Tests;

public sealed class QuestionBankAuditTests
{
    [Fact]
    [Trait("Category", "ContentValidation")]
    public void Repository_question_bank_registry_has_no_unregistered_or_invalid_approved_banks()
    {
        var repositoryRoot = FindRepositoryRoot();
        var referenceRoot = Path.Combine(repositoryRoot, "docs", "assessment-reference");

        var result = new QuestionBankAudit().AuditRegistry(referenceRoot);

        Assert.True(result.IsValid, string.Join(Environment.NewLine, result.Errors));
    }

    [Fact]
    public void AuditRegistry_accepts_verified_unique_approved_bank()
    {
        var root = CreateRoot();
        WriteRegistry(root, "approved");
        File.WriteAllText(Path.Combine(root, "bank-question-bank.yaml"), ValidBank());

        var result = new QuestionBankAudit().AuditRegistry(root);

        Assert.True(result.IsValid, string.Join(Environment.NewLine, result.Errors));
        Assert.Empty(result.Warnings);
    }

    [Fact]
    public void AuditRegistry_accepts_latex_inside_display_math_delimiters()
    {
        var root = CreateRoot();
        WriteRegistry(root, "approved");
        var bank = ValidBank().Replace(
            @"$\sum_{n=1}^{\infty}(-1)^{n-1}/n$",
            @"$$\sum_{n=1}^{\infty}(-1)^{n-1}/n$$",
            StringComparison.Ordinal);
        File.WriteAllText(Path.Combine(root, "bank-question-bank.yaml"), bank);

        var result = new QuestionBankAudit().AuditRegistry(root);

        Assert.True(result.IsValid, string.Join(Environment.NewLine, result.Errors));
    }

    [Fact]
    public void AuditRegistry_rejects_duplicates_placeholders_unsafe_math_and_unverified_answers()
    {
        var root = CreateRoot();
        WriteRegistry(root, "approved");
        var invalid = ValidBank()
            .Replace("bank-q002", "bank-q001", StringComparison.Ordinal)
            .Replace("Which condition fails for the series", "Did you understand this step? Which condition fails for the series", StringComparison.Ordinal)
            .Replace(@"$\sum_{n=1}^{\infty}(-1)^{n-1}/n$", @"\sum_{n=1}^{\infty}(-1)^{n-1}/n", StringComparison.Ordinal)
            .Replace("reviewStatus: verified", "reviewStatus: draft", StringComparison.Ordinal);
        File.WriteAllText(Path.Combine(root, "bank-question-bank.yaml"), invalid);

        var result = new QuestionBankAudit().AuditRegistry(root);

        Assert.Contains(result.Errors, issue => issue.Code == "BANK_DUPLICATE_ITEM_ID");
        Assert.Contains(result.Errors, issue => issue.Code == "BANK_PLACEHOLDER_PHRASE");
        Assert.Contains(result.Errors, issue => issue.Code == "BANK_UNDELIMITED_LATEX");
        Assert.Contains(result.Errors, issue => issue.Code == "BANK_UNVERIFIED_ANSWER");
    }

    [Fact]
    public void AuditRegistry_allows_documented_quarantine_but_rejects_unregistered_banks()
    {
        var root = CreateRoot();
        WriteRegistry(root, "quarantined", "Known repetitive source.");
        File.WriteAllText(Path.Combine(root, "bank-question-bank.yaml"), "not: [valid");
        File.WriteAllText(Path.Combine(root, "unregistered-question-bank.yaml"), "items: []");

        var result = new QuestionBankAudit().AuditRegistry(root);

        Assert.Contains(result.Warnings, issue => issue.Code == "BANK_QUARANTINED");
        Assert.Contains(result.Errors, issue => issue.Code == "BANK_UNREGISTERED");
        Assert.DoesNotContain(result.Errors, issue => issue.Code == "BANK_PARSE");
    }

    [Fact]
    public void AuditRegistry_rejects_missing_answers_and_registry_category_mismatches()
    {
        var root = CreateRoot();
        WriteRegistry(root, "approved");
        var invalid = ValidBank()
            .Replace("categoryId: calculus-2", "categoryId: algebra", StringComparison.Ordinal)
            .Replace("    answer:\n      choiceId: a\n", string.Empty, StringComparison.Ordinal);
        File.WriteAllText(Path.Combine(root, "bank-question-bank.yaml"), invalid);

        var result = new QuestionBankAudit().AuditRegistry(root);

        Assert.Contains(result.Errors, issue => issue.Code == "BANK_CATEGORY_MISMATCH");
        Assert.Contains(result.Errors, issue => issue.Code == "BANK_REQUIRED_FIELD");
    }

    private static string CreateRoot()
    {
        var root = Path.Combine(AppContext.BaseDirectory, "question-bank-audit-tests", Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(root);
        return root;
    }

    private static string FindRepositoryRoot()
    {
        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current is not null && !Directory.Exists(Path.Combine(current.FullName, "docs", "assessment-reference")))
        {
            current = current.Parent;
        }

        return current?.FullName
            ?? throw new DirectoryNotFoundException("Could not locate docs/assessment-reference.");
    }

    private static void WriteRegistry(string root, string status, string? reason = null)
    {
        File.WriteAllText(Path.Combine(root, "question-bank-registry.yaml"), $$"""
            schemaVersion: 1
            managedRoots:
              - .
            banks:
              - id: bank
                path: bank-question-bank.yaml
                status: {{status}}
                categoryId: calculus-2
                {{(reason is null ? string.Empty : $"reason: {reason}")}}
            """);
    }

    private static string ValidBank()
        => """
            schemaVersion: 1
            bankId: bank
            categoryId: calculus-2
            topicIds:
              - alternating-series
            minimumItemCount: 2
            items:
              - id: bank-q001
                topicId: alternating-series
                skills:
                  - verify-alternating-series-hypotheses
                archetype: hypothesis-check
                difficulty: foundation
                reasoningDepth: 2
                difficultyEvidence: Requires checking the magnitude limit and monotonicity.
                assessmentUses:
                  - easy-quiz
                questionType: multipleChoice
                prompt: 'Which condition fails for the series $\sum_{n=1}^{\infty}(-1)^{n-1}/n$?'
                answer:
                  choiceId: a
                solutionOutline: The magnitude tends to zero and decreases, so no condition fails.
                commonTrap: Treating alternating signs alone as sufficient.
                verification:
                  method: independent-derivation
                  result: verified
                reviewStatus: verified
              - id: bank-q002
                topicId: alternating-series
                skills:
                  - bound-alternating-series-remainders
                archetype: remainder-bound
                difficulty: hard
                reasoningDepth: 3
                difficultyEvidence: Requires solving an inequality after applying the remainder theorem.
                assessmentUses:
                  - hard-test
                questionType: numericResponse
                prompt: 'Find the least $N$ for which the alternating harmonic remainder is below $1/(N+1)$.'
                answer:
                  value: 1
                solutionOutline: Apply the next-term remainder bound and solve the strict inequality for an integer.
                commonTrap: Replacing a strict bound by a non-strict one.
                verification:
                  method: theorem-and-bound-check
                  result: verified
                reviewStatus: verified
            """;
}
