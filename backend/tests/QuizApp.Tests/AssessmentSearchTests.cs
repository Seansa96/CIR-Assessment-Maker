using Xunit;
using QuizApp.Core.Domain;
using QuizApp.Infrastructure.Retention;

namespace QuizApp.Tests;

public class AssessmentSearchTests
{
    [Fact]
    public void SearchNormalizer_Handles_Punctuation_And_MathTerms()
    {
        var input = "This is a u-sub (integration) problem with dy/dx! And A-B_C.";
        var expected = "this is a u sub integration problem with dy dx and a b c";
        
        var actual = SearchNormalizer.Normalize(input);
        
        Assert.Equal(expected, actual);
    }

    [Theory]
    [InlineData("work", "work", 0, 0)]
    [InlineData("work", "word", 1, 1)]
    [InlineData("wor", "word", 1, 1)]
    [InlineData("work", "working", 3, 3)]
    [InlineData("work", "working", 2, 3)] // Max distance 2, should return 3
    public void SearchNormalizer_BoundedLevenshtein_ReturnsExpected(string s, string t, int maxDistance, int expectedDistance)
    {
        var distance = SearchNormalizer.BoundedLevenshteinDistance(s, t, maxDistance);
        Assert.Equal(expectedDistance, distance);
    }
}
