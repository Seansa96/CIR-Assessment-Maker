using System;
using System.IO;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

class Program
{
    static void Main(string[] args)
    {
        var files = Directory.GetFiles(@"..\data\assessments", "*.yaml");
        
        var deserializer = new DeserializerBuilder()
            .WithNamingConvention(CamelCaseNamingConvention.Instance)
            .IgnoreUnmatchedProperties()
            .Build();
        
        foreach (var file in files)
        {
            try
            {
                var content = File.ReadAllText(file);
                deserializer.Deserialize<object>(content);
            }
            catch (YamlDotNet.Core.YamlException ex)
            {
                Console.WriteLine($"Failed to parse {file}");
                Console.WriteLine($"Line: {ex.Start.Line}, Column: {ex.Start.Column}");
                Console.WriteLine($"Error: {ex.Message}");
                if (ex.InnerException != null)
                {
                    Console.WriteLine($"Inner: {ex.InnerException.Message}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Other error on {file}: {ex.Message}");
            }
        }
        Console.WriteLine("Done.");
    }
}
