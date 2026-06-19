using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public sealed class CircuitQuestionScorer : ICircuitQuestionScorer
{
    private readonly ISymbolicMathEngine mathEngine;

    public CircuitQuestionScorer(ISymbolicMathEngine mathEngine)
    {
        this.mathEngine = mathEngine;
    }

    public async Task<AnswerEvaluation> ScoreAsync(
        QuestionDefinition question,
        SubmittedAnswer submittedAnswer,
        AppSettings settings,
        CancellationToken cancellationToken = default)
    {
        var expected = question.Answer.CircuitAnswer;
        var submitted = submittedAnswer.CircuitAnswer;
        var interactionMode = question.CircuitQuestion?.InteractionMode ?? "select";

        if (expected is null)
        {
            return new AnswerEvaluation(question.Id, false, question.Explanation, "No expected circuit answer defined.");
        }

        if (submitted is null)
        {
            return new AnswerEvaluation(question.Id, false, question.Explanation, "No circuit answer was submitted.")
            {
                CircuitFeedback = new CircuitFeedback(
                    Array.Empty<string>(), Array.Empty<string>(), Array.Empty<string>(),
                    Array.Empty<string>(), Array.Empty<string>(), Array.Empty<string>(),
                    null, null, new Dictionary<string, string>(), Array.Empty<string>())
            };
        }

        return interactionMode.ToLowerInvariant() switch
        {
            "select" => ScoreSelectMode(question, expected, submitted),
            "meterplacement" => ScoreMeterPlacementMode(question, expected, submitted),
            "valueentry" => await ScoreValueEntryModeAsync(question, expected, submitted, cancellationToken),
            "build" => ScoreBuildMode(question, expected, submitted),
            _ => new AnswerEvaluation(question.Id, false, question.Explanation, $"Unsupported interaction mode: {interactionMode}")
        };
    }

    private static AnswerEvaluation ScoreSelectMode(QuestionDefinition question, CircuitAnswerDefinition expected, SubmittedCircuitAnswer submitted)
    {
        var expectedTargets = expected.SelectedTargetIds ?? Array.Empty<string>();
        var submittedComponents = submitted.SelectedComponentIds ?? Array.Empty<string>();
        var submittedNodes = submitted.SelectedNodeIds ?? Array.Empty<string>();
        var submittedBranches = submitted.SelectedBranchIds ?? Array.Empty<string>();

        var submittedTargets = submittedComponents.Concat(submittedNodes).Concat(submittedBranches).ToList();

        var expectedSet = expectedTargets.ToHashSet(StringComparer.OrdinalIgnoreCase);
        var submittedSet = submittedTargets.ToHashSet(StringComparer.OrdinalIgnoreCase);

        var incorrectTargets = new List<string>();
        foreach (var sub in submittedSet)
        {
            if (!expectedSet.Contains(sub))
            {
                incorrectTargets.Add(sub);
            }
        }

        var missingTargets = new List<string>();
        foreach (var exp in expectedSet)
        {
            if (!submittedSet.Contains(exp))
            {
                missingTargets.Add(exp);
            }
        }

        bool isCorrect = incorrectTargets.Count == 0 && missingTargets.Count == 0;

        return new AnswerEvaluation(question.Id, isCorrect, question.Explanation, string.Join(", ", expectedTargets))
        {
            CircuitFeedback = new CircuitFeedback(
                Array.Empty<string>(), Array.Empty<string>(), Array.Empty<string>(),
                Array.Empty<string>(), Array.Empty<string>(), incorrectTargets,
                null, null, new Dictionary<string, string>(), expectedTargets.ToList())
        };
    }

    private static AnswerEvaluation ScoreMeterPlacementMode(QuestionDefinition question, CircuitAnswerDefinition expected, SubmittedCircuitAnswer submitted)
    {
        var expectedMeter = expected.MeterPlacement;
        if (expectedMeter is null)
        {
            return new AnswerEvaluation(question.Id, false, question.Explanation, "No expected meter placement defined.");
        }

        if (!string.Equals(submitted.MeterType, expectedMeter.MeterType, StringComparison.OrdinalIgnoreCase))
        {
            return new AnswerEvaluation(question.Id, false, question.Explanation, $"Expected meter type '{expectedMeter.MeterType}', but got '{submitted.MeterType}'.")
            {
                CircuitFeedback = new CircuitFeedback(
                    Array.Empty<string>(), Array.Empty<string>(), Array.Empty<string>(),
                    Array.Empty<string>(), Array.Empty<string>(), Array.Empty<string>(),
                    true, null, new Dictionary<string, string>(), Array.Empty<string>())
            };
        }

        bool incorrectPlacement = false;
        bool? incorrectPolarity = null;

        if (string.Equals(expectedMeter.MeterType, "ammeter", StringComparison.OrdinalIgnoreCase))
        {
            if (!string.Equals(submitted.MeterTargetBranchId, expectedMeter.TargetBranchId, StringComparison.OrdinalIgnoreCase))
            {
                incorrectPlacement = true;
            }
            else if (expectedMeter.RequirePolarity == true)
            {
                incorrectPolarity = !string.Equals(submitted.MeterPositiveTerminalId, expectedMeter.PositiveTerminalId, StringComparison.OrdinalIgnoreCase)
                                     || !string.Equals(submitted.MeterNegativeTerminalId, expectedMeter.NegativeTerminalId, StringComparison.OrdinalIgnoreCase);
            }
        }
        else if (string.Equals(expectedMeter.MeterType, "voltmeter", StringComparison.OrdinalIgnoreCase))
        {
            var expNodes = expectedMeter.TargetNodeIds ?? Array.Empty<string>();
            var subNodes = submitted.MeterTargetNodeIds ?? Array.Empty<string>();

            var expNodeSet = expNodes.ToHashSet(StringComparer.OrdinalIgnoreCase);
            var subNodeSet = subNodes.ToHashSet(StringComparer.OrdinalIgnoreCase);

            if (expNodeSet.Count != 2 || subNodeSet.Count != 2 || !expNodeSet.SetEquals(subNodeSet))
            {
                incorrectPlacement = true;
            }
            else if (expectedMeter.RequirePolarity == true)
            {
                incorrectPolarity = !string.Equals(submitted.MeterPositiveTerminalId, expectedMeter.PositiveTerminalId, StringComparison.OrdinalIgnoreCase)
                                     || !string.Equals(submitted.MeterNegativeTerminalId, expectedMeter.NegativeTerminalId, StringComparison.OrdinalIgnoreCase);
            }
        }

        bool isCorrect = !incorrectPlacement && (incorrectPolarity != true);
        string expectedText = string.Equals(expectedMeter.MeterType, "ammeter", StringComparison.OrdinalIgnoreCase)
            ? $"Ammeter on branch {expectedMeter.TargetBranchId}"
            : $"Voltmeter across nodes {string.Join("-", expectedMeter.TargetNodeIds ?? Array.Empty<string>())}";

        var highlightTargets = new List<string>();
        if (expectedMeter.TargetBranchId != null) highlightTargets.Add(expectedMeter.TargetBranchId);
        if (expectedMeter.TargetNodeIds != null) highlightTargets.AddRange(expectedMeter.TargetNodeIds);

        return new AnswerEvaluation(question.Id, isCorrect, question.Explanation, expectedText)
        {
            CircuitFeedback = new CircuitFeedback(
                Array.Empty<string>(), Array.Empty<string>(), Array.Empty<string>(),
                Array.Empty<string>(), Array.Empty<string>(), Array.Empty<string>(),
                incorrectPlacement, incorrectPolarity, new Dictionary<string, string>(), highlightTargets)
        };
    }

    private async Task<AnswerEvaluation> ScoreValueEntryModeAsync(
        QuestionDefinition question,
        CircuitAnswerDefinition expected,
        SubmittedCircuitAnswer submitted,
        CancellationToken cancellationToken)
    {
        var expectedValues = expected.ExpectedValues ?? new Dictionary<string, ExpectedValueDefinition>();
        var submittedValues = submitted.Values ?? new Dictionary<string, string>();

        var incorrectValues = new Dictionary<string, string>();
        var highlightTargets = expectedValues.Keys.ToList();

        foreach (var kv in expectedValues)
        {
            var targetId = kv.Key;
            var expectedDef = kv.Value;

            if (!submittedValues.TryGetValue(targetId, out var subVal) || string.IsNullOrWhiteSpace(subVal))
            {
                incorrectValues[targetId] = "Missing value";
                continue;
            }

            subVal = subVal.Trim();

            if (string.Equals(expectedDef.Mode, "text", StringComparison.OrdinalIgnoreCase))
            {
                var expText = expectedDef.ExpectedText?.Trim() ?? string.Empty;
                if (!string.Equals(subVal, expText, StringComparison.OrdinalIgnoreCase))
                {
                    incorrectValues[targetId] = $"Expected '{expText}'";
                }
            }
            else if (string.Equals(expectedDef.Mode, "numeric", StringComparison.OrdinalIgnoreCase))
            {
                if (!decimal.TryParse(subVal, out var parsedSub) || expectedDef.NumericValue is null)
                {
                    incorrectValues[targetId] = "Invalid number";
                }
                else
                {
                    var diff = Math.Abs(parsedSub - expectedDef.NumericValue.Value);
                    var tol = expectedDef.NumericTolerance ?? 0m;
                    if (diff > tol)
                    {
                        incorrectValues[targetId] = $"Expected {expectedDef.NumericValue.Value} (±{tol})";
                    }
                }
            }
            else if (string.Equals(expectedDef.Mode, "symbolic", StringComparison.OrdinalIgnoreCase))
            {
                var expLatex = expectedDef.SymbolicExpectedLatex?.Trim() ?? string.Empty;
                var mode = expectedDef.SymbolicEquivalenceMode ?? "expression";
                var vars = expectedDef.SymbolicVariables ?? new List<string> { "x" };
                var tol = expectedDef.SymbolicTolerance ?? 0.000001m;

                var result = await mathEngine.CompareAsync(
                    new SymbolicComparisonRequest(subVal, expLatex, mode, vars, tol),
                    cancellationToken);

                if (!result.IsEquivalent)
                {
                    incorrectValues[targetId] = result.Reason ?? "Not equivalent expression";
                }
            }
        }

        bool isCorrect = incorrectValues.Count == 0;
        string expectedText = string.Join(", ", expectedValues.Select(kv => $"{kv.Key}={kv.Value.ExpectedText ?? kv.Value.NumericValue?.ToString() ?? kv.Value.SymbolicExpectedLatex}"));

        return new AnswerEvaluation(question.Id, isCorrect, question.Explanation, expectedText)
        {
            CircuitFeedback = new CircuitFeedback(
                Array.Empty<string>(), Array.Empty<string>(), Array.Empty<string>(),
                Array.Empty<string>(), Array.Empty<string>(), Array.Empty<string>(),
                null, null, incorrectValues, highlightTargets)
        };
    }

    private static AnswerEvaluation ScoreBuildMode(QuestionDefinition question, CircuitAnswerDefinition expected, SubmittedCircuitAnswer submitted)
    {
        var expectedTopology = expected.Topology;
        if (expectedTopology is null)
        {
            return new AnswerEvaluation(question.Id, false, question.Explanation, "No expected topology defined.");
        }

        var expectedDiagram = question.CircuitQuestion?.Diagram;
        var submittedDiagram = submitted.BuiltDiagram;

        if (expectedDiagram is null)
        {
            return new AnswerEvaluation(question.Id, false, question.Explanation, "No reference expected diagram defined.");
        }

        if (submittedDiagram is null)
        {
            return new AnswerEvaluation(question.Id, false, question.Explanation, "No diagram submitted.");
        }

        // Compare component counts by Symbol ID
        var expCounts = expectedTopology.RequiredComponents.ToDictionary(rc => rc.SymbolId, rc => rc.Count, StringComparer.OrdinalIgnoreCase);
        var subCounts = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);
        foreach (var comp in submittedDiagram.Components)
        {
            var sym = comp.SymbolId;
            if (subCounts.ContainsKey(sym)) subCounts[sym]++;
            else subCounts[sym] = 1;
        }

        var missingComponents = new List<string>();
        var extraComponents = new List<string>();
        var incorrectComponentTypes = new List<string>();

        foreach (var kv in expCounts)
        {
            var symbolId = kv.Key;
            var reqCount = kv.Value;
            var actCount = subCounts.TryGetValue(symbolId, out var count) ? count : 0;

            if (actCount < reqCount)
            {
                missingComponents.Add($"{symbolId} (Missing {reqCount - actCount})");
            }
        }

        foreach (var kv in subCounts)
        {
            var symbolId = kv.Key;
            var actCount = kv.Value;
            var reqCount = expCounts.TryGetValue(symbolId, out var count) ? count : 0;

            if (actCount > reqCount)
            {
                extraComponents.Add($"{symbolId} (Extra {actCount - reqCount})");
            }
        }

        if (missingComponents.Count > 0 || extraComponents.Count > 0)
        {
            return new AnswerEvaluation(question.Id, false, question.Explanation, "Component counts do not match expected topology.")
            {
                CircuitFeedback = new CircuitFeedback(
                    missingComponents, extraComponents, incorrectComponentTypes,
                    Array.Empty<string>(), Array.Empty<string>(), Array.Empty<string>(),
                    null, null, new Dictionary<string, string>(), Array.Empty<string>())
            };
        }

        // Perform Isomorphism check
        bool isomorphic = CheckIsomorphism(expectedDiagram, submittedDiagram);

        return new AnswerEvaluation(question.Id, isomorphic, question.Explanation, isomorphic ? "Correct topology." : "Incorrect circuit connections.")
        {
            CircuitFeedback = new CircuitFeedback(
                Array.Empty<string>(), Array.Empty<string>(), Array.Empty<string>(),
                isomorphic ? Array.Empty<string>() : new[] { "Connections do not match expected schematic." },
                Array.Empty<string>(), Array.Empty<string>(),
                null, null, new Dictionary<string, string>(), Array.Empty<string>())
        };
    }

    private static bool CheckIsomorphism(CircuitDiagramDefinition expected, CircuitDiagramDefinition submitted)
    {
        var expNets = GetNets(expected);
        var subNets = GetNets(submitted);

        var expComponents = expected.Components.ToList();
        var subComponents = submitted.Components.ToList();

        if (expComponents.Count != subComponents.Count) return false;

        // Group components by Symbol ID
        var symbolGroups = expComponents.Select(c => c.SymbolId).Distinct(StringComparer.OrdinalIgnoreCase).ToList();
        var expectedBySymbol = symbolGroups.ToDictionary(s => s, s => expComponents.Where(c => string.Equals(c.SymbolId, s, StringComparison.OrdinalIgnoreCase)).ToList(), StringComparer.OrdinalIgnoreCase);
        var submittedBySymbol = symbolGroups.ToDictionary(s => s, s => subComponents.Where(c => string.Equals(c.SymbolId, s, StringComparison.OrdinalIgnoreCase)).ToList(), StringComparer.OrdinalIgnoreCase);

        // Ensure symbols line up
        foreach (var sym in symbolGroups)
        {
            if (!submittedBySymbol.ContainsKey(sym) || expectedBySymbol[sym].Count != submittedBySymbol[sym].Count)
                return false;
        }

        var componentMapping = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase); // expectedId -> submittedId
        var terminalAssignments = new Dictionary<string, Dictionary<string, string>>(StringComparer.OrdinalIgnoreCase); // componentId -> (expectedTerminal -> submittedTerminal)

        return TryMatchGroups(0);

        bool TryMatchGroups(int groupIndex)
        {
            if (groupIndex == symbolGroups.Count)
            {
                // All components matched, verify nets
                return VerifyNetIsomorphism(expNets, subNets, componentMapping, terminalAssignments);
            }

            var symbol = symbolGroups[groupIndex];
            var expList = expectedBySymbol[symbol];
            var subList = submittedBySymbol[symbol];

            return TryPermutations(expList, subList, 0);

            bool TryPermutations(List<CircuitComponentInstance> exp, List<CircuitComponentInstance> sub, int index)
            {
                if (index == exp.Count)
                {
                    return TryMatchGroups(groupIndex + 1);
                }

                var expComp = exp[index];
                for (int i = 0; i < sub.Count; i++)
                {
                    var subComp = sub[i];
                    if (componentMapping.Values.Contains(subComp.Id)) continue; // Already mapped

                    // Check value/label match constraints if specified in expected
                    if (!string.IsNullOrEmpty(expComp.Value) && !string.Equals(expComp.Value, subComp.Value, StringComparison.OrdinalIgnoreCase))
                        continue;

                    // Map expected component to submitted component
                    componentMapping[expComp.Id] = subComp.Id;

                    // Set up terminal mappings (try both configurations if symmetric)
                    var termMap = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
                    terminalAssignments[expComp.Id] = termMap;

                    var terms = GetTerminalsForSymbol(symbol);
                    if (IsSymmetricSymbol(symbol) && terms.Count == 2)
                    {
                        // Try mapping 1: p1 -> p1, p2 -> p2
                        termMap[terms[0]] = terms[0];
                        termMap[terms[1]] = terms[1];
                        if (TryPermutations(exp, sub, index + 1)) return true;

                        // Try mapping 2: p1 -> p2, p2 -> p1
                        termMap[terms[0]] = terms[1];
                        termMap[terms[1]] = terms[0];
                        if (TryPermutations(exp, sub, index + 1)) return true;
                    }
                    else
                    {
                        // Non-symmetric or simple component
                        foreach (var term in terms)
                        {
                            termMap[term] = term;
                        }
                        if (TryPermutations(exp, sub, index + 1)) return true;
                    }

                    // Backtrack
                    componentMapping.Remove(expComp.Id);
                    terminalAssignments.Remove(expComp.Id);
                }

                return false;
            }
        }
    }

    private static bool VerifyNetIsomorphism(
        List<HashSet<string>> expNets,
        List<HashSet<string>> subNets,
        Dictionary<string, string> componentMapping,
        Dictionary<string, Dictionary<string, string>> terminalAssignments)
    {
        // Filter out nets to only keep component terminals
        var expFilteredNets = expNets.Select(net => FilterComponentTerminals(net)).Where(net => net.Count > 0).ToList();
        var subFilteredNets = subNets.Select(net => FilterComponentTerminals(net)).Where(net => net.Count > 0).ToList();

        if (expFilteredNets.Count != subFilteredNets.Count) return false;

        // Try to match each expected net to a submitted net
        var matchedSubNets = new HashSet<int>();

        foreach (var expNet in expFilteredNets)
        {
            // Map the expected terminals in this net
            var mappedTerminals = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            foreach (var term in expNet)
            {
                var dotIndex = term.IndexOf('.');
                var compId = term.Substring(0, dotIndex);
                var termId = term.Substring(dotIndex + 1);

                if (!componentMapping.TryGetValue(compId, out var subCompId)) return false;
                var subTermId = terminalAssignments[compId][termId];

                mappedTerminals.Add($"{subCompId}.{subTermId}");
            }

            // Find matching submitted net
            bool foundMatch = false;
            for (int i = 0; i < subFilteredNets.Count; i++)
            {
                if (matchedSubNets.Contains(i)) continue;
                if (subFilteredNets[i].SetEquals(mappedTerminals))
                {
                    matchedSubNets.Add(i);
                    foundMatch = true;
                    break;
                }
            }

            if (!foundMatch) return false;
        }

        return true;
    }

    private static HashSet<string> FilterComponentTerminals(HashSet<string> net)
    {
        // Keep only terminals with component format (e.g. R1.p1) and ignore explicit node IDs
        return net.Where(t => t.Contains('.')).ToHashSet(StringComparer.OrdinalIgnoreCase);
    }

    private static List<HashSet<string>> GetNets(CircuitDiagramDefinition diagram)
    {
        // Union-Find implementation to find connected nets of component terminals and nodes
        var parent = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);

        string Find(string node)
        {
            if (!parent.ContainsKey(node)) parent[node] = node;
            if (parent[node] == node) return node;
            return parent[node] = Find(parent[node]);
        }

        void Union(string node1, string node2)
        {
            var r1 = Find(node1);
            var r2 = Find(node2);
            if (r1 != r2)
            {
                parent[r1] = r2;
            }
        }

        // Initialize component terminals and nodes
        foreach (var comp in diagram.Components)
        {
            var terms = GetTerminalsForSymbol(comp.SymbolId);
            foreach (var term in terms)
            {
                var termRef = $"{comp.Id}.{term}";
                parent[termRef] = termRef;
            }
        }

        foreach (var node in diagram.Nodes)
        {
            parent[node.Id] = node.Id;
        }

        // Union along wires
        foreach (var wire in diagram.Wires)
        {
            Union(wire.SourceId, wire.TargetId);
        }

        // Group into sets
        var groups = new Dictionary<string, HashSet<string>>(StringComparer.OrdinalIgnoreCase);
        foreach (var key in parent.Keys)
        {
            var root = Find(key);
            if (!groups.ContainsKey(root))
            {
                groups[root] = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            }
            groups[root].Add(key);
        }

        return groups.Values.ToList();
    }

    private static List<string> GetTerminalsForSymbol(string symbolId)
    {
        var sym = symbolId.ToLowerInvariant();
        if (sym.StartsWith("ground") || sym.Contains("ground"))
        {
            return new List<string> { "p1" };
        }
        if (sym.Contains("npn") || sym.Contains("pnp") || sym.Contains("bjt") || sym.Contains("transistor"))
        {
            return new List<string> { "b", "c", "e" };
        }
        if (sym.Contains("opamp") || sym.Contains("amp"))
        {
            return new List<string> { "in_pos", "in_neg", "out" };
        }
        if (sym.Contains("gate.and") || sym.Contains("gate.or") || sym.Contains("gate.nand") || sym.Contains("gate.nor") || sym.Contains("gate.xor") || sym.Contains("gate.xnor") || sym.Contains("and") || sym.Contains("or") || sym.Contains("nand") || sym.Contains("nor") || sym.Contains("xor") || sym.Contains("xnor"))
        {
            return new List<string> { "in1", "in2", "out" };
        }
        if (sym.Contains("gate.not") || sym.Contains("not"))
        {
            return new List<string> { "in", "out" };
        }

        // Default 2 terminals for resistors, sources, capacitors, diodes, meters, switches
        return new List<string> { "p1", "p2" };
    }

    private static bool IsSymmetricSymbol(string symbolId)
    {
        var sym = symbolId.ToLowerInvariant();
        return sym.Contains("resistor") || sym.Contains("switch") || (sym.Contains("capacitor") && !sym.Contains("polarized")) || sym.Contains("lamp") || sym.Contains("fuse");
    }
}
