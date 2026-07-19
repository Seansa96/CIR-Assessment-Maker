using System.Text.RegularExpressions;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace QuizApp.Infrastructure.Files;

public sealed record QuestionBankAuditIssue(string Code, string Path, string Message);

public sealed record QuestionBankAuditResult(
    IReadOnlyList<QuestionBankAuditIssue> Errors,
    IReadOnlyList<QuestionBankAuditIssue> Warnings)
{
    public bool IsValid => Errors.Count == 0;
}

public sealed class QuestionBankAudit
{
    private static readonly Regex Whitespace = new(@"\s+", RegexOptions.Compiled);
    private static readonly Regex NumberToken = new(@"(?<![A-Za-z])\d+(?:\.\d+)?", RegexOptions.Compiled);
    private static readonly Regex LatexCommand = new(@"\\(?:sum|frac|sqrt|lim|infty|log|ln|sin|cos|tan|int|pi|theta|left|right|cdot|leq|geq|to)\b", RegexOptions.Compiled);
    private static readonly string[] BannedPhrases =
    [
        "did you understand this step?",
        "use the ratio test....",
        "a definition for this term.",
        "translate the restriction into a usable equation or proof obligation",
        "identify the governing ",
        "find a structural reduction for "
    ];

    private readonly IDeserializer deserializer = new DeserializerBuilder()
        .WithNamingConvention(CamelCaseNamingConvention.Instance)
        .IgnoreUnmatchedProperties()
        .Build();

    public QuestionBankAuditResult AuditRegistry(string assessmentReferenceRoot)
    {
        var errors = new List<QuestionBankAuditIssue>();
        var warnings = new List<QuestionBankAuditIssue>();
        var registryPath = Path.Combine(assessmentReferenceRoot, "question-bank-registry.yaml");
        if (!File.Exists(registryPath))
        {
            errors.Add(new("BANK_REGISTRY_MISSING", registryPath, "Question-bank registry was not found."));
            return new(errors, warnings);
        }

        QuestionBankRegistryFile registry;
        try
        {
            registry = deserializer.Deserialize<QuestionBankRegistryFile>(File.ReadAllText(registryPath))
                ?? new QuestionBankRegistryFile();
        }
        catch (Exception ex)
        {
            errors.Add(new("BANK_REGISTRY_PARSE", registryPath, ex.Message));
            return new(errors, warnings);
        }

        if (registry.SchemaVersion != 1)
        {
            errors.Add(new("BANK_REGISTRY_SCHEMA", registryPath, "Registry schemaVersion must be 1."));
        }
        if (registry.ManagedRoots.Count == 0)
        {
            errors.Add(new("BANK_REGISTRY_MANAGED_ROOTS", registryPath, "Registry must declare at least one managed root."));
        }

        foreach (var duplicate in registry.Banks
                     .GroupBy(bank => bank.Id, StringComparer.OrdinalIgnoreCase)
                     .Where(group => string.IsNullOrWhiteSpace(group.Key) || group.Count() > 1))
        {
            errors.Add(new("BANK_REGISTRY_DUPLICATE_ID", registryPath, $"Bank ID '{duplicate.Key}' is blank or duplicated."));
        }

        var registeredPaths = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var entry in registry.Banks)
        {
            var entryPath = Path.GetFullPath(Path.Combine(assessmentReferenceRoot, entry.Path ?? string.Empty));
            if (!entryPath.StartsWith(Path.GetFullPath(assessmentReferenceRoot) + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase))
            {
                errors.Add(new("BANK_PATH_OUTSIDE_ROOT", registryPath, $"Bank '{entry.Id}' points outside assessment-reference."));
                continue;
            }

            if (!registeredPaths.Add(entryPath))
            {
                errors.Add(new("BANK_REGISTRY_DUPLICATE_PATH", registryPath, $"More than one bank points to '{entry.Path}'."));
            }
            if (!File.Exists(entryPath))
            {
                errors.Add(new("BANK_FILE_MISSING", entryPath, $"Registered bank '{entry.Id}' does not exist."));
                continue;
            }

            if (entry.Status is not ("approved" or "quarantined"))
            {
                errors.Add(new("BANK_STATUS_INVALID", registryPath, $"Bank '{entry.Id}' must be approved or quarantined."));
                continue;
            }

            if (entry.Status == "quarantined")
            {
                if (string.IsNullOrWhiteSpace(entry.Reason))
                {
                    errors.Add(new("BANK_QUARANTINE_REASON", registryPath, $"Quarantined bank '{entry.Id}' needs a reason."));
                }
                warnings.Add(new("BANK_QUARANTINED", entryPath, entry.Reason ?? "Bank is quarantined."));
                continue;
            }

            AuditApprovedBank(entry, entryPath, errors);
        }

        foreach (var managedRoot in registry.ManagedRoots)
        {
            var managedPath = Path.GetFullPath(Path.Combine(assessmentReferenceRoot, managedRoot));
            var normalizedRoot = Path.GetFullPath(assessmentReferenceRoot);
            if (!(string.Equals(managedPath, normalizedRoot, StringComparison.OrdinalIgnoreCase)
                  || managedPath.StartsWith(normalizedRoot + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase))
                || !Directory.Exists(managedPath))
            {
                errors.Add(new("BANK_MANAGED_ROOT", registryPath, $"Managed root '{managedRoot}' is missing or outside assessment-reference."));
                continue;
            }

            foreach (var bankPath in Directory.EnumerateFiles(managedPath, "*question-bank.yaml", SearchOption.AllDirectories))
            {
                if (!registeredPaths.Contains(Path.GetFullPath(bankPath)))
                {
                    errors.Add(new("BANK_UNREGISTERED", bankPath, "Question bank must be registered as approved or quarantined."));
                }
            }
        }

        return new(errors, warnings);
    }

    private void AuditApprovedBank(
        QuestionBankRegistryEntry registryEntry,
        string path,
        List<QuestionBankAuditIssue> errors)
    {
        QuestionBankFile bank;
        try
        {
            bank = deserializer.Deserialize<QuestionBankFile>(File.ReadAllText(path)) ?? new QuestionBankFile();
        }
        catch (Exception ex)
        {
            errors.Add(new("BANK_PARSE", path, ex.Message));
            return;
        }

        if (bank.SchemaVersion != 1 || string.IsNullOrWhiteSpace(bank.BankId))
        {
            errors.Add(new("BANK_METADATA", path, "Approved bank requires schemaVersion 1 and bankId."));
        }
        else if (!string.Equals(bank.BankId, registryEntry.Id, StringComparison.OrdinalIgnoreCase))
        {
            errors.Add(new("BANK_ID_MISMATCH", path, $"bankId '{bank.BankId}' does not match registry ID '{registryEntry.Id}'."));
        }

        if (string.IsNullOrWhiteSpace(bank.CategoryId) || bank.TopicIds.Count == 0)
        {
            errors.Add(new("BANK_CLASSIFICATION", path, "Approved bank requires categoryId and at least one topicId."));
        }
        else if (!string.IsNullOrWhiteSpace(registryEntry.CategoryId)
                 && !string.Equals(bank.CategoryId, registryEntry.CategoryId, StringComparison.OrdinalIgnoreCase))
        {
            errors.Add(new(
                "BANK_CATEGORY_MISMATCH",
                path,
                $"Bank categoryId '{bank.CategoryId}' does not match registry categoryId '{registryEntry.CategoryId}'."));
        }

        var minimum = Math.Max(1, bank.MinimumItemCount);
        if (bank.Items.Count < minimum)
        {
            errors.Add(new("BANK_ITEM_COUNT", path, $"Approved bank has {bank.Items.Count} items; minimum is {minimum}."));
        }

        foreach (var duplicate in bank.Items
                     .GroupBy(item => item.Id, StringComparer.OrdinalIgnoreCase)
                     .Where(group => string.IsNullOrWhiteSpace(group.Key) || group.Count() > 1))
        {
            errors.Add(new("BANK_DUPLICATE_ITEM_ID", path, $"Item ID '{duplicate.Key}' is blank or duplicated."));
        }

        var promptGroups = bank.Items.GroupBy(item => Normalize(item.Prompt), StringComparer.Ordinal).Where(group => group.Key.Length == 0 || group.Count() > 1);
        foreach (var group in promptGroups)
        {
            errors.Add(new("BANK_DUPLICATE_PROMPT", path, $"Normalized prompt is blank or repeated {group.Count()} times."));
        }

        var outlineGroups = bank.Items.GroupBy(item => Normalize(item.SolutionOutline), StringComparer.Ordinal).Where(group => group.Key.Length == 0 || group.Count() > 1);
        foreach (var group in outlineGroups)
        {
            errors.Add(new("BANK_DUPLICATE_OUTLINE", path, $"Normalized solution outline is blank or repeated {group.Count()} times."));
        }

        foreach (var group in bank.Items.GroupBy(item => ParameterSkeleton(item.Prompt), StringComparer.Ordinal).Where(group => group.Key.Length > 0 && group.Count() > 2))
        {
            errors.Add(new("BANK_PARAMETER_VARIANTS", path, $"{group.Count()} prompts differ only by numeric parameters."));
        }

        foreach (var item in bank.Items)
        {
            var itemPath = $"{path}#{item.Id}";
            if (!bank.TopicIds.Contains(item.TopicId, StringComparer.OrdinalIgnoreCase))
            {
                errors.Add(new("BANK_TOPIC_MISMATCH", itemPath, $"Item topicId '{item.TopicId}' is not declared by its bank."));
            }

            if (item.Skills.Count == 0 || string.IsNullOrWhiteSpace(item.Archetype)
                || string.IsNullOrWhiteSpace(item.Difficulty) || item.AssessmentUses.Count == 0
                || string.IsNullOrWhiteSpace(item.QuestionType) || string.IsNullOrWhiteSpace(item.CommonTrap)
                || item.Answer is null)
            {
                errors.Add(new("BANK_REQUIRED_FIELD", itemPath, "Item is missing skills, archetype, difficulty, assessmentUses, questionType, answer, or commonTrap."));
            }

            if (item.ReviewStatus != "verified" || item.Verification?.Result != "verified"
                || string.IsNullOrWhiteSpace(item.Verification.Method))
            {
                errors.Add(new("BANK_UNVERIFIED_ANSWER", itemPath, "Approved items require verified reviewStatus and verification method/result."));
            }

            if (item.Difficulty is "hard" or "olympiad")
            {
                if (item.ReasoningDepth < 2 || string.IsNullOrWhiteSpace(item.DifficultyEvidence))
                {
                    errors.Add(new("BANK_DIFFICULTY_EVIDENCE", itemPath, "Hard/Olympiad items require reasoningDepth >= 2 and difficultyEvidence."));
                }
            }

            foreach (var text in new[] { item.Prompt, item.SolutionOutline, item.CommonTrap, item.DifficultyEvidence })
            {
                if (ContainsControlCharacters(text))
                {
                    errors.Add(new("BANK_CONTROL_CHARACTER", itemPath, "Rendered text contains a control character."));
                }
                if (ContainsUndelimitedLatex(text))
                {
                    errors.Add(new("BANK_UNDELIMITED_LATEX", itemPath, "LaTeX commands must be inside Markdown math delimiters."));
                }
                if (BannedPhrases.Any(phrase => text.Contains(phrase, StringComparison.OrdinalIgnoreCase)))
                {
                    errors.Add(new("BANK_PLACEHOLDER_PHRASE", itemPath, "Rendered text contains banned placeholder language."));
                }
            }
        }
    }

    private static string Normalize(string? value)
        => Whitespace.Replace(value?.Trim().ToLowerInvariant() ?? string.Empty, " ");

    private static string ParameterSkeleton(string? value)
        => NumberToken.Replace(Normalize(value), "#");

    private static bool ContainsControlCharacters(string? value)
        => value?.Any(character => char.IsControl(character) && character is not ('\r' or '\n' or '\t')) == true;

    private static bool ContainsUndelimitedLatex(string? value)
    {
        if (string.IsNullOrEmpty(value) || !LatexCommand.IsMatch(value))
        {
            return false;
        }

        var inMath = false;
        var escaped = false;
        for (var index = 0; index < value.Length; index++)
        {
            var character = value[index];
            if (character == '\\')
            {
                escaped = !escaped;
                if (!inMath && LatexCommand.IsMatch(value, index))
                {
                    return true;
                }
                continue;
            }

            if (character == '$' && !escaped)
            {
                inMath = !inMath;
                if (index + 1 < value.Length && value[index + 1] == '$')
                {
                    index++;
                }
            }
            escaped = false;
        }

        return false;
    }

    private sealed class QuestionBankRegistryFile
    {
        public int SchemaVersion { get; set; }
        public List<string> ManagedRoots { get; set; } = [];
        public List<QuestionBankRegistryEntry> Banks { get; set; } = [];
    }

    private sealed class QuestionBankRegistryEntry
    {
        public string Id { get; set; } = string.Empty;
        public string? Path { get; set; }
        public string Status { get; set; } = string.Empty;
        public string? CategoryId { get; set; }
        public string? Reason { get; set; }
    }

    private sealed class QuestionBankFile
    {
        public int SchemaVersion { get; set; }
        public string BankId { get; set; } = string.Empty;
        public string CategoryId { get; set; } = string.Empty;
        public List<string> TopicIds { get; set; } = [];
        public int MinimumItemCount { get; set; }
        public List<QuestionBankItem> Items { get; set; } = [];
    }

    private sealed class QuestionBankItem
    {
        public string Id { get; set; } = string.Empty;
        public string TopicId { get; set; } = string.Empty;
        public List<string> Skills { get; set; } = [];
        public string Archetype { get; set; } = string.Empty;
        public string Difficulty { get; set; } = string.Empty;
        public int ReasoningDepth { get; set; }
        public string DifficultyEvidence { get; set; } = string.Empty;
        public List<string> AssessmentUses { get; set; } = [];
        public string QuestionType { get; set; } = string.Empty;
        public string Prompt { get; set; } = string.Empty;
        public object? Answer { get; set; }
        public string SolutionOutline { get; set; } = string.Empty;
        public string CommonTrap { get; set; } = string.Empty;
        public QuestionBankVerification? Verification { get; set; }
        public string ReviewStatus { get; set; } = string.Empty;
    }

    private sealed class QuestionBankVerification
    {
        public string Method { get; set; } = string.Empty;
        public string Result { get; set; } = string.Empty;
    }
}
