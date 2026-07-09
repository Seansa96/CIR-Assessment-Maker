using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Core.Services;

public sealed class GradeAnalyticsService
{
    private readonly IGradeLogRepository gradeLogRepository;
    private readonly IAttemptRepository attemptRepository;
    private readonly IAttemptSessionStore attemptSessionStore;
    private readonly IAssessmentRepository assessmentRepository;
    private readonly ICategoryRepository categoryRepository;
    private readonly IAreaRepository areaRepository;
    private readonly INavigationCatalogService catalogService;
    private readonly ScoringService scoringService;

    public GradeAnalyticsService(
        IGradeLogRepository gradeLogRepository,
        IAttemptRepository attemptRepository,
        IAttemptSessionStore attemptSessionStore,
        IAssessmentRepository assessmentRepository,
        ICategoryRepository categoryRepository,
        IAreaRepository areaRepository,
        INavigationCatalogService catalogService,
        ScoringService scoringService)
    {
        this.gradeLogRepository = gradeLogRepository;
        this.attemptRepository = attemptRepository;
        this.attemptSessionStore = attemptSessionStore;
        this.assessmentRepository = assessmentRepository;
        this.categoryRepository = categoryRepository;
        this.areaRepository = areaRepository;
        this.catalogService = catalogService;
        this.scoringService = scoringService;
    }

    public async Task<GradeAnalyticsSummary> GetSummaryAsync(GradeAnalyticsFilter filter, CancellationToken cancellationToken = default)
    {
        var entries = await gradeLogRepository.ListAsync(cancellationToken);
        var attempts = await ListAllAttemptsAsync(cancellationToken);
        var categories = await categoryRepository.ListAsync(cancellationToken);
        var areas = await areaRepository.ListAsync(cancellationToken);
        var assessmentLookup = await BuildAssessmentLookupAsync(entries.Select(entry => entry.AssessmentId)
            .Concat(attempts.Select(attempt => attempt.AssessmentId)), cancellationToken);

        var committedAttemptIds = entries.Select(entry => entry.AttemptId).ToHashSet(StringComparer.OrdinalIgnoreCase);
        var historyRows = BuildAttemptRows(attempts, assessmentLookup, categories, areas, committedAttemptIds)
            .Where(row => MatchesFilter(row, filter))
            .OrderByDescending(row => row.LastActivityAt ?? row.StartedAt)
            .ToList();

        var filteredCommittedEntries = entries
            .Where(entry => assessmentLookup.ContainsKey(entry.AssessmentId))
            .Where(entry => historyRows.Any(row => string.Equals(row.AttemptId, entry.AttemptId, StringComparison.OrdinalIgnoreCase)))
            .ToList();

        var categorySummaries = BuildCategorySummaries(filteredCommittedEntries, assessmentLookup, categories);
        var subcategorySummaries = BuildSubcategorySummaries(filteredCommittedEntries, assessmentLookup, categories);
        var areaSummaries = BuildAreaSummaries(filteredCommittedEntries, assessmentLookup, categories, areas);
        var questionTypeSummaries = BuildQuestionTypeSummaries(historyRows, attempts, assessmentLookup, filter.QuestionType);
        var recallRatingSummaries = BuildRecallRatingSummaries(historyRows, attempts, assessmentLookup);
        var recallTagSummaries = BuildRecallTagSummaries(historyRows, attempts, assessmentLookup);
        var recallCategorySummaries = BuildRecallCategorySummaries(historyRows, attempts, assessmentLookup, categories);
        var recallSubcategorySummaries = BuildRecallSubcategorySummaries(historyRows, attempts, assessmentLookup, categories);
        var weakAreas = BuildWeakFocusSummaries(categorySummaries, areaSummaries);
        var skillSummaries = BuildSkillPerformanceSummaries(historyRows, attempts, assessmentLookup);
        var catalog = await catalogService.GetCatalogAsync(cancellationToken);
        var actionableNextSteps = BuildActionableNextSteps(skillSummaries, recallTagSummaries, catalog, assessmentLookup, categories, areas);

        return new GradeAnalyticsSummary(
            filteredCommittedEntries.Count,
            ComputeWeightedAverage(filteredCommittedEntries, assessmentLookup),
            categorySummaries.OrderBy(summary => summary.AveragePercent).ThenByDescending(summary => summary.AttemptCount)
                .Select(summary => new AnalyticsFocus(summary.CategoryId, summary.CategoryTitle, summary.AttemptCount, summary.AveragePercent))
                .FirstOrDefault(),
            areaSummaries.OrderBy(summary => summary.AveragePercent).ThenByDescending(summary => summary.AttemptCount)
                .Select(summary => new AnalyticsFocus(summary.AreaId, summary.AreaTitle, summary.AttemptCount, summary.AveragePercent))
                .FirstOrDefault(),
            questionTypeSummaries.Where(summary => summary.AnsweredCount > 0)
                .OrderBy(summary => summary.CorrectPercent)
                .ThenByDescending(summary => summary.AnsweredCount)
                .FirstOrDefault(),
            categorySummaries,
            subcategorySummaries,
            areaSummaries,
            questionTypeSummaries,
            recallRatingSummaries,
            recallTagSummaries,
            recallCategorySummaries,
            recallSubcategorySummaries,
            weakAreas,
            skillSummaries,
            actionableNextSteps,
            historyRows);
    }

    private async Task<IReadOnlyList<Attempt>> ListAllAttemptsAsync(CancellationToken cancellationToken)
    {
        var active = await attemptSessionStore.ListAsync(cancellationToken);
        var persisted = await attemptRepository.ListAsync(cancellationToken);
        return active
            .Concat(persisted)
            .GroupBy(attempt => attempt.Id, StringComparer.OrdinalIgnoreCase)
            .Select(group => group.First())
            .ToList();
    }

    private async Task<Dictionary<string, AssessmentDefinition>> BuildAssessmentLookupAsync(IEnumerable<string> assessmentIds, CancellationToken cancellationToken)
    {
        var lookup = new Dictionary<string, AssessmentDefinition>(StringComparer.OrdinalIgnoreCase);
        foreach (var assessmentId in assessmentIds.Where(id => !string.IsNullOrWhiteSpace(id)).Distinct(StringComparer.OrdinalIgnoreCase))
        {
            var assessment = await assessmentRepository.GetByIdAsync(assessmentId, cancellationToken);
            if (assessment is not null)
            {
                lookup[assessment.Id] = assessment;
            }
        }

        return lookup;
    }

    private static IReadOnlyList<AttemptHistoryRow> BuildAttemptRows(
        IReadOnlyList<Attempt> attempts,
        IReadOnlyDictionary<string, AssessmentDefinition> assessments,
        IReadOnlyList<Category> categories,
        IReadOnlyList<AreaDefinition> areas,
        ISet<string> committedAttemptIds)
    {
        return attempts
            .Where(attempt => assessments.ContainsKey(attempt.AssessmentId))
            .Select(attempt =>
            {
                var assessment = assessments[attempt.AssessmentId];
                var category = categories.FirstOrDefault(candidate => string.Equals(candidate.Id, assessment.CategoryId, StringComparison.OrdinalIgnoreCase));
                var subcategoryTitles = assessment.SubcategoryIds
                    .Select(subcategoryId => category?.Subcategories.FirstOrDefault(subcategory => string.Equals(subcategory.Id, subcategoryId, StringComparison.OrdinalIgnoreCase))?.Title ?? subcategoryId)
                    .ToList();
                var matchingAreas = MatchAreas(assessment, areas).ToList();
                var correctCount = assessment.AssessmentType is AssessmentType.RecallDrill or AssessmentType.Glossary
                    ? attempt.RecallItems.Count(item => item.Rating is RecallRating.Easy or RecallRating.Correct)
                    : assessment.AssessmentType is AssessmentType.ConceptLesson or AssessmentType.InteractiveExploration
                        ? attempt.LearningSections.Count(section => section.Completed)
                    : attempt.Answers.Count(answer => answer.Evaluation?.IsCorrect == true);
                var totalQuestions = attempt.QuestionOrder.Count;
                var answeredCount = assessment.AssessmentType is AssessmentType.RecallDrill or AssessmentType.Glossary
                    ? attempt.RecallItems.Count(item => item.Rating is not RecallRating.Unknown)
                    : assessment.AssessmentType is AssessmentType.ConceptLesson or AssessmentType.InteractiveExploration
                        ? attempt.LearningSections.Count(section => section.Visited)
                    : attempt.Answers.Count(answer => answer.Answer is not null);

                return new AttemptHistoryRow(
                    attempt.Id,
                    assessment.Id,
                    assessment.Title,
                    assessment.AssessmentType,
                    attempt.Mode,
                    attempt.Status,
                    assessment.CategoryId,
                    category?.Title ?? assessment.CategoryId,
                    assessment.SubcategoryIds,
                    subcategoryTitles,
                    matchingAreas.Select(area => area.Id).ToList(),
                    matchingAreas.Select(area => area.Title).ToList(),
                    ExtractQuestionTypes(assessment),
                    correctCount,
                    totalQuestions,
                    totalQuestions == 0 ? 0 : Math.Round(correctCount * 100m / totalQuestions, 2),
                    answeredCount,
                    attempt.Answers.Any(answer => answer.Answer.FreeResponseText is not null && answer.Answer.SelfCheckCorrect is null),
                    committedAttemptIds.Contains(attempt.Id),
                    attempt.StartedAt,
                    attempt.CompletedAt,
                    attempt.CompletedAt ?? attempt.AbandonedAt ?? attempt.PausedAt ?? attempt.Answers.OrderByDescending(answer => answer.SubmittedAt).FirstOrDefault()?.SubmittedAt ?? attempt.StartedAt,
                    NavigationInference.Infer(assessment).LearningGoal,
                    NavigationInference.Infer(assessment).ActivityType);
            })
            .ToList();
    }

    private static IReadOnlyList<RecallRatingAnalytics> BuildRecallRatingSummaries(
        IReadOnlyList<AttemptHistoryRow> rows,
        IReadOnlyList<Attempt> attempts,
        IReadOnlyDictionary<string, AssessmentDefinition> assessments)
    {
        var recallAttempts = CompletedRecallAttempts(rows, attempts, assessments);
        return recallAttempts
            .SelectMany(attempt => attempt.RecallItems)
            .Where(item => item.Rating is not RecallRating.Unknown)
            .GroupBy(item => item.Rating)
            .Select(group => new RecallRatingAnalytics(group.Key, group.Count()))
            .OrderBy(summary => summary.Rating)
            .ToList();
    }

    private static IReadOnlyList<RecallTagAnalytics> BuildRecallTagSummaries(
        IReadOnlyList<AttemptHistoryRow> rows,
        IReadOnlyList<Attempt> attempts,
        IReadOnlyDictionary<string, AssessmentDefinition> assessments)
    {
        var records = RecallRecords(rows, attempts, assessments);
        return records
            .SelectMany(record => record.Item.Tags.Select(tag => new { Tag = tag, record.Rating }))
            .Where(item => !string.IsNullOrWhiteSpace(item.Tag) && item.Rating is not RecallRating.Unknown)
            .GroupBy(item => item.Tag, StringComparer.OrdinalIgnoreCase)
            .Select(group => new RecallTagAnalytics(
                group.Key,
                group.Count(),
                Math.Round(group.Average(item => RatingValue(item.Rating)), 2),
                group.Count(item => IsWeakRating(item.Rating))))
            .OrderByDescending(summary => summary.WeakCount)
            .ThenBy(summary => summary.AverageRating)
            .ThenBy(summary => summary.Tag)
            .ToList();
    }

    private static IReadOnlyList<RecallGroupAnalytics> BuildRecallCategorySummaries(
        IReadOnlyList<AttemptHistoryRow> rows,
        IReadOnlyList<Attempt> attempts,
        IReadOnlyDictionary<string, AssessmentDefinition> assessments,
        IReadOnlyList<Category> categories)
    {
        var records = RecallRecords(rows, attempts, assessments);
        return records
            .GroupBy(record => record.Assessment.CategoryId, StringComparer.OrdinalIgnoreCase)
            .Select(group =>
            {
                var category = categories.FirstOrDefault(candidate => string.Equals(candidate.Id, group.Key, StringComparison.OrdinalIgnoreCase));
                return new RecallGroupAnalytics(
                    group.Key,
                    category?.Title ?? group.Key,
                    group.Count(),
                    Math.Round(group.Average(record => RatingValue(record.Rating)), 2),
                    group.Count(record => IsWeakRating(record.Rating)));
            })
            .OrderBy(summary => summary.Title)
            .ToList();
    }

    private static IReadOnlyList<RecallGroupAnalytics> BuildRecallSubcategorySummaries(
        IReadOnlyList<AttemptHistoryRow> rows,
        IReadOnlyList<Attempt> attempts,
        IReadOnlyDictionary<string, AssessmentDefinition> assessments,
        IReadOnlyList<Category> categories)
    {
        var records = RecallRecords(rows, attempts, assessments);
        return records
            .SelectMany(record => record.Assessment.SubcategoryIds.Select(subcategoryId => new { record.Assessment, record.Rating, SubcategoryId = subcategoryId }))
            .GroupBy(record => new { record.Assessment.CategoryId, record.SubcategoryId })
            .Select(group =>
            {
                var category = categories.FirstOrDefault(candidate => string.Equals(candidate.Id, group.Key.CategoryId, StringComparison.OrdinalIgnoreCase));
                var title = category?.Subcategories.FirstOrDefault(subcategory => string.Equals(subcategory.Id, group.Key.SubcategoryId, StringComparison.OrdinalIgnoreCase))?.Title ?? group.Key.SubcategoryId;
                return new RecallGroupAnalytics(
                    group.Key.SubcategoryId,
                    title,
                    group.Count(),
                    Math.Round(group.Average(record => RatingValue(record.Rating)), 2),
                    group.Count(record => IsWeakRating(record.Rating)));
            })
            .OrderBy(summary => summary.Title)
            .ToList();
    }

    private static IReadOnlyList<CategoryGradeAnalytics> BuildCategorySummaries(
        IReadOnlyList<GradeLogEntry> entries,
        IReadOnlyDictionary<string, AssessmentDefinition> assessments,
        IReadOnlyList<Category> categories)
    {
        return entries
            .GroupBy(entry => assessments[entry.AssessmentId].CategoryId, StringComparer.OrdinalIgnoreCase)
            .Select(group =>
            {
                var category = categories.FirstOrDefault(candidate => string.Equals(candidate.Id, group.Key, StringComparison.OrdinalIgnoreCase));
                var ordered = group.OrderByDescending(entry => entry.CommittedAt).ToList();
                return new CategoryGradeAnalytics(
                    group.Key,
                    category?.Title ?? group.Key,
                    ordered.Count,
                    ComputeWeightedAverage(ordered, assessments) ?? 0m,
                    ordered.FirstOrDefault()?.PercentScore);
            })
            .OrderBy(summary => summary.CategoryTitle)
            .ToList();
    }

    private static IReadOnlyList<SubcategoryGradeAnalytics> BuildSubcategorySummaries(
        IReadOnlyList<GradeLogEntry> entries,
        IReadOnlyDictionary<string, AssessmentDefinition> assessments,
        IReadOnlyList<Category> categories)
    {
        return entries
            .SelectMany(entry => assessments[entry.AssessmentId].SubcategoryIds.Select(subcategoryId => new { Entry = entry, Assessment = assessments[entry.AssessmentId], SubcategoryId = subcategoryId }))
            .GroupBy(item => new { item.Assessment.CategoryId, item.SubcategoryId })
            .Select(group =>
            {
                var category = categories.FirstOrDefault(candidate => string.Equals(candidate.Id, group.Key.CategoryId, StringComparison.OrdinalIgnoreCase));
                var subcategoryTitle = category?.Subcategories.FirstOrDefault(subcategory => string.Equals(subcategory.Id, group.Key.SubcategoryId, StringComparison.OrdinalIgnoreCase))?.Title ?? group.Key.SubcategoryId;
                var ordered = group.Select(item => item.Entry).OrderByDescending(entry => entry.CommittedAt).ToList();
                return new SubcategoryGradeAnalytics(
                    group.Key.SubcategoryId,
                    subcategoryTitle,
                    group.Key.CategoryId,
                    ordered.Count,
                    ComputeWeightedAverage(ordered, assessments) ?? 0m,
                    ordered.FirstOrDefault()?.PercentScore);
            })
            .OrderBy(summary => summary.SubcategoryTitle)
            .ToList();
    }

    private static IReadOnlyList<AreaGradeAnalytics> BuildAreaSummaries(
        IReadOnlyList<GradeLogEntry> entries,
        IReadOnlyDictionary<string, AssessmentDefinition> assessments,
        IReadOnlyList<Category> categories,
        IReadOnlyList<AreaDefinition> areas)
    {
        var subcategories = BuildSubcategorySummaries(entries, assessments, categories);
        return entries
            .SelectMany(entry => MatchAreas(assessments[entry.AssessmentId], areas).Select(area => new { Entry = entry, Area = area }))
            .GroupBy(item => item.Area.Id, StringComparer.OrdinalIgnoreCase)
            .Select(group =>
            {
                var area = group.First().Area;
                var ordered = group.Select(item => item.Entry).OrderByDescending(entry => entry.CommittedAt).ToList();
                var weakestSubcategory = subcategories
                    .Where(subcategory => area.SubcategoryIds.Contains(subcategory.SubcategoryId, StringComparer.OrdinalIgnoreCase))
                    .OrderBy(subcategory => subcategory.AveragePercent)
                    .FirstOrDefault();

                return new AreaGradeAnalytics(
                    area.Id,
                    area.Title,
                    ordered.Count,
                    ComputeWeightedAverage(ordered, assessments) ?? 0m,
                    weakestSubcategory?.SubcategoryId,
                    weakestSubcategory?.SubcategoryTitle)
                {
                    CategoryIds = area.CategoryIds
                };
            })
            .OrderBy(summary => summary.AreaTitle)
            .ToList();
    }

    private IReadOnlyList<QuestionTypePerformance> BuildQuestionTypeSummaries(
        IReadOnlyList<AttemptHistoryRow> rows,
        IReadOnlyList<Attempt> attempts,
        IReadOnlyDictionary<string, AssessmentDefinition> assessments,
        QuestionType? questionTypeFilter)
    {
        var includedAttemptIds = rows
            .Where(row => row.Status is AttemptStatus.Completed)
            .Select(row => row.AttemptId)
            .ToHashSet(StringComparer.OrdinalIgnoreCase);
        var stats = new Dictionary<QuestionType, (int Answered, int Correct, int NeedsReview)>();

        foreach (var attempt in attempts.Where(attempt => includedAttemptIds.Contains(attempt.Id)))
        {
            var assessment = assessments[attempt.AssessmentId];
            var results = scoringService.BuildResults(assessment, attempt);
            foreach (var question in results.Questions.Where(question => question.SubmittedAnswer is not null))
            {
                if (questionTypeFilter is not null && question.Type != questionTypeFilter)
                {
                    continue;
                }

                var current = stats.TryGetValue(question.Type, out var value) ? value : (Answered: 0, Correct: 0, NeedsReview: 0);
                stats[question.Type] = (
                    current.Answered + 1,
                    current.Correct + (question.IsCorrect == true ? 1 : 0),
                    current.NeedsReview + (question.IsPendingSelfCheck ? 1 : 0));
            }
        }

        return stats
            .Select(pair => new QuestionTypePerformance(
                pair.Key,
                pair.Value.Answered,
                pair.Value.Correct,
                pair.Value.NeedsReview,
                pair.Value.Answered == 0 ? 0 : Math.Round(pair.Value.Correct * 100m / pair.Value.Answered, 2)))
            .OrderBy(summary => summary.QuestionType)
            .ToList();
    }

    private static IReadOnlyList<WeakFocusSummary> BuildWeakFocusSummaries(
        IReadOnlyList<CategoryGradeAnalytics> categories,
        IReadOnlyList<AreaGradeAnalytics> areas)
    {
        return categories.Select(category => new WeakFocusSummary(
                category.CategoryId,
                category.CategoryTitle,
                "category",
                category.AttemptCount,
                category.AveragePercent,
                $"Focus on {category.CategoryTitle}: {category.AveragePercent}% across {category.AttemptCount} committed attempt(s)."))
            .Concat(areas.Select(area => new WeakFocusSummary(
                area.AreaId,
                area.AreaTitle,
                "area",
                area.AttemptCount,
                area.AveragePercent,
                $"Focus on {area.AreaTitle}: {area.AveragePercent}% across {area.AttemptCount} committed attempt(s).")))
            .Where(summary => summary.AttemptCount > 0)
            .OrderBy(summary => summary.AveragePercent)
            .ThenByDescending(summary => summary.AttemptCount)
            .Take(5)
            .ToList();
    }

    private static IEnumerable<AreaDefinition> MatchAreas(AssessmentDefinition assessment, IReadOnlyList<AreaDefinition> areas)
    {
        return areas.Where(area =>
            area.CategoryIds.Contains(assessment.CategoryId, StringComparer.OrdinalIgnoreCase)
            || assessment.SubcategoryIds.Any(subcategoryId => area.SubcategoryIds.Contains(subcategoryId, StringComparer.OrdinalIgnoreCase)));
    }

    private static IReadOnlyList<QuestionType> ExtractQuestionTypes(AssessmentDefinition assessment)
    {
        return assessment.AssessmentType switch
        {
            AssessmentType.WorkedExample => assessment.WorkedExamples
                .SelectMany(example => example.Steps.Select(step => step.Question.Type))
                .Distinct()
                .ToList(),
            AssessmentType.RecallDrill or AssessmentType.Glossary => Array.Empty<QuestionType>(),
            AssessmentType.ConceptLesson => assessment.Lesson is null
                ? Array.Empty<QuestionType>()
                : assessment.Lesson.Sections
                    .Where(section => section.Check is not null)
                    .Select(section => section.Check!.Type)
                    .Distinct()
                    .ToList(),
            AssessmentType.InteractiveExploration => assessment.Exploration is null
                ? Array.Empty<QuestionType>()
                : assessment.Exploration.Sections
                    .Where(section => section.Check is not null)
                    .Select(section => section.Check!.Type)
                    .Distinct()
                    .ToList(),
            _ => assessment.Questions
                .Select(question => question.Type)
                .Distinct()
                .ToList()
        };
    }

    private static IReadOnlyList<Attempt> CompletedRecallAttempts(
        IReadOnlyList<AttemptHistoryRow> rows,
        IReadOnlyList<Attempt> attempts,
        IReadOnlyDictionary<string, AssessmentDefinition> assessments)
    {
        var includedAttemptIds = rows
            .Where(row => row.Status is AttemptStatus.Completed && row.AssessmentType is AssessmentType.RecallDrill)
            .Select(row => row.AttemptId)
            .ToHashSet(StringComparer.OrdinalIgnoreCase);

        return attempts
            .Where(attempt => includedAttemptIds.Contains(attempt.Id)
                && assessments.TryGetValue(attempt.AssessmentId, out var assessment)
                && assessment.AssessmentType is AssessmentType.RecallDrill)
            .ToList();
    }

    private static IReadOnlyList<RecallRecord> RecallRecords(
        IReadOnlyList<AttemptHistoryRow> rows,
        IReadOnlyList<Attempt> attempts,
        IReadOnlyDictionary<string, AssessmentDefinition> assessments)
    {
        return CompletedRecallAttempts(rows, attempts, assessments)
            .SelectMany(attempt =>
            {
                var assessment = assessments[attempt.AssessmentId];
                return attempt.RecallItems
                    .Where(recall => recall.Rating is not RecallRating.Unknown)
                    .Select(recall =>
                    {
                        var item = assessment.Items.FirstOrDefault(candidate => string.Equals(candidate.Id, recall.ItemId, StringComparison.OrdinalIgnoreCase));
                        return item is null ? null : new RecallRecord(assessment, item, recall.Rating);
                    })
                    .OfType<RecallRecord>();
            })
            .ToList();
    }

    private static decimal RatingValue(RecallRating rating)
    {
        return rating switch
        {
            RecallRating.Easy => 4,
            RecallRating.Correct => 3,
            RecallRating.NeedsReview => 2,
            RecallRating.ForgotCompletely => 1,
            _ => 0
        };
    }

    private static bool IsWeakRating(RecallRating rating)
    {
        return rating is RecallRating.NeedsReview or RecallRating.ForgotCompletely;
    }

    private sealed record RecallRecord(
        AssessmentDefinition Assessment,
        RecallItemDefinition Item,
        RecallRating Rating);

    private static bool MatchesFilter(AttemptHistoryRow row, GradeAnalyticsFilter filter)
    {
        if (filter.Status is not null && row.Status != filter.Status) return false;
        if (filter.Mode is not null && row.Mode != filter.Mode) return false;
        if (filter.AssessmentType is not null && row.AssessmentType != filter.AssessmentType) return false;
        if (!string.IsNullOrWhiteSpace(filter.CategoryId) && !string.Equals(row.CategoryId, filter.CategoryId, StringComparison.OrdinalIgnoreCase)) return false;
        if (!string.IsNullOrWhiteSpace(filter.SubcategoryId) && !row.SubcategoryIds.Contains(filter.SubcategoryId, StringComparer.OrdinalIgnoreCase)) return false;
        if (!string.IsNullOrWhiteSpace(filter.AreaId) && !row.AreaIds.Contains(filter.AreaId, StringComparer.OrdinalIgnoreCase)) return false;
        if (filter.Committed is not null && row.IsCommitted != filter.Committed) return false;
        if (filter.From is not null && (row.LastActivityAt ?? row.StartedAt) < filter.From) return false;
        if (filter.To is not null && (row.LastActivityAt ?? row.StartedAt) > filter.To) return false;
        if (filter.MinScore is not null && row.PercentScore < filter.MinScore) return false;
        if (filter.MaxScore is not null && row.PercentScore > filter.MaxScore) return false;

        return true;
    }

    private IReadOnlyList<SkillPerformance> BuildSkillPerformanceSummaries(
        IReadOnlyList<AttemptHistoryRow> rows,
        IReadOnlyList<Attempt> attempts,
        IReadOnlyDictionary<string, AssessmentDefinition> assessments)
    {
        var includedAttemptIds = rows
            .Where(row => row.Status is AttemptStatus.Completed)
            .Select(row => row.AttemptId)
            .ToHashSet(StringComparer.OrdinalIgnoreCase);
        var stats = new Dictionary<string, (int Answered, int Correct)>(StringComparer.OrdinalIgnoreCase);

        foreach (var attempt in attempts.Where(attempt => includedAttemptIds.Contains(attempt.Id)))
        {
            if (!assessments.TryGetValue(attempt.AssessmentId, out var assessment)) continue;
            
            var questionSkills = new Dictionary<string, IReadOnlyList<string>>(StringComparer.OrdinalIgnoreCase);
            
            foreach (var q in assessment.Questions)
                questionSkills[q.Id] = q.Skills;
            foreach (var we in assessment.WorkedExamples)
                foreach (var step in we.Steps)
                    questionSkills[step.Id] = step.Question.Skills;
            if (assessment.Lesson != null)
                foreach (var sec in assessment.Lesson.Sections.Where(s => s.Check != null))
                    questionSkills[sec.Check!.Id] = sec.Check.Skills;
            if (assessment.Exploration != null)
                foreach (var sec in assessment.Exploration.Sections.Where(s => s.Check != null))
                    questionSkills[sec.Check!.Id] = sec.Check.Skills;
            
            var results = scoringService.BuildResults(assessment, attempt);
            foreach (var question in results.Questions.Where(q => q.SubmittedAnswer is not null))
            {
                if (!questionSkills.TryGetValue(question.QuestionId, out var skills)) continue;
                
                foreach (var skill in skills)
                {
                    var current = stats.TryGetValue(skill, out var value) ? value : (Answered: 0, Correct: 0);
                    stats[skill] = (
                        current.Answered + 1,
                        current.Correct + (question.IsCorrect == true ? 1 : 0));
                }
            }
        }

        return stats
            .Select(pair => new SkillPerformance(
                pair.Key,
                pair.Value.Answered,
                pair.Value.Correct,
                pair.Value.Answered == 0 ? 0 : Math.Round(pair.Value.Correct * 100m / pair.Value.Answered, 2)))
            .OrderBy(summary => summary.CorrectPercent)
            .ThenByDescending(summary => summary.AnsweredCount)
            .ToList();
    }

    private static decimal? ComputeWeightedAverage(IEnumerable<GradeLogEntry> entries, IReadOnlyDictionary<string, AssessmentDefinition> assessments)
    {
        var validEntries = entries.Where(e => assessments.ContainsKey(e.AssessmentId)).ToList();
        if (validEntries.Count == 0) return null;

        var totalWeight = validEntries.Sum(e => GradeContributionPolicy.WeightFor(assessments[e.AssessmentId].AssessmentType) * Math.Max(1m, e.PossiblePoints));
        if (totalWeight == 0m) return null;

        var totalScore = validEntries.Sum(e => e.PercentScore * GradeContributionPolicy.WeightFor(assessments[e.AssessmentId].AssessmentType) * Math.Max(1m, e.PossiblePoints));
        return Math.Round(totalScore / totalWeight, 2);
    }

    private static IReadOnlyList<ActionableNextStep> BuildActionableNextSteps(
        IReadOnlyList<SkillPerformance> skills,
        IReadOnlyList<RecallTagAnalytics> recallTags,
        NavigationCatalog catalog,
        IReadOnlyDictionary<string, AssessmentDefinition> assessments,
        IReadOnlyList<Category> categories,
        IReadOnlyList<AreaDefinition> areas)
    {
        var steps = new List<ActionableNextStep>();
        foreach (var weakSkill in skills.Where(s => s.CorrectPercent < 80))
        {
            var targetActivity = weakSkill.CorrectPercent < 60 ? "conceptLesson" : "guidedWorkedExample";
            
            var assessment = catalog.Assessments
                .FirstOrDefault(a => string.Equals(a.ActivityType, targetActivity, StringComparison.OrdinalIgnoreCase)
                    && a.Skills.Contains(weakSkill.SkillId, StringComparer.OrdinalIgnoreCase));
            
            assessment ??= catalog.Assessments
                .FirstOrDefault(a => a.Skills.Contains(weakSkill.SkillId, StringComparer.OrdinalIgnoreCase));
            
            if (assessment is not null)
            {
                var message = weakSkill.CorrectPercent < 60 
                    ? $"Review the fundamental concepts for {weakSkill.SkillId}." 
                    : $"Practice more examples for {weakSkill.SkillId}.";

                assessments.TryGetValue(assessment.Id, out var def);
                var categoryId = def?.CategoryId ?? assessment.SubjectId;
                var category = categories.FirstOrDefault(candidate => string.Equals(candidate.Id, categoryId, StringComparison.OrdinalIgnoreCase));
                var matchingAreas = def is not null ? MatchAreas(def, areas).ToList() : new List<AreaDefinition>();
                var matchingTopics = catalog.Topics.Where(t => assessment.TopicIds.Contains(t.Id, StringComparer.OrdinalIgnoreCase)).ToList();

                steps.Add(new ActionableNextStep(
                    weakSkill.SkillId,
                    message,
                    assessment.Id,
                    assessment.Title)
                {
                    CategoryId = categoryId,
                    CategoryTitle = category?.Title ?? categoryId,
                    AreaIds = matchingAreas.Select(a => a.Id).ToList(),
                    AreaTitles = matchingAreas.Select(a => a.Title).ToList(),
                    TopicIds = matchingTopics.Select(t => t.Id).ToList(),
                    TopicTitles = matchingTopics.Select(t => t.Title).ToList(),
                    Source = "skill",
                    EvidencePercent = weakSkill.CorrectPercent
                });
            }
        }

        foreach (var weakTag in recallTags.Where(t => t.AverageRating < 3.0m))
        {
            var assessment = catalog.Assessments
                .FirstOrDefault(a => string.Equals(a.ActivityType, "conceptLesson", StringComparison.OrdinalIgnoreCase)
                    && a.Tags.Contains(weakTag.Tag, StringComparer.OrdinalIgnoreCase));
            
            assessment ??= catalog.Assessments
                .FirstOrDefault(a => a.Tags.Contains(weakTag.Tag, StringComparer.OrdinalIgnoreCase));
            
            if (assessment is not null)
            {
                var message = $"Review the fundamental concepts for {weakTag.Tag}.";

                assessments.TryGetValue(assessment.Id, out var def);
                var categoryId = def?.CategoryId ?? assessment.SubjectId;
                var category = categories.FirstOrDefault(candidate => string.Equals(candidate.Id, categoryId, StringComparison.OrdinalIgnoreCase));
                var matchingAreas = def is not null ? MatchAreas(def, areas).ToList() : new List<AreaDefinition>();
                var matchingTopics = catalog.Topics.Where(t => assessment.TopicIds.Contains(t.Id, StringComparer.OrdinalIgnoreCase)).ToList();

                steps.Add(new ActionableNextStep(
                    weakTag.Tag,
                    message,
                    assessment.Id,
                    assessment.Title)
                {
                    CategoryId = categoryId,
                    CategoryTitle = category?.Title ?? categoryId,
                    AreaIds = matchingAreas.Select(a => a.Id).ToList(),
                    AreaTitles = matchingAreas.Select(a => a.Title).ToList(),
                    TopicIds = matchingTopics.Select(t => t.Id).ToList(),
                    TopicTitles = matchingTopics.Select(t => t.Title).ToList(),
                    Source = "recall",
                    EvidencePercent = Math.Round(weakTag.AverageRating * 25m, 2)
                });
            }
        }

        return steps;
    }
}
