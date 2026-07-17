using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using YamlDotNet.RepresentationModel;

namespace QuizApp.Infrastructure.Files;

public class AssessmentSourceInspector : IAssessmentSourceInspector
{
    public AssessmentSourceInspection Inspect(string content, string extension, string? sourcePath = null)
    {
        var diagnostics = new List<AssessmentSourceDiagnostic>();

        try
        {
            var stream = new YamlStream();
            using var reader = new StringReader(content);
            stream.Load(reader);

            if (stream.Documents.Count > 0)
            {
                var root = stream.Documents[0].RootNode;
                if (root is YamlMappingNode rootMap)
                {
                    InspectRoot(rootMap, diagnostics, sourcePath);
                    InspectNodesRecursively(rootMap, diagnostics, sourcePath);
                }
            }
        }
        catch (Exception ex)
        {
            diagnostics.Add(new AssessmentSourceDiagnostic
            {
                Severity = DiagnosticSeverity.Error,
                Code = "PARSE_ERROR",
                Message = $"Failed to parse source: {ex.Message}",
                Path = sourcePath
            });
        }

        return new AssessmentSourceInspection
        {
            IsValid = !diagnostics.Any(d => d.Severity == DiagnosticSeverity.Error),
            Diagnostics = diagnostics
        };
    }

    private void InspectRoot(YamlMappingNode rootMap, List<AssessmentSourceDiagnostic> diagnostics, string? sourcePath)
    {
        foreach (var entry in rootMap.Children)
        {
            if (entry.Key is YamlScalarNode keyNode)
            {
                var key = keyNode.Value;
                if (key == "subcategoryId")
                {
                    AddDiagnostic(diagnostics, "LEGACY_SUBCATEGORY_ID", 
                        "Top-level 'subcategoryId' is unsupported. Use singular 'topicId'.", 
                        sourcePath, keyNode, key, "topicId");
                }
                else if (key == "subcategoryIds")
                {
                    AddDiagnostic(diagnostics, "LEGACY_SUBCATEGORY_IDS", 
                        "Top-level 'subcategoryIds' is unsupported. Every assessment must use exactly one singular 'topicId'.", 
                        sourcePath, keyNode, key, "topicId");
                }
                else if (key == "learningGoal")
                {
                    AddDiagnostic(diagnostics, "MISPLACED_LEARNING_GOAL", 
                        "Top-level 'learningGoal' belongs under 'navigation'.", 
                        sourcePath, keyNode, key, "navigation.learningGoal");
                }
                else if (key == "activityType")
                {
                    AddDiagnostic(diagnostics, "MISPLACED_ACTIVITY_TYPE", 
                        "Top-level 'activityType' belongs under 'navigation'.", 
                        sourcePath, keyNode, key, "navigation.activityType");
                }
                else if (key == "tags")
                {
                    AddDiagnostic(diagnostics, "MISPLACED_NAVIGATION_TAGS", 
                        "Top-level 'tags' belongs under 'navigation'.", 
                        sourcePath, keyNode, key, "navigation.tags");
                }
            }
        }
    }

    private void InspectNodesRecursively(YamlNode node, List<AssessmentSourceDiagnostic> diagnostics, string? sourcePath)
    {
        if (node is YamlMappingNode map)
        {
            // Check for answer expected
            if (TryGetScalarValue(map, "type", out var typeValue))
            {
                if (typeValue == "numericResponse" || typeValue == "symbolicResponse")
                {
                    if (map.Children.TryGetValue(new YamlScalarNode("answer"), out var answerNode) && answerNode is YamlMappingNode answerMap)
                    {
                        foreach (var ansEntry in answerMap.Children)
                        {
                            if (ansEntry.Key is YamlScalarNode ansKeyNode && ansKeyNode.Value == "expected")
                            {
                                if (typeValue == "numericResponse")
                                {
                                    AddDiagnostic(diagnostics, "LEGACY_NUMERIC_EXPECTED", 
                                        "Numeric answer uses obsolete 'expected' instead of 'value'.", 
                                        sourcePath, ansKeyNode, "expected", "value");
                                }
                                else if (typeValue == "symbolicResponse")
                                {
                                    AddDiagnostic(diagnostics, "LEGACY_SYMBOLIC_EXPECTED", 
                                        "Symbolic answer uses obsolete 'expected' instead of 'expectedLatex'.", 
                                        sourcePath, ansKeyNode, "expected", "expectedLatex");
                                }
                            }
                        }
                    }
                }
            }

            foreach (var child in map.Children)
            {
                InspectNodesRecursively(child.Value, diagnostics, sourcePath);
            }
        }
        else if (node is YamlSequenceNode seq)
        {
            foreach (var child in seq.Children)
            {
                InspectNodesRecursively(child, diagnostics, sourcePath);
            }
        }
    }

    private bool TryGetScalarValue(YamlMappingNode map, string key, out string? value)
    {
        if (map.Children.TryGetValue(new YamlScalarNode(key), out var node) && node is YamlScalarNode scalar)
        {
            value = scalar.Value;
            return true;
        }
        value = null;
        return false;
    }

    private void AddDiagnostic(List<AssessmentSourceDiagnostic> diagnostics, string code, string message, string? path, YamlNode node, string actualKey, string suggestedKey)
    {
        // "For these known legacy keys, use activation-blocking errors after the migration is complete."
        // We will make them Errors.
        diagnostics.Add(new AssessmentSourceDiagnostic
        {
            Severity = DiagnosticSeverity.Error,
            Code = code,
            Message = message,
            Path = path,
            Line = (int?)node.Start.Line,
            Column = (int?)node.Start.Column,
            ActualKey = actualKey,
            SuggestedKey = suggestedKey
        });
    }
}
