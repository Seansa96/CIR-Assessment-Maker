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

        var file = @"C:\Users\SeanS\Downloads\cir_app\data\assessments\physics-rotational-variables-concept-lesson-1.yaml";
        var content = File.ReadAllText(file);
        var dto = deserializer.Deserialize<AssessmentFileDto>(content);
        
        Console.WriteLine($"Lesson is null? {dto.Lesson == null}");
        if (dto.Lesson != null) {
            Console.WriteLine($"Introduction: '{dto.Lesson.Introduction}'");
            Console.WriteLine($"Sections is null? {dto.Lesson.Sections == null}");
            if (dto.Lesson.Sections != null && dto.Lesson.Sections.Count > 0) {
                var section = dto.Lesson.Sections[0];
                Console.WriteLine($"Section 0 Media is null? {section.Media == null}");
                if (section.Media != null && section.Media.Count > 0) {
                    var media = section.Media[0];
                    Console.WriteLine($"Media 0 Type: '{media.Type}'");
                    Console.WriteLine($"Media 0 Src: '{media.Src}'");
                    Console.WriteLine($"Media 0 Alt: '{media.Alt}'");
                }
            }
        }
    }
}
