using System.Text.Json;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace QuizApp.Infrastructure.Files;

internal static class FileFormat
{
    private static readonly JsonSerializerOptions JsonOptions = new(JsonSerializerDefaults.Web)
    {
        WriteIndented = true,
        PropertyNameCaseInsensitive = true
    };

    private static readonly IDeserializer YamlDeserializer = new DeserializerBuilder()
        .WithNamingConvention(CamelCaseNamingConvention.Instance)
        .IgnoreUnmatchedProperties()
        .Build();

    private static readonly ISerializer YamlSerializer = new SerializerBuilder()
        .WithNamingConvention(CamelCaseNamingConvention.Instance)
        .Build();

    public static async Task<T?> ReadAsync<T>(string path, CancellationToken cancellationToken = default)
    {
        if (!File.Exists(path))
        {
            return default;
        }

        var content = await File.ReadAllTextAsync(path, cancellationToken);
        if (Path.GetExtension(path).Equals(".json", StringComparison.OrdinalIgnoreCase))
        {
            return JsonSerializer.Deserialize<T>(content, JsonOptions);
        }

        return YamlDeserializer.Deserialize<T>(content);
    }

    public static T? ReadFromString<T>(string content, string extension = ".yaml")
    {
        if (extension.Equals(".json", StringComparison.OrdinalIgnoreCase))
            return JsonSerializer.Deserialize<T>(content, JsonOptions);
        return YamlDeserializer.Deserialize<T>(content);
    }


    public static async Task WriteJsonAsync<T>(string path, T value, CancellationToken cancellationToken = default)
    {
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        var content = JsonSerializer.Serialize(value, JsonOptions);
        await File.WriteAllTextAsync(path, content, cancellationToken);
    }

    public static async Task WriteYamlAsync<T>(string path, T value, CancellationToken cancellationToken = default)
    {
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        var content = YamlSerializer.Serialize(value);
        await File.WriteAllTextAsync(path, content, cancellationToken);
    }
}
