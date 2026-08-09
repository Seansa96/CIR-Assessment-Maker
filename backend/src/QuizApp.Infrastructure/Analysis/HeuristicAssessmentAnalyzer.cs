using System.Text.Json;
using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Infrastructure.Analysis;

public sealed class HeuristicAssessmentAnalyzer : ILocalAssessmentAnalyzer
{
    private readonly FileStorageOptions storageOptions;
    private DictionaryModel? dictionary;

    public HeuristicAssessmentAnalyzer(FileStorageOptions storageOptions)
    {
        this.storageOptions = storageOptions;
    }

    private async Task EnsureDictionaryLoadedAsync(CancellationToken cancellationToken)
    {
        if (dictionary is not null) return;
        
        var path = Path.Combine(storageOptions.DataRoot, "nlp-dictionary.json");
        if (File.Exists(path))
        {
            var json = await File.ReadAllTextAsync(path, cancellationToken);
            dictionary = JsonSerializer.Deserialize<DictionaryModel>(json, new JsonSerializerOptions(JsonSerializerDefaults.Web));
        }
        
        dictionary ??= new DictionaryModel(Array.Empty<SkillEntry>(), Array.Empty<SignalEntry>(), Array.Empty<TagEntry>());
    }

    public async Task<AssessmentDefinition> AnalyzeAsync(AssessmentDefinition assessment, CancellationToken cancellationToken = default)
    {
        await EnsureDictionaryLoadedAsync(cancellationToken);

        var textCorpus = ExtractTextCorpus(assessment).ToLowerInvariant();
        
        var newSkills = new HashSet<string>(assessment.Skills, StringComparer.OrdinalIgnoreCase);
        var newTags = new HashSet<string>(assessment.Navigation?.Tags ?? Array.Empty<string>(), StringComparer.OrdinalIgnoreCase);
        
        if (dictionary is not null)
        {
            foreach (var skill in dictionary.Skills)
            {
                if (skill.Keywords.Any(k => textCorpus.Contains(k.ToLowerInvariant())))
                {
                    newSkills.Add(skill.SkillId);
                }
            }

            foreach (var tag in dictionary.Tags)
            {
                if (tag.Keywords.Any(k => textCorpus.Contains(k.ToLowerInvariant())))
                {
                    newTags.Add(tag.Tag);
                }
            }
        }

        var nav = assessment.Navigation ?? new NavigationMetadata(null, null, Array.Empty<string>());
        nav = nav with { Tags = newTags.OrderBy(t => t).ToList() };

        var newQuestions = new List<QuestionDefinition>();
        foreach (var q in assessment.Questions)
        {
            var qText = (q.Prompt + " " + q.Explanation + " " + string.Join(" ", q.Choices.Select(c => c.Text))).ToLowerInvariant();
            var qSkills = new HashSet<string>(q.Skills, StringComparer.OrdinalIgnoreCase);
            var qSignals = new List<IssueSignal>(q.IssueSignals);
            var newChoices = new List<ChoiceOption>(q.Choices);

            if (dictionary is not null)
            {
                foreach (var skill in dictionary.Skills)
                {
                    if (skill.Keywords.Any(k => qText.Contains(k.ToLowerInvariant())))
                    {
                        qSkills.Add(skill.SkillId);
                    }
                }
                
                if (q.Type == QuestionType.MultipleChoice || q.Type == QuestionType.SelectAll)
                {
                    newChoices.Clear();
                    foreach (var choice in q.Choices)
                    {
                        var isCorrect = (q.Answer.ChoiceId != null && string.Equals(choice.Id, q.Answer.ChoiceId, StringComparison.OrdinalIgnoreCase))
                            || (q.Answer.ChoiceIds != null && q.Answer.ChoiceIds.Contains(choice.Id, StringComparer.OrdinalIgnoreCase));
                            
                        if (isCorrect) 
                        {
                            newChoices.Add(choice);
                            continue;
                        }
                        
                        var choiceSignals = new List<IssueSignal>(choice.IssueSignals);
                        var existingSignalIds = new HashSet<string>(choice.IssueSignals.Select(s => s.Id), StringComparer.OrdinalIgnoreCase);
                        
                        foreach (var signal in dictionary.IssueSignals)
                        {
                            if (existingSignalIds.Contains(signal.SignalId)) continue;
                            
                            var choiceText = choice.Text.ToLowerInvariant();
                            if (signal.Keywords.Any(k => choiceText.Contains(k.ToLowerInvariant())))
                            {
                                choiceSignals.Add(new IssueSignal(signal.SignalId, Array.Empty<string>()));
                                existingSignalIds.Add(signal.SignalId);
                            }
                        }
                        
                        newChoices.Add(choice with { IssueSignals = choiceSignals });
                    }
                }
                else
                {
                    var existingSignalIds = new HashSet<string>(q.IssueSignals.Select(s => s.Id), StringComparer.OrdinalIgnoreCase);
                    foreach (var signal in dictionary.IssueSignals)
                    {
                        if (existingSignalIds.Contains(signal.SignalId)) continue;
                        
                        if (signal.Keywords.Any(k => qText.Contains(k.ToLowerInvariant())))
                        {
                            qSignals.Add(new IssueSignal(signal.SignalId, Array.Empty<string>()));
                            existingSignalIds.Add(signal.SignalId);
                        }
                    }
                }
            }

            newQuestions.Add(q with 
            { 
                Skills = qSkills.OrderBy(s => s).ToList(),
                IssueSignals = qSignals,
                Choices = newChoices
            });
        }

        return assessment with 
        { 
            Skills = newSkills.OrderBy(s => s).ToList(),
            Navigation = nav,
            Questions = newQuestions,
            MetadataStatus = MetadataStatus.Coarse
        };
    }

    private string ExtractTextCorpus(AssessmentDefinition assessment)
    {
        var parts = new List<string>
        {
            assessment.Title
        };

        if (assessment.Navigation?.LearningGoal is not null) parts.Add(assessment.Navigation.LearningGoal);
        
        if (assessment.Lesson is not null)
        {
            parts.Add(assessment.Lesson.Introduction);
            foreach (var sec in assessment.Lesson.Sections)
            {
                parts.Add(sec.Content);
            }
        }

        foreach (var q in assessment.Questions)
        {
            parts.Add(q.Prompt);
            if (q.Explanation is not null) parts.Add(q.Explanation);
        }
        
        return string.Join(" ", parts);
    }

    private sealed record DictionaryModel(
        IReadOnlyList<SkillEntry> Skills, 
        IReadOnlyList<SignalEntry> IssueSignals, 
        IReadOnlyList<TagEntry> Tags);
        
    private sealed record SkillEntry(string SkillId, IReadOnlyList<string> Keywords);
    private sealed record SignalEntry(string SignalId, IReadOnlyList<string> Keywords);
    private sealed record TagEntry(string Tag, IReadOnlyList<string> Keywords);
}
