using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;
using QuizApp.Core.Services;
using System.Text.Json;

namespace QuizApp.Tests;

public sealed class AttemptFlowTests
{
    [Fact]
    public async Task StartAsync_saves_the_question_order_on_the_attempt()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.MultipleChoiceQuestion("q001"),
            TestData.MultipleChoiceQuestion("q002"),
            TestData.MultipleChoiceQuestion("q003")
        });
        var attempts = new InMemoryAttemptRepository();
        var sessions = new InMemoryAttemptSessionStore();
        var service = CreateAttemptService(assessment, attempts, sessions);

        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);
        var savedAttempt = await sessions.GetByIdAsync(attempt.Id);

        Assert.NotNull(savedAttempt);
        Assert.Equal(AttemptStatus.InProgress, savedAttempt.Status);
        Assert.Equal(attempt.QuestionOrder, savedAttempt.QuestionOrder);
        Assert.Equal(assessment.Questions.Count, savedAttempt.QuestionOrder.Count);
        Assert.Null(await attempts.GetByIdAsync(attempt.Id));
    }

    [Fact]
    public async Task StartAsync_samples_attempt_question_count_and_results_use_sample()
    {
        var assessment = TestData.Assessment(AssessmentType.Test, Enumerable.Range(1, 15)
            .Select(index => TestData.MultipleChoiceQuestion($"q{index:000}"))
            .ToList()) with
        {
            AttemptQuestionCount = 12
        };
        var service = CreateAttemptService(assessment);

        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);
        var results = await service.GetResultsAsync(attempt.Id);

        Assert.Equal(12, attempt.QuestionOrder.Count);
        Assert.Equal(12, attempt.QuestionOrder.Distinct(StringComparer.OrdinalIgnoreCase).Count());
        Assert.All(attempt.QuestionOrder, questionId => Assert.Contains(assessment.Questions, question => question.Id == questionId));
        Assert.Equal(12, results.TotalQuestions);
        Assert.Equal(attempt.QuestionOrder, results.Questions.Select(question => question.QuestionId));
    }

    [Fact]
    public async Task StartAsync_selects_one_ordered_variant_per_slot()
    {
        var assessment = TestData.Assessment(AssessmentType.Test, new[]
        {
            TestData.MultipleChoiceQuestion("q001a"),
            TestData.MultipleChoiceQuestion("q001b"),
            TestData.MultipleChoiceQuestion("q002a"),
            TestData.MultipleChoiceQuestion("q002b"),
            TestData.MultipleChoiceQuestion("q003a")
        }) with
        {
            RandomizeQuestions = true,
            AttemptQuestionCount = 3,
            QuestionSelection = new QuestionSelectionDefinition(
                QuestionSelectionMode.OrderedVariants,
                new[]
                {
                    new QuestionSelectionSlotDefinition("slot-001", "First slot", new[] { "q001a", "q001b" }),
                    new QuestionSelectionSlotDefinition("slot-002", "Second slot", new[] { "q002a", "q002b" }),
                    new QuestionSelectionSlotDefinition("slot-003", "Third slot", new[] { "q003a" })
                })
        };
        var service = CreateAttemptService(assessment);

        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);
        var results = await service.GetResultsAsync(attempt.Id);

        Assert.Equal(3, attempt.QuestionOrder.Count);
        Assert.Contains(attempt.QuestionOrder[0], new[] { "q001a", "q001b" });
        Assert.Contains(attempt.QuestionOrder[1], new[] { "q002a", "q002b" });
        Assert.Equal("q003a", attempt.QuestionOrder[2]);
        Assert.Equal(attempt.QuestionOrder, results.Questions.Select(question => question.QuestionId));
    }

    [Fact]
    public async Task PauseAsync_persists_attempt_and_removes_active_session()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.MultipleChoiceQuestion("q001") });
        var attempts = new InMemoryAttemptRepository();
        var sessions = new InMemoryAttemptSessionStore();
        var service = CreateAttemptService(assessment, attempts, sessions);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.PauseAsync(attempt.Id);

        Assert.Null(await sessions.GetByIdAsync(attempt.Id));
        var persisted = await attempts.GetByIdAsync(attempt.Id);
        Assert.NotNull(persisted);
        Assert.Equal(AttemptStatus.Paused, persisted.Status);
    }

    [Fact]
    public async Task CompleteAsync_persists_attempt_and_removes_active_session()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.MultipleChoiceQuestion("q001") });
        var attempts = new InMemoryAttemptRepository();
        var sessions = new InMemoryAttemptSessionStore();
        var service = CreateAttemptService(assessment, attempts, sessions);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("q001", "a", Array.Empty<string>(), null, null, null));
        await service.CompleteAsync(attempt.Id);

        Assert.Null(await sessions.GetByIdAsync(attempt.Id));
        var persisted = await attempts.GetByIdAsync(attempt.Id);
        Assert.NotNull(persisted);
        Assert.Equal(AttemptStatus.Completed, persisted.Status);
    }

    [Fact]
    public async Task PauseAsync_marks_attempt_paused_without_losing_answers()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.MultipleChoiceQuestion("q001") });
        var attempts = new InMemoryAttemptRepository();
        var service = CreateAttemptService(assessment, attempts);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("q001", "a", Array.Empty<string>(), null, null, null));
        var paused = await service.PauseAsync(attempt.Id);

        Assert.Equal(AttemptStatus.Paused, paused.Status);
        Assert.NotNull(paused.PausedAt);
        Assert.Single(paused.Answers);
    }

    [Fact]
    public async Task ResumeAsync_marks_paused_attempt_in_progress_and_preserves_order()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.MultipleChoiceQuestion("q001"),
            TestData.MultipleChoiceQuestion("q002")
        });
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);
        var originalOrder = attempt.QuestionOrder.ToList();

        await service.PauseAsync(attempt.Id);
        var resumed = await service.ResumeAsync(attempt.Id);

        Assert.Equal(AttemptStatus.InProgress, resumed.Status);
        Assert.Equal(originalOrder, resumed.QuestionOrder);
    }

    [Fact]
    public async Task ResumeAsync_keeps_previous_durable_checkpoint_until_next_explicit_save()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.MultipleChoiceQuestion("q001"),
            TestData.MultipleChoiceQuestion("q002")
        });
        var attempts = new InMemoryAttemptRepository();
        var sessions = new InMemoryAttemptSessionStore();
        var service = CreateAttemptService(assessment, attempts, sessions);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("q001", "a", Array.Empty<string>(), null, null, null));
        await service.PauseAsync(attempt.Id);
        await service.ResumeAsync(attempt.Id);
        await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("q002", "a", Array.Empty<string>(), null, null, null));

        var checkpoint = await attempts.GetByIdAsync(attempt.Id);
        var active = await sessions.GetByIdAsync(attempt.Id);

        Assert.NotNull(checkpoint);
        Assert.Equal(AttemptStatus.Paused, checkpoint.Status);
        Assert.Single(checkpoint.Answers);
        Assert.NotNull(active);
        Assert.Equal(AttemptStatus.InProgress, active.Status);
        Assert.Equal(2, active.Answers.Count);
    }

    [Fact]
    public async Task AbandonAsync_rejects_future_answers_and_grade_commit()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.MultipleChoiceQuestion("q001") });
        var attemptService = CreateAttemptService(assessment);
        var gradeService = new GradeLogService(new InMemoryGradeLogRepository(), attemptService);
        var attempt = await attemptService.StartAsync(assessment.Id, AssessmentMode.Practice);

        var abandoned = await attemptService.AbandonAsync(attempt.Id);

        Assert.Equal(AttemptStatus.Abandoned, abandoned.Status);
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            attemptService.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("q001", "a", Array.Empty<string>(), null, null, null)));
        await Assert.ThrowsAsync<InvalidOperationException>(() => gradeService.CommitAttemptAsync(attempt.Id));
    }

    [Fact]
    public async Task DeleteAsync_removes_attempt_and_linked_grade_entry()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.MultipleChoiceQuestion("q001") });
        var attempts = new InMemoryAttemptRepository();
        var grades = new InMemoryGradeLogRepository();
        var attemptService = CreateAttemptService(assessment, attempts, grades: grades);
        var gradeService = new GradeLogService(grades, attemptService);
        var attempt = await attemptService.StartAsync(assessment.Id, AssessmentMode.Scored);

        await attemptService.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("q001", "a", Array.Empty<string>(), null, null, null));
        await attemptService.CompleteAsync(attempt.Id);
        await gradeService.CommitAttemptAsync(attempt.Id);

        await attemptService.DeleteAsync(attempt.Id);

        Assert.Null(await attempts.GetByIdAsync(attempt.Id));
        Assert.Empty((await grades.ListAsync()).Where(entry => entry.AttemptId == attempt.Id));
    }

    [Fact]
    public async Task Free_response_self_check_scores_and_shows_feedback_in_practice_mode()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.FreeResponseQuestion("q001") });
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(
            attempt.Id,
            new SubmittedAnswer("q001", null, Array.Empty<string>(), "It sums upper minus lower.", true, null));

        var results = await service.GetResultsAsync(attempt.Id);

        Assert.False(results.IsComplete);
        Assert.Equal(1, results.CorrectCount);
        Assert.True(results.Questions.Single().IsCorrect);
        Assert.NotNull(results.Questions.Single().Explanation);
    }

    [Fact]
    public async Task Free_response_text_submission_remains_pending_until_self_check()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.FreeResponseQuestion("q001") });
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(
            attempt.Id,
            new SubmittedAnswer("q001", null, Array.Empty<string>(), "It sums upper minus lower.", null, null));

        var results = await service.GetResultsAsync(attempt.Id);

        var result = Assert.Single(results.Questions);
        Assert.True(result.IsPendingSelfCheck);
        Assert.True(results.HasPendingSelfChecks);
        Assert.False(result.IsCorrect);
        Assert.Equal(0, results.CorrectCount);
        Assert.Equal(new[] { "Mention the accumulated difference.", "Identify upper minus lower." }, result.KeyPoints);
    }

    [Fact]
    public async Task Free_response_self_check_update_preserves_locked_text_and_recalculates_results()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.FreeResponseQuestion("q001") });
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(
            attempt.Id,
            new SubmittedAnswer("q001", null, Array.Empty<string>(), "Original response.", null, null));
        await service.SubmitAnswerAsync(
            attempt.Id,
            new SubmittedAnswer("q001", null, Array.Empty<string>(), "Edited after lock.", true, null));

        var results = await service.GetResultsAsync(attempt.Id);

        var result = Assert.Single(results.Questions);
        Assert.False(results.HasPendingSelfChecks);
        Assert.True(result.IsCorrect);
        Assert.Equal("Original response.", result.SubmittedAnswer?.FreeResponseText);
    }

    [Fact]
    public async Task Completed_scored_attempt_allows_free_response_self_check_review()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.FreeResponseQuestion("q001") });
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Scored);

        await service.SubmitAnswerAsync(
            attempt.Id,
            new SubmittedAnswer("q001", null, Array.Empty<string>(), "It sums upper minus lower.", null, null));
        await service.CompleteAsync(attempt.Id);
        await service.SubmitAnswerAsync(
            attempt.Id,
            new SubmittedAnswer("q001", null, Array.Empty<string>(), null, true, null));

        var results = await service.GetResultsAsync(attempt.Id);

        Assert.False(results.HasPendingSelfChecks);
        Assert.Equal(1, results.CorrectCount);
        Assert.True(results.Questions.Single().IsCorrect);
    }

    [Fact]
    public async Task Grade_log_commit_rejects_pending_free_response_self_check()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.FreeResponseQuestion("q001") });
        var attemptService = CreateAttemptService(assessment);
        var gradeService = new GradeLogService(new InMemoryGradeLogRepository(), attemptService);
        var attempt = await attemptService.StartAsync(assessment.Id, AssessmentMode.Scored);

        await attemptService.SubmitAnswerAsync(
            attempt.Id,
            new SubmittedAnswer("q001", null, Array.Empty<string>(), "It sums upper minus lower.", null, null));
        await attemptService.CompleteAsync(attempt.Id);

        await Assert.ThrowsAsync<InvalidOperationException>(() => gradeService.CommitAttemptAsync(attempt.Id));
    }

    [Fact]
    public async Task Scored_attempt_shows_expected_answers_for_review_once_all_questions_are_answered()
    {
        var assessment = TestData.Assessment(AssessmentType.Test, new[]
        {
            TestData.MultipleChoiceQuestion("q001"),
            TestData.FreeResponseQuestion("q002")
        });
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Scored);

        await service.SubmitAnswerAsync(
            attempt.Id,
            new SubmittedAnswer("q001", "a", Array.Empty<string>(), null, null, null));

        var partialResults = await service.GetResultsAsync(attempt.Id);
        Assert.Null(partialResults.Questions.Single(question => question.QuestionId == "q002").ExpectedAnswer);

        await service.SubmitAnswerAsync(
            attempt.Id,
            new SubmittedAnswer("q002", null, Array.Empty<string>(), "", null, null));

        var reviewResults = await service.GetResultsAsync(attempt.Id);
        var freeResponseResult = reviewResults.Questions.Single(question => question.QuestionId == "q002");

        Assert.Equal(AttemptStatus.InProgress, reviewResults.Status);
        Assert.False(string.IsNullOrWhiteSpace(freeResponseResult.ExpectedAnswer));
        Assert.NotEmpty(freeResponseResult.KeyPoints);
        Assert.True(freeResponseResult.IsPendingSelfCheck);
    }

    [Fact]
    public async Task Symbolic_response_scores_and_shows_feedback_in_practice_mode()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.SymbolicResponseQuestion("q001") });
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(
            attempt.Id,
            new SubmittedAnswer("q001", null, Array.Empty<string>(), null, null, null)
            {
                SymbolicLatex = "x^2+2x+1"
            });

        var results = await service.GetResultsAsync(attempt.Id);

        Assert.True(results.Questions.Single().IsCorrect);
        Assert.NotNull(results.Questions.Single().SymbolicFeedback);
    }


    [Fact]
    public async Task Grade_log_commit_records_completed_attempt_once()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.MultipleChoiceQuestion("q001") });
        var attemptService = CreateAttemptService(assessment);
        var gradeRepository = new InMemoryGradeLogRepository();
        var gradeService = new GradeLogService(gradeRepository, attemptService);
        var attempt = await attemptService.StartAsync(assessment.Id, AssessmentMode.Scored);

        await attemptService.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("q001", "a", Array.Empty<string>(), null, null, null));
        await attemptService.CompleteAsync(attempt.Id);

        var firstCommit = await gradeService.CommitAttemptAsync(attempt.Id);
        var secondCommit = await gradeService.CommitAttemptAsync(attempt.Id);
        var summary = await gradeService.GetSummaryAsync();

        Assert.Equal(firstCommit.Id, secondCommit.Id);
        Assert.Equal(1, summary.EntryCount);
        Assert.Equal(100m, summary.AveragePercentScore);
    }

    [Fact]
    public async Task ListResultsAsync_returns_saved_attempt_results()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.MultipleChoiceQuestion("q001") });
        var attempts = new InMemoryAttemptRepository();
        var service = CreateAttemptService(assessment, attempts);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("q001", "a", Array.Empty<string>(), null, null, null));

        var results = await service.ListResultsAsync();

        Assert.Contains(results, result => result.AttemptId == attempt.Id && result.PercentScore == 100m);
    }

    [Fact]
    public async Task Worked_example_start_uses_authored_step_order()
    {
        var assessment = TestData.WorkedExampleAssessment();
        var service = CreateAttemptService(assessment);

        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Scored);

        Assert.Equal(AssessmentMode.Practice, attempt.Mode);
        Assert.Equal(new[] { "s001", "s002" }, attempt.QuestionOrder);
    }

    [Fact]
    public async Task Worked_example_wrong_answer_keeps_current_step()
    {
        var assessment = TestData.WorkedExampleAssessment();
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("s001", "yes", Array.Empty<string>(), null, null, null));

        var results = await service.GetResultsAsync(attempt.Id);
        Assert.False(results.IsComplete);
        Assert.False(results.Questions.First().IsCorrect);
        Assert.Equal("Try checking whether an inner expression has a constant derivative.", results.Questions.First().Hint);
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("s002", null, Array.Empty<string>(), "u = 3x + 1", true, null)));
    }

    [Fact]
    public async Task Worked_example_auto_graded_steps_retry_with_hint_until_correct()
    {
        var assessment = TestData.WorkedExampleAssessment() with
        {
            WorkedExamples = new[]
            {
                new WorkedExampleDefinition(
                    "we001", "Auto-graded chemistry flow", "Solve each conversion.", new[]
                    {
                        new WorkedExampleStepDefinition("numeric", "Numeric conversion", "Convert the quantity.", "Use the stated conversion factor.", TestData.NumericResponseQuestion("numeric")),
                        new WorkedExampleStepDefinition("symbolic", "Symbolic relationship", "Enter the relationship.", "Use equivalent algebraic notation.", TestData.SymbolicResponseQuestion("symbolic")),
                        new WorkedExampleStepDefinition("choice", "Chemical decision", "Choose the limiting reactant.", "Compare product amounts.", TestData.MultipleChoiceQuestion("choice"))
                    })
            }
        };
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("numeric", null, Array.Empty<string>(), null, null, 4m));
        var afterWrong = await service.GetResultsAsync(attempt.Id);

        Assert.False(afterWrong.Questions[0].IsCorrect);
        Assert.Equal("Use the stated conversion factor.", afterWrong.Questions[0].Hint);
        Assert.False(afterWrong.IsComplete);
        await Assert.ThrowsAsync<InvalidOperationException>(() => service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("symbolic", null, Array.Empty<string>(), null, null, null)));

        await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("numeric", null, Array.Empty<string>(), null, null, 8.38m));
        await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("symbolic", null, Array.Empty<string>(), null, null, null) { SymbolicLatex = "(x+1)^2" });
        var completed = await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("choice", "a", Array.Empty<string>(), null, null, null));

        Assert.Equal(AttemptStatus.Completed, completed.Status);
    }

    [Fact]
    public async Task Worked_example_free_response_rejects_blank_submission()
    {
        var assessment = TestData.WorkedExampleAssessment();
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("s001", "no", Array.Empty<string>(), null, null, null));

        var exception = await Assert.ThrowsAsync<InvalidOperationException>(() =>
            service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("s002", null, Array.Empty<string>(), "   ", null, null)));

        Assert.Equal("Worked example free-response steps require a response before continuing.", exception.Message);
    }

    [Fact]
    public async Task Worked_example_correct_answers_unlock_and_complete()
    {
        var assessment = TestData.WorkedExampleAssessment();
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("s001", "no", Array.Empty<string>(), null, null, null));
        var afterFirstStep = await service.GetResultsAsync(attempt.Id);
        Assert.False(afterFirstStep.IsComplete);

        var completed = await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("s002", null, Array.Empty<string>(), "u = 3x + 1", true, null));
        var results = await service.GetResultsAsync(attempt.Id);

        Assert.Equal(AttemptStatus.Completed, completed.Status);
        Assert.True(results.IsComplete);
        Assert.Equal(2, results.CorrectCount);
        Assert.Equal(AssessmentType.WorkedExample, results.AssessmentType);
        Assert.Equal("Define the substitution", results.Questions[1].Title);
    }

    [Fact]
    public async Task Worked_example_cannot_be_committed_to_grade_log()
    {
        var assessment = TestData.WorkedExampleAssessment();
        var attemptService = CreateAttemptService(assessment);
        var gradeService = new GradeLogService(new InMemoryGradeLogRepository(), attemptService);
        var attempt = await attemptService.StartAsync(assessment.Id, AssessmentMode.Practice);

        await attemptService.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("s001", "no", Array.Empty<string>(), null, null, null));
        await attemptService.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("s002", null, Array.Empty<string>(), "u = 3x + 1", true, null));

        await Assert.ThrowsAsync<InvalidOperationException>(() => gradeService.CommitAttemptAsync(attempt.Id));
    }

    [Fact]
    public async Task Recall_drill_reveal_and_rating_tracks_summary_and_completes()
    {
        var assessment = TestData.RecallDrillAssessment();
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Scored);

        Assert.Equal(AssessmentMode.Practice, attempt.Mode);
        Assert.Equal(new[] { "typed-1", "symbolic-1", "flashcard-1", "cloze-1" }, attempt.QuestionOrder);

        await service.RevealRecallItemAsync(attempt.Id, "typed-1", "A variable stores a value.");
        await service.RateRecallItemAsync(attempt.Id, "typed-1", RecallRating.Correct);
        await service.RevealRecallItemAsync(attempt.Id, "symbolic-1", "\\sin^2(x)+\\cos^2(x)=1");
        await service.RateRecallItemAsync(attempt.Id, "symbolic-1", RecallRating.Easy);
        await service.RevealRecallItemAsync(attempt.Id, "flashcard-1", null);
        await service.RateRecallItemAsync(attempt.Id, "flashcard-1", RecallRating.NeedsReview);
        await service.RevealRecallItemAsync(attempt.Id, "cloze-1", "cos^2(x)");
        var completed = await service.RateRecallItemAsync(attempt.Id, "cloze-1", RecallRating.ForgotCompletely);

        var results = await service.GetResultsAsync(attempt.Id);

        Assert.Equal(AttemptStatus.Completed, completed.Status);
        Assert.True(results.IsComplete);
        Assert.Equal(AssessmentType.RecallDrill, results.AssessmentType);
        Assert.Equal(4, results.RecallSummary?.ItemsReviewed);
        Assert.Equal(1, results.RecallSummary?.EasyCount);
        Assert.Equal(1, results.RecallSummary?.CorrectCount);
        Assert.Equal(1, results.RecallSummary?.NeedsReviewCount);
        Assert.Equal(1, results.RecallSummary?.ForgotCompletelyCount);
        Assert.Contains("trig", results.RecallSummary!.WeakTags);
    }

    [Fact]
    public async Task Recall_drill_requires_reveal_and_all_ratings_before_grade_commit()
    {
        var assessment = TestData.RecallDrillAssessment();
        var attemptService = CreateAttemptService(assessment);
        var gradeRepository = new InMemoryGradeLogRepository();
        var gradeService = new GradeLogService(gradeRepository, attemptService);
        var attempt = await attemptService.StartAsync(assessment.Id, AssessmentMode.Practice);

        await Assert.ThrowsAsync<InvalidOperationException>(() => gradeService.CommitAttemptAsync(attempt.Id));
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            attemptService.RateRecallItemAsync(attempt.Id, "typed-1", RecallRating.Correct));

        foreach (var itemId in attempt.QuestionOrder)
        {
            await attemptService.RevealRecallItemAsync(attempt.Id, itemId, "response");
            await attemptService.RateRecallItemAsync(attempt.Id, itemId, RecallRating.Correct);
        }

        var committed = await gradeService.CommitAttemptAsync(attempt.Id);
        var summary = await gradeService.GetSummaryAsync();

        Assert.Equal(attempt.Id, committed.AttemptId);
        Assert.Equal(assessment.Id, committed.AssessmentId);
        Assert.Equal(3.4m, committed.EarnedPoints);
        Assert.Equal(4m, committed.PossiblePoints);
        Assert.Equal(85m, committed.PercentScore);
        Assert.Single(summary.Entries);
    }

    [Fact]
    public async Task Glossary_requires_study_before_recall_and_never_commits_to_grade_log()
    {
        var assessment = TestData.GlossaryAssessment();
        var attemptService = CreateAttemptService(assessment);
        var gradeService = new GradeLogService(new InMemoryGradeLogRepository(), attemptService);
        var attempt = await attemptService.StartAsync(assessment.Id, AssessmentMode.Scored);

        Assert.Equal(AssessmentMode.Practice, attempt.Mode);
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            attemptService.RevealRecallItemAsync(attempt.Id, "acute-recall", "Acute angle"));

        await attemptService.CompleteLearningSectionAsync(attempt.Id, "classifications");
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            attemptService.RevealRecallItemAsync(attempt.Id, "acute-recall", "Acute angle"));
        var studied = await attemptService.CompleteLearningSectionAsync(attempt.Id, "relationships");

        Assert.Equal(AttemptStatus.InProgress, studied.Status);
        await attemptService.RevealRecallItemAsync(attempt.Id, "acute-recall", "Acute angle");
        await attemptService.RateRecallItemAsync(attempt.Id, "acute-recall", RecallRating.Correct);
        await attemptService.RevealRecallItemAsync(attempt.Id, "vertical-recognition", "Vertical angles");
        var completed = await attemptService.RateRecallItemAsync(attempt.Id, "vertical-recognition", RecallRating.Easy);
        var results = await attemptService.GetResultsAsync(attempt.Id);

        Assert.Equal(AttemptStatus.Completed, completed.Status);
        Assert.Equal(AssessmentType.Glossary, results.AssessmentType);
        Assert.All(results.LearningSections, section => Assert.True(section.Completed));
        Assert.Equal(2, results.RecallSummary?.ItemsReviewed);
        await Assert.ThrowsAsync<InvalidOperationException>(() => gradeService.CommitAttemptAsync(attempt.Id));
    }

    [Fact]
    public async Task DirectedProject_start_and_track_steps()
    {
        var assessment = TestData.DirectedProjectAssessment();
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        Assert.Equal(AssessmentMode.Practice, attempt.Mode);
        Assert.Equal(AttemptStatus.InProgress, attempt.Status);

        var step1 = await service.UpdateDirectedProjectStepStateAsync(
            attempt.Id,
            "step-1",
            visited: true,
            completed: true,
            completedChecklistItemIds: new[] { "chk-1" },
            notes: "Installed successfully."
        );

        Assert.Equal(AttemptStatus.InProgress, step1.Status);
        
        var results = await service.GetResultsAsync(attempt.Id);
        Assert.False(results.IsComplete);
        Assert.Single(results.DirectedProjectSteps);
        
        var res = results.DirectedProjectSteps[0];
        Assert.Equal("step-1", res.StepId);
        Assert.True(res.Completed);
        Assert.Contains("chk-1", res.CompletedChecklistItemIds);
        Assert.Equal("Installed successfully.", res.Notes);

        var completed = await service.CompleteAsync(attempt.Id);
        Assert.Equal(AttemptStatus.Completed, completed.Status);
    }

    [Fact]
    public async Task ConceptLesson_enforces_ordered_checks_and_rejects_grade_commit()
    {
        var assessment = TestData.ConceptLessonAssessment();
        var attemptService = CreateAttemptService(assessment);
        var gradeService = new GradeLogService(new InMemoryGradeLogRepository(), attemptService);
        var attempt = await attemptService.StartAsync(assessment.Id, AssessmentMode.Scored);

        Assert.Equal(AssessmentMode.Practice, attempt.Mode);
        Assert.Equal(new[] { "intro", "check-loop" }, attempt.QuestionOrder);
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            attemptService.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("check-loop-question", "a", Array.Empty<string>(), null, null, null)));

        await attemptService.CompleteLearningSectionAsync(attempt.Id, "intro");
        await attemptService.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("check-loop-question", "b", Array.Empty<string>(), null, null, null));
        await Assert.ThrowsAsync<InvalidOperationException>(() =>
            attemptService.CompleteLearningSectionAsync(attempt.Id, "check-loop"));

        await attemptService.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("check-loop-question", "a", Array.Empty<string>(), null, null, null));
        var completed = await attemptService.CompleteLearningSectionAsync(attempt.Id, "check-loop");
        var results = await attemptService.GetResultsAsync(attempt.Id);

        Assert.Equal(AttemptStatus.Completed, completed.Status);
        Assert.All(results.LearningSections, section => Assert.True(section.Completed));
        await Assert.ThrowsAsync<InvalidOperationException>(() => gradeService.CommitAttemptAsync(attempt.Id));
    }

    [Fact]
    public async Task InteractiveExploration_state_survives_pause_and_resume()
    {
        var assessment = TestData.InteractiveExplorationAssessment();
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);
        var values = new Dictionary<string, JsonElement>
        {
            ["n"] = JsonSerializer.SerializeToElement(7)
        };

        await service.UpdateLearningSectionStateAsync(attempt.Id, "parameter-effect", true, true, values);
        await service.PauseAsync(attempt.Id);
        var resumed = await service.ResumeAsync(attempt.Id);
        var results = await service.GetResultsAsync(attempt.Id);

        Assert.Equal(AttemptStatus.InProgress, resumed.Status);
        var progress = Assert.Single(results.LearningSections);
        Assert.True(progress.Visited);
        Assert.True(progress.InteractionChanged);
        Assert.Equal(7, progress.ControlValues["n"].GetInt32());
    }

    private static AttemptService CreateAttemptService(
        AssessmentDefinition assessment,
        InMemoryAttemptRepository? attempts = null,
        InMemoryAttemptSessionStore? sessions = null,
        InMemoryGradeLogRepository? grades = null)
    {
        return new AttemptService(
            new InMemoryAssessmentRepository(assessment),
            attempts ?? new InMemoryAttemptRepository(),
            sessions ?? new InMemoryAttemptSessionStore(),
            grades ?? new InMemoryGradeLogRepository(),
            new InMemoryGuidedProjectSessionRepository(),
            new InMemorySettingsRepository(),
            new AssessmentValidator(),
            new ScoringService(
                new FakeCodeQuestionScorer(),
                new FakeSymbolicExpressionScorer(),
                new FakeCircuitQuestionScorer(),
                null!));
    }
}

internal static class TestData
{
    public static AssessmentDefinition Assessment(
        AssessmentType type = AssessmentType.Quiz,
        IReadOnlyList<QuestionDefinition>? questions = null)
    {
        return new AssessmentDefinition(
            1,
            "calc2-area-between-curves-easy-quiz-s2c",
            "Area Between Curves Basic Quiz",
            type,
            "calculus-2",
            "area-between-curves",
            AssessmentMode.Practice,
            true,
            null,
            null,
            null,
            questions ?? new[] { MultipleChoiceQuestion("q001") });
    }

    public static AssessmentDefinition WorkedExampleAssessment()
    {
        return Assessment(AssessmentType.WorkedExample, Array.Empty<QuestionDefinition>()) with
        {
            Id = "linear-substitution-worked-example",
            Title = "Linear Substitution Worked Example",
            WorkedExamples = new[]
            {
                new WorkedExampleDefinition(
                    "we001",
                    "Solving an integral with linear substitution",
                    "Evaluate $\\int 2(3x+1)^4 dx$.",
                    new[]
                    {
                        WorkedExampleStep("s001"),
                        new WorkedExampleStepDefinition(
                            "s002",
                            "Define the substitution",
                            "Choose the inner expression so the integral becomes easier to read.",
                            "Use the expression inside the power.",
                            FreeResponseQuestion("s002") with
                            {
                                Prompt = "What should $u$ equal?",
                                Explanation = "Set $u=3x+1$ so $du=3dx$ and the remaining constant can be adjusted."
                            })
                    })
            }
        };
    }

    public static WorkedExampleStepDefinition WorkedExampleStep(string id)
    {
        return new WorkedExampleStepDefinition(
            id,
            "Check direct integration",
            "Decide whether this can be solved by a direct antiderivative before choosing substitution.",
            "Try checking whether an inner expression has a constant derivative.",
            MultipleChoiceQuestion(id) with
            {
                Prompt = "Can this integral be solved cleanly by direct integration?",
                Choices = new[]
                {
                    new ChoiceOption("yes", "Yes", Array.Empty<MediaAsset>()),
                    new ChoiceOption("no", "No", Array.Empty<MediaAsset>())
                },
                Answer = new AnswerDefinition("no", Array.Empty<string>(), null, null, null, null, Array.Empty<MediaAsset>()),
                Explanation = "The composed factor suggests substitution because the derivative of $3x+1$ is constant."
            });
    }

    public static AssessmentDefinition GuidedProjectAssessment()
    {
        return Assessment(AssessmentType.GuidedProject, Array.Empty<QuestionDefinition>()) with
        {
            Id = "cpp-runner-guided-project",
            Title = "C++ Runner Guided Project",
            CategoryId = "c++",
            TopicId = "c++-oop",
            GuidedProject = new GuidedProjectDefinition(
                "cpp",
                null,
                null,
                "Build a Runner class.",
                null,
                new[]
                {
                    new GuidedProjectFileDefinition(
                        "Runner.h",
                        "#pragma once\nclass Runner {};",
                        false)
                },
                Array.Empty<GuidedProjectFixtureDefinition>(),
                Array.Empty<GuidedProjectScenarioDefinition>(),
                Array.Empty<string>(),
                new[]
                {
                    new GuidedProjectCheckDefinition(
                        "runner-check",
                        "Runner check",
                        "Checks that Runner exists.",
                        "int main() { cout << \"RUNNER_OK\"; return 0; }",
                        new[] { "RUNNER_OK" },
                        null,
                        null)
                },
                Array.Empty<GuidedProjectCheckDefinition>())
        };
    }

    public static AssessmentDefinition RecallDrillAssessment()
    {
        return Assessment(AssessmentType.RecallDrill, Array.Empty<QuestionDefinition>()) with
        {
            Id = "trig-identities-basic-recall",
            Title = "Trig Identities Basic Recall",
            CategoryId = "trigonometry",
            TopicId = "trig-identities",
            Items = new[]
            {
                new RecallItemDefinition(
                    "typed-1",
                    RecallItemType.Typed,
                    "Define a variable.",
                    new RecallItemAnswerDefinition("A named storage location for a value.", null, Array.Empty<string>(), Array.Empty<MediaAsset>()),
                    "Variables let code refer to values by name.",
                    new[] { "syntax", "definition" }),
                new RecallItemDefinition(
                    "symbolic-1",
                    RecallItemType.Symbolic,
                    "Write the primary Pythagorean identity.",
                    new RecallItemAnswerDefinition(null, "\\sin^2(x)+\\cos^2(x)=1", new[] { "sin^2(x)+cos^2(x)=1" }, Array.Empty<MediaAsset>()),
                    "This follows from points on the unit circle.",
                    new[] { "trig", "pythagorean-identity" }),
                new RecallItemDefinition(
                    "flashcard-1",
                    RecallItemType.Flashcard,
                    "When do you use the Law of Cosines?",
                    new RecallItemAnswerDefinition("When two sides and the included angle, or all three sides, are known.", null, Array.Empty<string>(), Array.Empty<MediaAsset>()),
                    "It generalizes the Pythagorean theorem.",
                    new[] { "trig", "law-of-cosines" }),
                new RecallItemDefinition(
                    "cloze-1",
                    RecallItemType.Cloze,
                    "Complete: sin^2(x) + ____ = 1",
                    new RecallItemAnswerDefinition("cos^2(x)", null, Array.Empty<string>(), Array.Empty<MediaAsset>()),
                    "The missing term is the complementary square.",
                    new[] { "trig" })
            }
        };
    }

    public static AssessmentDefinition GlossaryAssessment()
    {
        var acuteDrill = new RecallItemDefinition(
            "acute-recall",
            RecallItemType.Typed,
            "What angle is less than 90 degrees?",
            new RecallItemAnswerDefinition("Acute angle", null, Array.Empty<string>(), Array.Empty<MediaAsset>()),
            "Acute angles are strictly between zero and ninety degrees.",
            new[] { "acute-angle" });
        var recognitionDrill = new RecallItemDefinition(
            "vertical-recognition",
            RecallItemType.Recognition,
            "Which opposite angles are congruent?",
            new RecallItemAnswerDefinition("Vertical angles", null, Array.Empty<string>(), Array.Empty<MediaAsset>()),
            "Vertical angles are opposite angles at an intersection.",
            new[] { "vertical-angles" })
        {
            ChoiceId = "vertical",
            Choices = new[]
            {
                new ChoiceOption("adjacent", "Adjacent angles", Array.Empty<MediaAsset>()),
                new ChoiceOption("vertical", "Vertical angles", Array.Empty<MediaAsset>())
            }
        };

        return Assessment(AssessmentType.Glossary, Array.Empty<QuestionDefinition>()) with
        {
            Id = "geometry-angle-glossary",
            Title = "Geometry Angle Glossary",
            RandomizeQuestions = false,
            Glossary = new GlossaryDefinition(
                "Study the terms, then recall them.",
                new[]
                {
                    new GlossarySectionDefinition(
                        "classifications",
                        "Classifications",
                        true,
                        "Classify individual angles.",
                        new[]
                        {
                            new GlossaryEntryDefinition(
                                "acute",
                                "Acute Angle",
                                "An angle between zero and ninety degrees.",
                                null,
                                Array.Empty<string>(),
                                Array.Empty<string>(),
                                Array.Empty<MediaAsset>(),
                                new[] { "acute-angle" },
                                new[] { acuteDrill })
                        }),
                    new GlossarySectionDefinition(
                        "relationships",
                        "Relationships",
                        true,
                        "Compare angle pairs.",
                        new[]
                        {
                            new GlossaryEntryDefinition(
                                "vertical",
                                "Vertical Angles",
                                "Opposite angles formed by intersecting lines.",
                                null,
                                Array.Empty<string>(),
                                Array.Empty<string>(),
                                Array.Empty<MediaAsset>(),
                                new[] { "vertical-angles" },
                                new[] { recognitionDrill })
                        })
                })
        };
    }

    public static AssessmentDefinition ConceptLessonAssessment()
    {
        return Assessment(AssessmentType.ConceptLesson, Array.Empty<QuestionDefinition>()) with
        {
            Id = "python-loops-concept-lesson",
            Title = "Python Loops Concept Lesson",
            CategoryId = "python",
            TopicId = "python-control-flow",
            Lesson = new ConceptLessonDefinition(
                "Learn how loops repeat work.",
                new[]
                {
                    new LearningSectionDefinition("intro", "Why loops", true, "Loops repeat a block.", Array.Empty<MediaAsset>(), null),
                    new LearningSectionDefinition(
                        "check-loop",
                        "Check the loop body",
                        true,
                        "Indentation defines the body.",
                        Array.Empty<MediaAsset>(),
                        MultipleChoiceQuestion("check-loop-question"))
                })
        };
    }

    public static AssessmentDefinition InteractiveExplorationAssessment()
    {
        return Assessment(AssessmentType.InteractiveExploration, Array.Empty<QuestionDefinition>()) with
        {
            Id = "parameter-exploration",
            Title = "Parameter Exploration",
            Exploration = new InteractiveExplorationDefinition(
                "Change a control.",
                new[]
                {
                    new ExplorationSectionDefinition(
                        "parameter-effect",
                        "Parameter effect",
                        true,
                        "Move the slider.",
                        new[]
                        {
                            new ExplorationControlDefinition(
                                "n",
                                "slider",
                                "Iterations",
                                1,
                                10,
                                1,
                                "3",
                                Array.Empty<ExplorationOptionDefinition>())
                        },
                        new[]
                        {
                            new ExplorationViewDefinition("double", "readout", "Doubled", "2n", null, null, null, null, null, null)
                        },
                        null)
                })
        };
    }

    public static AssessmentDefinition DirectedProjectAssessment()
    {
        return Assessment(AssessmentType.DirectedProject, Array.Empty<QuestionDefinition>()) with
        {
            Id = "dp-test",
            Title = "Test Directed Project",
            DirectedProject = new DirectedProjectDefinition(
                "A test directed project.",
                Array.Empty<string>(),
                new[]
                {
                    new DirectedProjectPhaseDefinition(
                        "phase-1",
                        "Phase 1",
                        true,
                        new[]
                        {
                            new DirectedProjectStepDefinition(
                                "step-1",
                                "Step 1",
                                "Do the first thing.")
                            {
                                Checklist = new[]
                                {
                                    new DirectedProjectChecklistItemDefinition("chk-1", "Done thing 1")
                                },
                                NotesPrompt = "Any notes?"
                            }
                        })
                })
            {
                EstimatedTimeMinutes = 10,
                Resources = Array.Empty<DirectedProjectResourceDefinition>()
            }
        };
    }


    public static QuestionDefinition MultipleChoiceQuestion(string id)
    {
        return new QuestionDefinition(
            id,
            QuestionType.MultipleChoice,
            "What does the area between two curves represent?",
            new[]
            {
                new ChoiceOption("a", "The accumulated vertical difference between two functions over an interval", Array.Empty<MediaAsset>()),
                new ChoiceOption("b", "The slope of the upper function", Array.Empty<MediaAsset>())
            },
            new AnswerDefinition("a", Array.Empty<string>(), null, null, null, null, Array.Empty<MediaAsset>()),
            "Area between curves measures accumulated difference.",
            Array.Empty<MediaAsset>());
    }

    public static QuestionDefinition SelectAllQuestion(string id)
    {
        return new QuestionDefinition(
            id,
            QuestionType.SelectAll,
            "Which are valid setup steps?",
            new[]
            {
                new ChoiceOption("a", "Identify the upper function", Array.Empty<MediaAsset>()),
                new ChoiceOption("b", "Identify the lower function", Array.Empty<MediaAsset>()),
                new ChoiceOption("c", "Subtract lower from upper", Array.Empty<MediaAsset>())
            },
            new AnswerDefinition(null, new[] { "a", "b", "c" }, null, null, null, null, Array.Empty<MediaAsset>()),
            "Area between curves requires upper minus lower.",
            Array.Empty<MediaAsset>());
    }

    public static QuestionDefinition FreeResponseQuestion(string id)
    {
        return new QuestionDefinition(
            id,
            QuestionType.FreeResponse,
            "Explain what the integral represents.",
            Array.Empty<ChoiceOption>(),
            new AnswerDefinition(null, Array.Empty<string>(), "The accumulated difference between upper and lower functions.", "selfCheck", null, null, Array.Empty<MediaAsset>())
            {
                KeyPoints = new[] { "Mention the accumulated difference.", "Identify upper minus lower." }
            },
            "The integral sums vertical differences over the interval.",
            Array.Empty<MediaAsset>());
    }

    public static QuestionDefinition NumericResponseQuestion(string id)
    {
        return new QuestionDefinition(
            id,
            QuestionType.NumericResponse,
            "Compute the volume to the nearest hundredth.",
            Array.Empty<ChoiceOption>(),
            new AnswerDefinition(null, Array.Empty<string>(), null, null, 8.38m, 0.01m, Array.Empty<MediaAsset>()),
            "The exact value is 8 pi over 3.",
            new[] { new MediaAsset("image", "/samples/volume-washer.svg", "Washer cross section diagram", null) });
    }

    public static QuestionDefinition CodeQuestion(string id, string language)
    {
        return new QuestionDefinition(
            id,
            QuestionType.Code,
            "Write a function that squares an integer.",
            Array.Empty<ChoiceOption>(),
            new AnswerDefinition(null, Array.Empty<string>(), null, null, null, null, Array.Empty<MediaAsset>()),
            "A square multiplies the value by itself.",
            Array.Empty<MediaAsset>())
        {
            CodeQuestion = new CodeQuestionDefinition(
                language,
                "square",
                language.Equals("cpp", StringComparison.OrdinalIgnoreCase)
                    ? "int square(int n)\n{\n    return n * n;\n}"
                    : "def square(n):\n    return n * n",
                new[] { new CodeQuestionTest("3", "9") })
        };
    }

    public static QuestionDefinition SymbolicResponseQuestion(string id, string mode = "expression")
    {
        return new QuestionDefinition(
            id,
            QuestionType.SymbolicResponse,
            "Simplify $x^2 + 2x + 1$.",
            Array.Empty<ChoiceOption>(),
            new AnswerDefinition(null, Array.Empty<string>(), null, null, null, null, Array.Empty<MediaAsset>())
            {
                SymbolicExpectedLatex = "(x+1)^2",
                SymbolicEquivalenceMode = mode,
                SymbolicVariables = new[] { "x" },
                SymbolicTolerance = 0.000001m
            },
            "The expression factors as $(x+1)^2$.",
            Array.Empty<MediaAsset>());
    }
}

internal sealed class InMemorySettingsRepository : ISettingsRepository
{
    public Task<AppSettings> GetAsync(CancellationToken cancellationToken = default)
    {
        return Task.FromResult(new AppSettings(1, AssessmentMode.Practice, QuestionOrderMode.Randomized, 15, 25, null, null, false));
    }

    public Task SaveAsync(AppSettings settings, CancellationToken cancellationToken = default)
    {
        return Task.CompletedTask;
    }
}

internal sealed class InMemoryAssessmentRepository : IAssessmentRepository
{
    private readonly AssessmentDefinition assessment;

    public InMemoryAssessmentRepository(AssessmentDefinition assessment)
    {
        this.assessment = assessment;
    }

    public Task<IReadOnlyList<AssessmentSummary>> ListByCategoryAsync(string categoryId, CancellationToken cancellationToken = default)
    {
        IReadOnlyList<AssessmentSummary> summaries = new[]
        {
            new AssessmentSummary(
                assessment.Id,
                assessment.Title,
                assessment.AssessmentType,
                assessment.CategoryId,
                assessment.TopicId,
                assessment.AssessmentType is AssessmentType.WorkedExample
                    ? assessment.WorkedExamples.Sum(example => example.Steps.Count)
                    : assessment.AssessmentType is AssessmentType.RecallDrill
                        ? assessment.Items.Count
                        : assessment.Questions.Count)
        };

        return Task.FromResult(summaries);
    }

    public Task<AssessmentDefinition?> GetByIdAsync(string assessmentId, CancellationToken cancellationToken = default)
    {
        return Task.FromResult<AssessmentDefinition?>(assessment);
    }

    public Task SaveAsync(AssessmentDefinition assessment, CancellationToken cancellationToken = default)
    {
        return Task.CompletedTask;
    }

    public Task<AssessmentValidationResult> ValidateFileAsync(string fileName, CancellationToken cancellationToken = default)
    {
        return Task.FromResult(new AssessmentValidationResult(Array.Empty<ValidationIssue>()));
    }
}

internal sealed class InMemoryAttemptRepository : IAttemptRepository
{
    private readonly Dictionary<string, Attempt> attempts = new(StringComparer.OrdinalIgnoreCase);

    public Task<IReadOnlyList<Attempt>> ListAsync(CancellationToken cancellationToken = default)
    {
        return Task.FromResult<IReadOnlyList<Attempt>>(attempts.Values.OrderByDescending(attempt => attempt.StartedAt).ToList());
    }

    public Task<Attempt?> GetByIdAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        attempts.TryGetValue(attemptId, out var attempt);
        return Task.FromResult(attempt);
    }

    public Task SaveAsync(Attempt attempt, CancellationToken cancellationToken = default)
    {
        attempts[attempt.Id] = attempt;
        return Task.CompletedTask;
    }

    public Task DeleteAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        attempts.Remove(attemptId);
        return Task.CompletedTask;
    }

    public Task<IReadOnlyList<string>> GetCompletedAssessmentIdsAsync(CancellationToken cancellationToken = default)
    {
        var ids = attempts.Values
            .Where(a => a.Status == AttemptStatus.Completed)
            .Select(a => a.AssessmentId)
            .Distinct()
            .ToList();
        return Task.FromResult<IReadOnlyList<string>>(ids);
    }
}

internal sealed class InMemoryAttemptSessionStore : IAttemptSessionStore
{
    private readonly Dictionary<string, Attempt> attempts = new(StringComparer.OrdinalIgnoreCase);

    public Task<IReadOnlyList<Attempt>> ListAsync(CancellationToken cancellationToken = default)
    {
        return Task.FromResult<IReadOnlyList<Attempt>>(attempts.Values.OrderByDescending(attempt => attempt.StartedAt).ToList());
    }

    public Task<Attempt?> GetByIdAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        attempts.TryGetValue(attemptId, out var attempt);
        return Task.FromResult(attempt);
    }

    public Task SaveAsync(Attempt attempt, CancellationToken cancellationToken = default)
    {
        attempts[attempt.Id] = attempt;
        return Task.CompletedTask;
    }

    public Task DeleteAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        attempts.Remove(attemptId);
        return Task.CompletedTask;
    }
}

internal sealed class InMemoryGradeLogRepository : IGradeLogRepository
{
    private readonly List<GradeLogEntry> entries = new();

    public Task<IReadOnlyList<GradeLogEntry>> ListAsync(CancellationToken cancellationToken = default)
    {
        return Task.FromResult<IReadOnlyList<GradeLogEntry>>(entries.ToList());
    }

    public Task AddAsync(GradeLogEntry entry, CancellationToken cancellationToken = default)
    {
        entries.Add(entry);
        return Task.CompletedTask;
    }

    public Task RemoveByAttemptIdAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        entries.RemoveAll(entry => string.Equals(entry.AttemptId, attemptId, StringComparison.OrdinalIgnoreCase));
        return Task.CompletedTask;
    }
}

internal sealed class InMemoryGuidedProjectSessionRepository : IGuidedProjectSessionRepository
{
    private readonly Dictionary<string, GuidedProjectSession> sessions = new(StringComparer.OrdinalIgnoreCase);

    public Task<GuidedProjectSession?> GetAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        sessions.TryGetValue(attemptId, out var session);
        return Task.FromResult(session);
    }

    public Task SaveAsync(GuidedProjectSession session, CancellationToken cancellationToken = default)
    {
        sessions[session.AttemptId] = session;
        return Task.CompletedTask;
    }

    public Task DeleteAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        sessions.Remove(attemptId);
        return Task.CompletedTask;
    }
}

internal sealed class FakeCodeQuestionScorer : ICodeQuestionScorer
{
    public Task<AnswerEvaluation> ScoreAsync(
        QuestionDefinition question,
        SubmittedAnswer submittedAnswer,
        AppSettings settings,
        CancellationToken cancellationToken = default)
    {
        return Task.FromResult(new AnswerEvaluation(question.Id, true, question.Explanation, "All code tests pass")
        {
            CodeFeedback = new CodeFeedback(
                new[] { new CodeTestResult(1, "3", "9", "9", true) },
                null,
                "9",
                null)
        });
    }
}

internal sealed class FakeSymbolicExpressionScorer : ISymbolicExpressionScorer
{
    public Task<AnswerEvaluation> ScoreAsync(
        QuestionDefinition question,
        SubmittedAnswer submittedAnswer,
        AppSettings settings,
        CancellationToken cancellationToken = default)
    {
        return Task.FromResult(new AnswerEvaluation(question.Id, true, question.Explanation, question.Answer.SymbolicExpectedLatex)
        {
            SymbolicFeedback = new SymbolicFeedback(
                true,
                submittedAnswer.SymbolicLatex,
                question.Answer.SymbolicExpectedLatex ?? question.Answer.ExpectedLatex,
                question.Answer.SymbolicEquivalenceMode ?? question.Answer.EquivalenceMode ?? "expression",
                "Expressions matched.")
        });
    }
}

internal sealed class FakeCircuitQuestionScorer : ICircuitQuestionScorer
{
    public Task<AnswerEvaluation> ScoreAsync(
        QuestionDefinition question,
        SubmittedAnswer submittedAnswer,
        AppSettings settings,
        CancellationToken cancellationToken = default)
    {
        return Task.FromResult(new AnswerEvaluation(question.Id, true, question.Explanation, "Circuit matching requirements")
        {
            CircuitFeedback = new CircuitFeedback(
                Array.Empty<string>(), Array.Empty<string>(), Array.Empty<string>(),
                Array.Empty<string>(), Array.Empty<string>(), Array.Empty<string>(),
                null, null, new Dictionary<string, string>(), Array.Empty<string>())
        });
    }
}
