using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;
using QuizApp.Infrastructure.SymbolicMath;

namespace QuizApp.Tests;

public sealed class CortexSymbolicMathEngineTests
{
    [Fact]
    public async Task CompareAsync_matches_equivalent_expression()
    {
        var engine = CreateEngine();

        var result = await engine.CompareAsync(new SymbolicComparisonRequest(
            "x^2+2x+1",
            "(x+1)^2",
            "expression",
            new[] { "x" },
            0.000001m));

        Assert.True(result.IsEquivalent);
        Assert.True(result.ParseSucceeded);
    }

    [Fact]
    public async Task CompareAsync_matches_antiderivative_by_derivative()
    {
        var engine = CreateEngine();

        var result = await engine.CompareAsync(new SymbolicComparisonRequest(
            "\\frac{x^3}{3}+7",
            "\\frac{x^3}{3}+C",
            "derivative",
            new[] { "x" },
            0.000001m));

        Assert.True(result.IsEquivalent);
        Assert.True(result.ParseSucceeded);
    }

    [Fact]
    public async Task CompareAsync_reports_malformed_latex()
    {
        var engine = CreateEngine();

        var result = await engine.CompareAsync(new SymbolicComparisonRequest(
            "\\notacommand{x}",
            "x",
            "expression",
            new[] { "x" },
            0.000001m));

        Assert.False(result.IsEquivalent);
        Assert.False(result.ParseSucceeded);
        Assert.Equal("Submitted answer could not be parsed.", result.Reason);
    }

    private static CortexSymbolicMathEngine CreateEngine()
    {
        return new CortexSymbolicMathEngine(new FileStorageOptions
        {
            DataRoot = Path.Combine(FindRepoRoot(), "data")
        });
    }

    private static string FindRepoRoot()
    {
        var directory = new DirectoryInfo(AppContext.BaseDirectory);
        while (directory is not null)
        {
            if (File.Exists(Path.Combine(directory.FullName, "frontend", "scripts", "symbolic-engine.mjs")))
            {
                return directory.FullName;
            }

            directory = directory.Parent;
        }

        throw new DirectoryNotFoundException("Could not locate repository root.");
    }
}
