using QuizApp.Core.Domain;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Tests;

public sealed class AuthoringWorkspaceTests : IDisposable
{
    private readonly string root = Path.Combine(Path.GetTempPath(), "cir-authoring-tests", Guid.NewGuid().ToString("N"));

    [Fact]
    public async Task Import_text_source_creates_private_chunks_and_deduplicates_by_hash()
    {
        Directory.CreateDirectory(root);
        var input = Path.Combine(root, "waves.md");
        await File.WriteAllTextAsync(input, "# Traveling Waves\n\nA wave has speed, wavelength, and frequency.");
        var service = CreateService();

        var first = await service.ImportSourceAsync(new SourceImportRequest(input, "Waves", "CC BY 4.0"));
        var second = await service.ImportSourceAsync(new SourceImportRequest(input, "Different title", null));

        Assert.Equal(first.Manifest.Id, second.Manifest.Id);
        Assert.Equal("completed", first.Manifest.ExtractionStatus);
        Assert.NotEmpty(first.Chunks);
        Assert.All(first.Chunks, chunk => Assert.StartsWith($"{first.Manifest.Id}:chunk-", chunk.Id));
        Assert.True(File.Exists(Path.Combine(root, "data", "source-library", "sources", first.Manifest.Id, "original.md")));
    }

    [Fact]
    public async Task Packet_requires_existing_chunks_and_never_writes_source_text_to_tracked_manifest()
    {
        Directory.CreateDirectory(root);
        var input = Path.Combine(root, "source.txt");
        await File.WriteAllTextAsync(input, "Private verbatim textbook sentence.");
        var service = CreateService();
        var source = await service.ImportSourceAsync(new SourceImportRequest(input, null, null));

        var packet = await service.ExportPacketAsync("physics-1", "traveling-waves", ["wave-speed"], [source.Chunks[0].Id]);
        await service.SaveBlueprintAsync(new QuestionBlueprint(1, "wave-speed-blueprint", "physics-1", "traveling-waves", "wave-speed", "numericResponse", [source.Chunks[0].Id], ["wave relation"], ["identify values", "solve relation"], ["scenario", "unknown"], "Using amplitude instead of wavelength.", "easy", 2, false, SourceReviewState.NeedsReview));

        Assert.Single(packet.Chunks);
        var saved = Path.Combine(root, "docs", "assessment-reference", "question-blueprints", "wave-speed-blueprint.json");
        Assert.True(File.Exists(saved));
        Assert.DoesNotContain("Private verbatim textbook sentence.", await File.ReadAllTextAsync(saved));
    }

    [Fact]
    public async Task Blueprint_rejects_parameter_only_generation_metadata()
    {
        var service = CreateService();
        var blueprint = new QuestionBlueprint(1, "invalid-blueprint", "physics-1", "traveling-waves", "wave-speed", "numericResponse", ["src-example:chunk-0001"], ["wave relation"], ["solve"], ["numbers"], "trap", "easy", 1, false, SourceReviewState.Draft);
        var exception = await Assert.ThrowsAsync<InvalidOperationException>(() => service.SaveBlueprintAsync(blueprint));
        Assert.Contains("two method steps", exception.Message);
    }

    [Fact]
    public async Task Approved_draft_publishes_validated_blueprints()
    {
        Directory.CreateDirectory(root);
        var input = Path.Combine(root, "source.txt");
        await File.WriteAllTextAsync(input, "Wave speed depends on frequency and wavelength.");
        var service = CreateService();
        var source = await service.ImportSourceAsync(new SourceImportRequest(input, null, null));
        var payload = $$"""{"questionBlueprints":[{"schemaVersion":1,"id":"draft-wave-speed","categoryId":"physics-1","topicId":"traveling-waves","objectiveId":"wave-speed","questionType":"numericResponse","sourceChunkIds":["{{source.Chunks[0].Id}}"],"governingPrinciples":["wave relation"],"methodSteps":["identify values","solve relation"],"variationAxes":["scenario","unknown"],"commonTrap":"trap","difficulty":"easy","reasoningDepth":2,"requiresDiagram":false,"reviewState":"needsReview"}]}""";
        var draft = await service.ImportDraftAsync("packet-test", payload);
        await service.SetDraftStateAsync(draft.Id, SourceReviewState.Approved);
        Assert.Equal(SourceReviewState.Approved, (await service.ListBlueprintsAsync("physics-1")).Single().ReviewState);
    }



    private FileAuthoringWorkspaceService CreateService() => new(new FileStorageOptions { DataRoot = Path.Combine(root, "data") });
    public void Dispose() { if (Directory.Exists(root)) Directory.Delete(root, true); }
}
