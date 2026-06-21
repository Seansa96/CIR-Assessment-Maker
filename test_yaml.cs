using System;
using System.IO;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

class Program {
    static void Main() {
        var deserializer = new DeserializerBuilder()
            .WithNamingConvention(CamelCaseNamingConvention.Instance)
            .IgnoreUnmatchedProperties()
            .Build();

        foreach (var file in Directory.GetFiles("data/assessments", "*.yaml")) {
            try {
                var content = File.ReadAllText(file);
                // We don't have the exact DTO types here, but let's just see if we can load it into dynamic or object? 
                // Wait, without the DTO types, YamlDotNet won't throw the same exception.
            } catch (Exception e) {
                Console.WriteLine(file + ": " + e.Message);
            }
        }
    }
}
