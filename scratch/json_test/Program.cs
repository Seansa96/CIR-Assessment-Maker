using System;
using System.Text.Json;
using System.Collections.Generic;

public sealed record CodeFeedback(
    IReadOnlyList<CodeTestResult> Tests,
    string? CompileOutput,
    string? RunOutput,
    string? Error);

public sealed record CodeTestResult(
    int Index,
    string Input,
    string Expected,
    string? Actual,
    bool Passed);

class Program
{
    static void Main()
    {
        var feedback = new CodeFeedback(
            new List<CodeTestResult> { new CodeTestResult(1, "test", "Build\nRun", null, false) },
            "compile error",
            null,
            null
        );

        var options = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
            DefaultIgnoreCondition = System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull
        };

        Console.WriteLine(JsonSerializer.Serialize(feedback, options));
    }
}
