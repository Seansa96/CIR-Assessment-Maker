using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Xunit;
using Xunit.Abstractions;

namespace QuizApp.Tests;

public sealed class AssessmentContentAuditTests
{
    private readonly ITestOutputHelper output;
    private readonly AssessmentContentAudit audit;

    public AssessmentContentAuditTests(ITestOutputHelper output)
    {
        this.output = output;
        
        // Resolve the real data folder path
        var baseDir = AppContext.BaseDirectory;
        var projectRoot = "";
        
        var current = new DirectoryInfo(baseDir);
        while (current != null && !Directory.Exists(Path.Combine(current.FullName, "data", "assessments")))
        {
            current = current.Parent;
        }
        if (current != null)
        {
            projectRoot = current.FullName;
        }
        else
        {
            throw new DirectoryNotFoundException($"Could not find data/assessments from {baseDir}");
        }

        audit = new AssessmentContentAudit(projectRoot);
    }

    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task All_authored_assessment_files_deserialize_and_validate()
    {
        var files = audit.EnumerateAssessmentFiles();
        Assert.NotEmpty(files);
        
        var errors = await audit.ValidateAllAssessmentsAsync();
        
        if (errors.Any())
        {
            var message = string.Join(Environment.NewLine, errors);
            output.WriteLine(message);
            Assert.Fail($"Found {errors.Count} validation errors:\n{message}");
        }
    }

    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task All_authored_assessment_ids_are_unique()
    {
        var errors = await audit.CheckForDuplicateIdsAsync();
        
        if (errors.Any())
        {
            var message = string.Join(Environment.NewLine, errors);
            output.WriteLine(message);
            Assert.Fail($"Found {errors.Count} duplicate IDs:\n{message}");
        }
    }

    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task All_authored_assessments_have_valid_taxonomy()
    {
        var errors = await audit.ValidateTaxonomyAsync();
        
        if (errors.Any())
        {
            var message = string.Join(Environment.NewLine, errors);
            output.WriteLine(message);
            Assert.Fail($"Found {errors.Count} taxonomy errors:\n{message}");
        }
    }

    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task All_authored_assessments_have_valid_navigation_metadata()
    {
        var errors = await audit.ValidateNavigationMetadataAsync();
        
        if (errors.Any())
        {
            var message = string.Join(Environment.NewLine, errors);
            output.WriteLine(message);
            Assert.Fail($"Found {errors.Count} navigation metadata errors:\n{message}");
        }
    }

    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task Assessment_yaml_does_not_use_double_quoted_latex_backslashes()
    {
        var errors = await audit.CheckForDoubleQuotedLatexBackslashesAsync();
        
        if (errors.Any())
        {
            var message = string.Join(Environment.NewLine, errors);
            output.WriteLine(message);
            Assert.Fail($"Found {errors.Count} LaTeX backslash hazards in double quotes:\n{message}");
        }
    }
}
