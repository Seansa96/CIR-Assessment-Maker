using System;
using System.IO;
using QuizApp.Core.Domain;
using QuizApp.Infrastructure.Files;

var content = File.ReadAllText(@"c:\Users\SeanS\Downloads\cir_app\data\assessments\python-sockets-conceptual-worked-example.yaml");
var deserializer = FileFormat.CreateDeserializer();
try
{
    var assessment = deserializer.Deserialize<AssessmentDefinition>(content);
    Console.WriteLine($"Parsed assessment: {assessment.Id}");
    foreach (var we in assessment.WorkedExamples)
    {
        Console.WriteLine($"WE: {we.Id}");
        foreach (var step in we.Steps)
        {
            Console.WriteLine($"  Step: {step.Id}");
            var q = step.Question;
            if (q == null)
            {
                Console.WriteLine("    Question is NULL");
            }
            else
            {
                Console.WriteLine($"    Question Id: {q.Id}");
                Console.WriteLine($"    Question Type: {q.Type}");
                Console.WriteLine($"    Question Prompt: {q.Prompt}");
            }
        }
    }
}
catch (Exception ex)
{
    Console.WriteLine("Exception: " + ex.Message);
}
