using System;
using System.IO;
using QuizApp.Infrastructure.Files;
using YamlDotNet.Core;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

class Program {
    static void Main() {
        var deserializer = new DeserializerBuilder()
            .WithNamingConvention(CamelCaseNamingConvention.Instance)
            .IgnoreUnmatchedProperties()
            .Build();

        var files = Directory.GetFiles(@"..\..\..\data\assessments", "*.yaml");
        foreach (var file in files) {
            try {
                var content = File.ReadAllText(file);
                deserializer.Deserialize<AssessmentFileDto>(content);
            } catch (Exception e) {
                Console.WriteLine($"FAILED ON: {file}");
                Console.WriteLine(e.Message);
                if (e is YamlException ye) {
                    Console.WriteLine($"Line: {ye.Start.Line}, Col: {ye.Start.Column}");
                }
                if (e.InnerException != null) Console.WriteLine(e.InnerException.Message);
            }
        }
        Console.WriteLine("Done checking all yaml files");
    }
}
