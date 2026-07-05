using System.Text;
using System.Text.RegularExpressions;

namespace QuizApp.Infrastructure.Retention;

public static partial class SearchNormalizer
{
    private static readonly Regex PunctuationRegex = GeneratePunctuationRegex();

    [GeneratedRegex(@"[^\w\s\-\/]", RegexOptions.Compiled)]
    private static partial Regex GeneratePunctuationRegex();

    public static string Normalize(string? input)
    {
        if (string.IsNullOrWhiteSpace(input))
            return string.Empty;

        var lower = input.ToLowerInvariant().Trim();

        // Preserve math terms and IDs, replace other punctuation with space
        var noPunc = PunctuationRegex.Replace(lower, " ");

        // Collapse whitespace
        var collapsed = Regex.Replace(noPunc, @"\s+", " ");

        // Replace hyphens with space ONLY if it's not a common term like u-sub or part of an ID
        // For simplicity in v1, we split kebab/snake case but preserve common things if possible.
        // Actually, replacing all '-' and '_' with space makes tokenization very easy and matches SQLite unicode61.
        collapsed = collapsed.Replace('_', ' ').Replace('-', ' ').Replace('/', ' ');
        
        return Regex.Replace(collapsed, @"\s+", " ").Trim();
    }

    public static int BoundedLevenshteinDistance(string s, string t, int maxDistance)
    {
        if (string.IsNullOrEmpty(s)) return t?.Length ?? 0;
        if (string.IsNullOrEmpty(t)) return s.Length;

        if (s.Length > t.Length) (s, t) = (t, s);

        if (t.Length - s.Length > maxDistance) return maxDistance + 1;

        int[] v0 = new int[t.Length + 1];
        int[] v1 = new int[t.Length + 1];

        for (int i = 0; i <= t.Length; i++) v0[i] = i;

        for (int i = 0; i < s.Length; i++)
        {
            v1[0] = i + 1;
            int minDistance = v1[0];

            for (int j = 0; j < t.Length; j++)
            {
                int cost = (s[i] == t[j]) ? 0 : 1;
                v1[j + 1] = Math.Min(v1[j] + 1, Math.Min(v0[j + 1] + 1, v0[j] + cost));
                minDistance = Math.Min(minDistance, v1[j + 1]);
            }

            if (minDistance > maxDistance) return maxDistance + 1;

            var temp = v0;
            v0 = v1;
            v1 = temp;
        }

        return v0[t.Length];
    }
}
