using System;
using System.IO;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

class Program
{
    static void Main(string[] args)
    {
        var deserializer = new DeserializerBuilder()
            .WithNamingConvention(CamelCaseNamingConvention.Instance)
            .Build();

        string path = @"C:\Users\SeanS\Downloads\cir_app\data\assessments\csharp-combat-turn-guided-project.yaml";
        try
        {
            string content = File.ReadAllText(path);
            var result = deserializer.Deserialize<dynamic>(content);
            Console.WriteLine("Parsed to dynamic successfully!");
        }
        catch (Exception ex)
        {
            Console.WriteLine("DYNAMIC PARSE ERROR: " + ex);
        }
    }
}
