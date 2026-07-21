using System;
using System.Text.Json;
using QuizApp.Core.Domain;
using System.Collections.Generic;

var feedback = new CodeFeedback(
    new List<CodeTestResult> { new CodeTestResult(1, "test input", "test expected", "test actual", false) },
    "compile output",
    "run output",
    "error output"
);

var options = new JsonSerializerOptions
{
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
};

Console.WriteLine(JsonSerializer.Serialize(feedback, options));
