from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "assessments"


class LiteralString(str):
    pass


class Dumper(yaml.SafeDumper):
    pass


Dumper.add_representer(
    LiteralString,
    lambda dumper, value: dumper.represent_scalar(
        "tag:yaml.org,2002:str", value, style="|"
    ),
)


def mc(source, skill, prompt, choices, correct, explanation):
    return {
        "sourceFamilyId": source,
        "skills": [skill],
        "type": "multipleChoice",
        "prompt": LiteralString(prompt),
        "choices": [
            {"id": chr(ord("a") + i), "text": text}
            for i, text in enumerate(choices)
        ],
        "answer": {"choiceId": correct},
        "explanation": LiteralString(explanation),
    }


def select_all(source, skill, prompt, choices, correct, explanation):
    item = mc(source, skill, prompt, choices, "a", explanation)
    item["type"] = "selectAll"
    item["answer"] = {"choiceIds": correct}
    return item


STRING_QUIZ = [
    mc("cpp-fsf-string-001", "reverse-string-content",
       "Which standard-library call reverses every byte in a mutable `std::string text`?",
       ["`std::reverse(text.begin(), text.end());`", "`std::sort(text.begin(), text.end());`", "`text.erase(text.begin());`", "`std::rotate(text.begin(), text.end(), text.begin());`"],
       "a", "`std::reverse` operates on the complete half-open range and runs in linear time."),
    mc("cpp-fsf-string-002", "transform-ascii-letters",
       "The successor transform must preserve case and wrap alphabet endpoints. What should `Zaz-9` become?",
       ["`Aba-9`", "`[b{-9`", "`Aba-0`", "`Zba-9`"],
       "a", "`Z` wraps to `A`, `a` advances to `b`, `z` wraps to `a`, and nonletters remain unchanged."),
    mc("cpp-fsf-string-005", "sort-string-characters",
       "Given the lowercase-only contract, what does sorting `baba` with `std::sort` produce?",
       ["`abab`", "`aabb`", "`bbaa`", "`baba`"],
       "b", "Lowercase ASCII byte order is alphabetic, so both `a` values precede both `b` values."),
    mc("cpp-fsf-string-006", "scan-fixed-distance-patterns",
       "If exactly two characters must occur between `e` and `g`, what index offset should the scan compare?",
       ["1", "2", "3", "4"],
       "c", "Positions `i` and `i + 3` have two intervening positions."),
    mc("cpp-fsf-string-007", "count-vowels",
       "Under a case-insensitive `a e i o u` policy, how many vowels are in `USA rhythm`?",
       ["2", "3", "4", "5"],
       "b", "`U` and `A` are vowels and `rhythm` contributes none because `y` is excluded."),
    mc("cpp-fsf-string-008", "count-whitespace-delimited-words",
       "Which event should increment a maximal-nonwhitespace word counter?",
       ["Every whitespace byte", "Every nonwhitespace byte", "A transition from whitespace to nonwhitespace", "A transition from nonwhitespace to whitespace only"],
       "c", "Counting entry transitions handles leading, trailing, and repeated whitespace without empty tokens."),
    mc("cpp-fsf-string-009", "compare-character-frequencies",
       "What should `equal_occurrences(\"xyz\", 'a', 'b')` return?",
       ["false, because neither appears", "true, because both counts are zero", "false, because the string is nonempty", "The result is undefined"],
       "b", "The contract compares counts, and zero equals zero."),
    mc("cpp-fsf-string-010", "recognize-palindromes",
       "With exact case-sensitive comparison, which input is a palindrome?",
       ["`Madam`", "`race car`", "`level`", "`abca`"],
       "c", "`level` matches at every symmetric pair; case and spaces invalidate the other near-palindromes."),
    mc("cpp-fsf-string-013", "toggle-letter-case",
       "Why should case toggling use `if ... else if` rather than two independent case tests?",
       ["To sort letters first", "To avoid converting a letter and immediately converting it back", "To remove punctuation", "To allocate the output"],
       "b", "After a lowercase letter is uppercased, a second independent uppercase test could undo the change."),
    select_all("cpp-fsf-string-021", "recognize-subsequences",
       "Which strings are subsequences of `apple`? Select all that apply.",
       ["`apl`", "`ppe`", "`ale`", "`pae`"],
       ["a", "b", "c"], "The first three preserve left-to-right order; `pae` asks for `a` after the initial `p`, which is impossible."),
    mc("cpp-fsf-string-022", "filter-special-characters",
       "Which positive predicate implements “keep letters, digits, and whitespace”?",
       ["`isalnum(u) || isspace(u)`", "`ispunct(u)`", "`isalpha(u) && isdigit(u)`", "`!isspace(u)`"],
       "a", "A byte is retained when it belongs to either the alphanumeric or whitespace category."),
    mc("cpp-fsf-string-025", "find-longest-run",
       "Where should a longest-ones scan update its maximum so a run ending at the last byte is counted?",
       ["Only when a zero is read", "Whenever a one extends the current run", "Only after the loop if input ends in zero", "Before resetting the input"],
       "b", "Updating at each extension records terminal runs without a special flush."),
    mc("cpp-fsf-string-030", "detect-missing-sequence-letter",
       "Under the one-gap precondition, what does `missing_lowercase_letter(\"abdef\")` return?",
       ["`b`", "`c`", "`d`", "no value"],
       "b", "The first failed successor relation is `b` followed by `d`, so `c` is missing."),
    mc("cpp-fsf-string-036", "detect-adjacent-equality",
       "Why is a frequency table the wrong primary structure for detecting adjacent identical letters?",
       ["It cannot count letters", "It discards occurrence positions and adjacency", "It is always exponential", "It changes character case"],
       "b", "A letter may repeat far apart; adjacency requires comparing neighboring positions."),
    mc("cpp-fsf-string-037", "count-specific-characters",
       "What is the result of counting lowercase `'a'` in `\"Aa a\"` under an exact case-sensitive contract?",
       ["1", "2", "3", "4"],
       "b", "The lowercase target occurs at indices 1 and 3; uppercase `A` is different."),
]


STRING_TEST = [
    mc("cpp-fsf-string-004", "select-longest-token",
       "Words are maximal ASCII-letter runs and ties keep the first. What is returned for `one, three! seven`?",
       ["`one`", "`three`", "`seven`", "`three!`"],
       "b", "`three` and `seven` both have length five, so strict improvement preserves the first."),
    mc("cpp-fsf-string-014", "parse-embedded-integers",
       "What sum is produced from `v2 has 10 fixes and 003 tests` when maximal digit runs are integers?",
       ["15", "18", "210003", "6"],
       "a", "The parsed runs are 2, 10, and 3, whose sum is 15."),
    mc("cpp-fsf-string-015", "format-integers-as-english",
       "Why is an integer-to-English formatter naturally decomposed into groups below one thousand?",
       ["Every three decimal digits reuse the same hundreds/tens/ones rules", "C++ strings have a three-byte limit", "English never names zero", "It avoids all lookup tables"],
       "a", "Million, thousand, and units groups share one sub-thousand formatter plus a scale name."),
    mc("cpp-fsf-string-016", "find-common-prefix",
       "Which condition must be checked before reading `word[length]` during a vertical prefix scan?",
       ["`length < word.size()`", "`word.size() < words.size()`", "`length != 0`", "`word[length] != '\\0'` only"],
       "a", "A shorter word may end before the current prefix position, so the index must be bounded first."),
    mc("cpp-fsf-string-018", "find-longest-valid-parentheses",
       "In the unmatched-index stack method, what does the initial sentinel `-1` represent?",
       ["A fake opening parenthesis", "The boundary immediately before a valid prefix beginning at zero", "The number of pairs", "An invalid character"],
       "b", "Distance from the sentinel to a closing index gives a valid prefix length."),
    mc("cpp-fsf-string-023", "compute-character-set-union",
       "Two strings have 6 and 5 distinct bytes, with 3 shared. How many distinct bytes are in their union?",
       ["8", "11", "3", "14"],
       "a", "Union size is 6 + 5 - 3 = 8."),
    mc("cpp-fsf-string-024", "count-duplicated-character-values",
       "What is `duplicate_byte_count(\"aaaaabbc\")`?",
       ["2", "5", "6", "1"],
       "a", "Only byte values `a` and `b` occur at least twice; multiplicity beyond two does not add another value."),
    mc("cpp-fsf-string-026", "validate-title-case",
       "Under the rule “uppercase first letter, lowercase remaining letters,” which input passes?",
       ["`The Quick Brown Fox.`", "`The quick Brown Fox.`", "`NASA Mission`", "`123`"],
       "a", "Every letter run in the first option follows the required case pattern and at least one word exists."),
    mc("cpp-fsf-string-027", "split-camel-case",
       "What should lower-to-upper boundary splitting do with `XMLParser`?",
       ["`X M L Parser`", "`XML Parser`", "`XMLParser`", "`XM LParser`"],
       "c", "The `P` follows uppercase `L`, not a lowercase byte, so this specific contract inserts no space."),
    mc("cpp-fsf-string-028", "extract-first-matches",
       "When should `first_vowels(text, count)` return `nullopt`?",
       ["Whenever more vowels exist than requested", "When fewer vowels exist than requested", "Whenever count is zero", "When the first byte is a consonant"],
       "b", "Failure represents insufficient matching data, not unused extra vowels."),
    mc("cpp-fsf-string-029", "format-decimal-thousands",
       "Why is `std::to_string(value)` safer than first taking `abs(value)` in a signed thousands formatter?",
       ["It handles the most-negative signed value without overflowing its positive counterpart", "It sorts digits", "It removes the sign", "It changes the locale"],
       "a", "The positive magnitude of the minimum signed value is not representable in the same signed type."),
    select_all("cpp-fsf-string-031", "validate-uniform-letter-case",
       "Which inputs satisfy the nonempty, letters-only, uniform-case contract? Select all that apply.",
       ["`ABC`", "`abc`", "`Abc`", "`ABC1`"],
       ["a", "b"], "All-uppercase and all-lowercase letter strings pass; mixed case and nonletters fail."),
    mc("cpp-fsf-string-033", "test-multiset-containment",
       "Why does a set give the wrong answer for `can_construct_from(\"a\", \"aa\")`?",
       ["It ignores case", "It records membership but not the number of available copies", "It preserves order", "It cannot store `a`"],
       "b", "Constructibility is multiset containment, so multiplicity must be consumed."),
    mc("cpp-fsf-string-034", "remove-first-substring",
       "What must happen before calling `erase(pos, target.size())`?",
       ["Verify `pos != npos`", "Sort the string", "Append the target", "Convert the target to uppercase"],
       "a", "Passing `npos` as an erase position is out of range."),
    mc("cpp-fsf-string-035", "transform-odd-length-words",
       "Why must punctuation be excluded before testing a word's length parity?",
       ["Including it can change odd to even or even to odd", "Punctuation is always uppercase", "It prevents iteration", "It forces a file read"],
       "a", "The word definition controls the interval length and therefore the reversal decision."),
    mc("cpp-fsf-string-038", "remove-matching-characters",
       "After `std::remove`, why is `erase` still required?",
       ["`remove` returns a logical end but does not shrink the string", "`remove` deletes the entire string", "`erase` sorts retained bytes", "`erase` changes case"],
       "a", "The obsolete tail remains physically present until the container erases it."),
    mc("cpp-fsf-string-039", "validate-character-uniqueness",
       "Why should a byte be converted to `unsigned char` before indexing a 256-entry table?",
       ["Plain `char` may be negative", "Unsigned values are alphabetic", "It makes the table dynamic", "It removes duplicates"],
       "a", "On implementations with signed `char`, high-bit bytes otherwise produce negative indices."),
    mc("cpp-fsf-string-040", "select-by-parallel-string-mask",
       "What does `select_where_first_is_lower(\"Java\", \"jscript\")` return?",
       ["`Java`", "`jav`", "`scr`", "`jsc`"],
       "c", "Lowercase mask positions 1, 2, and 3 select `s`, `c`, and `r` from the value string."),
    mc("cpp-fsf-string-042", "alternate-letter-case",
       "What should `alternating_ascii_case(\"A-BC\")` return when punctuation does not advance the pattern?",
       ["`a-bC`", "`a-Bc`", "`A-bC`", "`a-bc`"],
       "b", "Letters receive lower, upper, lower in sequence; the hyphen is preserved and does not toggle state."),
]


FILE_QUIZ = [
    mc("cpp-fsf-file-002", "read-complete-file-content", "Which operation preserves whitespace while reading every file byte?", ["Construct a string from `istreambuf_iterator<char>`", "Use one `operator>>` extraction", "Call `getline` once", "Check `eof()` before opening"], "a", "Stream-buffer iterators copy raw stream characters without formatted whitespace skipping."),
    mc("cpp-fsf-file-002", "distinguish-empty-files", "How should a successful read of an empty file differ from an open failure?", ["Both return an empty string", "Empty success returns an engaged empty string; failure returns `nullopt`", "Both return `nullopt`", "Failure returns one newline"], "b", "`optional` separates absence caused by failure from valid empty content."),
    mc("cpp-fsf-file-002", "interpret-stream-state", "After reading a complete file to its natural end, which state indicates a genuine low-level read failure?", ["`eof()`", "`bad()`", "`is_open()`", "`tellg() == 0`"], "b", "EOF is expected; `bad()` signals a serious I/O error."),
    mc("cpp-fsf-file-002", "select-binary-mode", "Why open a whole-file byte reader with `std::ios::binary`?", ["To prevent platform text translation", "To encrypt the file", "To sort its lines", "To ignore null bytes"], "a", "Binary mode preserves the stored byte sequence, including line endings."),
    select_all("cpp-fsf-file-002", "avoid-formatted-file-reading", "Which approaches can preserve embedded whitespace across the whole file? Select all that apply.", ["Stream-buffer iterators", "Repeated `read` into a byte buffer", "A single formatted `operator>>`", "Reading only `input.peek()`"], ["a", "b"], "Raw iterators and unformatted reads preserve whitespace; formatted token extraction does not."),
    mc("cpp-fsf-file-004", "count-file-words", "For maximal alphanumeric runs, how many words are in `don't stop`?", ["2", "3", "4", "1"], "b", "The apostrophe delimits `don` and `t`, followed by `stop`."),
    mc("cpp-fsf-file-004", "track-word-state", "What event increments a streamed word counter?", ["Every alphanumeric byte", "Transition from delimiter to alphanumeric", "Every newline only", "Transition from alphanumeric to alphanumeric"], "b", "A maximal run begins exactly at a delimiter-to-word transition."),
    mc("cpp-fsf-file-004", "use-cctype-safely", "What value should be passed to `std::isalnum` for a stored `char ch`?", ["`static_cast<unsigned char>(ch)`", "`-ch`", "`ch + 256` unconditionally", "`&ch`"], "a", "The cctype contract requires EOF or an unsigned-char-representable value."),
    mc("cpp-fsf-file-004", "stream-large-files", "Why count words as bytes are read instead of loading the full file?", ["It bounds auxiliary memory", "It changes punctuation into spaces", "It guarantees Unicode support", "It prevents EOF"], "a", "Only the current boundary state and count are required."),
    mc("cpp-fsf-file-004", "preserve-state-across-lines", "If a word definition treats only alphanumeric bytes as word characters, what does a newline do?", ["Continues the word", "Ends the current word", "Adds two words", "Causes an I/O error"], "b", "A newline is a delimiter under the stated predicate."),
    mc("cpp-fsf-file-008", "sort-file-lines", "Which container is appropriate when all lines must be sorted with `std::sort`?", ["`std::vector<std::string>`", "`std::ofstream` alone", "`std::optional<char>`", "A single `char`"], "a", "Sorting needs random access to the materialized line values."),
    mc("cpp-fsf-file-008", "understand-getline", "What happens to line delimiters when lines are read with `std::getline`?", ["They become part of each string", "They are extracted but not stored in the string", "They are duplicated", "They are sorted"], "b", "A rewrite must define how delimiters are restored because `getline` removes them."),
    mc("cpp-fsf-file-008", "preserve-duplicate-lines", "Should sorting discard duplicate or empty lines?", ["Yes, sorting implies uniqueness", "No, ordinary sorting reorders but preserves elements", "Only duplicates are preserved", "Only empty lines are preserved"], "b", "Unless deduplication is explicitly requested, every input line remains an output line."),
    mc("cpp-fsf-file-008", "reason-about-string-order", "Under ordinary case-sensitive `std::string` ordering, which generally sorts first in ASCII?", ["Lowercase `a`", "Uppercase `A`", "They are always equal", "The longer string regardless of prefix"], "b", "Uppercase ASCII letters have lower byte values than lowercase letters."),
    mc("cpp-fsf-file-008", "define-output-newlines", "Why must a sorted-line exercise state its output newline policy?", ["`getline` discarded the original delimiters", "Sorting cannot compare strings", "Newlines are numbers", "Binary mode adds commas"], "a", "The program must deliberately choose whether and how to reconstruct line endings."),
]


FILE_TEST = [
    mc("cpp-fsf-file-012", "normalize-caesar-shifts", "Which expression normalizes any integer shift into `0..25`?", ["`((shift % 26) + 26) % 26`", "`shift / 26`", "`shift & 26`", "`26 - shift`"], "a", "The second modulo handles both large and negative inputs."),
    mc("cpp-fsf-file-012", "trace-caesar-encryption", "With shift 3, what does `Az-z!` encrypt to?", ["`Dc-c!`", "`Cz-b!`", "`Da-a!`", "`Dc-c$`"], "a", "Both cases wrap independently and punctuation remains unchanged."),
    mc("cpp-fsf-file-012", "preserve-caesar-nonletters", "Which bytes should a letter-only Caesar cipher leave unchanged?", ["Digits, punctuation, whitespace, and line endings", "Lowercase letters", "Uppercase letters", "Only null bytes"], "a", "The transform applies only to ASCII letter ranges."),
    select_all("cpp-fsf-file-012", "verify-caesar-file-output", "Which checks are required before reporting successful file encryption? Select all that apply.", ["The source did not enter `bad()`", "The destination remains healthy after flush", "The shift is positive", "The file contains at least one letter"], ["a", "b"], "I/O health determines success; zero/negative shifts and letter-free files remain valid."),
    mc("cpp-fsf-file-012", "stream-caesar-files", "What memory advantage comes from transforming one byte at a time?", ["Auxiliary memory remains constant", "Time becomes constant", "The output needs no file", "Modulo is avoided"], "a", "The algorithm does not retain the entire file."),
    mc("cpp-fsf-file-013", "invert-caesar-shifts", "How is decryption related to encryption modulo 26?", ["Use the additive inverse of the encryption shift", "Use the same positive direction twice", "Reverse the file bytes", "Toggle letter case"], "a", "Adding `-shift` modulo 26 undoes adding `shift`."),
    mc("cpp-fsf-file-013", "avoid-negative-remainders", "Why normalize before applying a negative decryption shift in C++?", ["The `%` result can remain negative", "Modulo works only on strings", "Letters are unsigned", "It closes the stream"], "a", "A negative remainder can produce a byte before the alphabet base."),
    mc("cpp-fsf-file-013", "verify-caesar-round-trip", "Which property is the strongest basic verification?", ["Decrypting encrypted bytes with the same shift restores every original byte", "Encrypted size is nonzero", "Output contains uppercase letters", "The destination path differs in length"], "a", "The round trip tests both wrap directions and preservation of nonletters."),
    mc("cpp-fsf-file-013", "detect-wrong-caesar-key", "Text encrypted with shift 5 is decrypted with shift 4. What is expected for letters?", ["They remain shifted forward by 1", "They are fully restored", "They reverse order", "They all become `A`"], "a", "Net transformation is +5 - 4 = +1 modulo 26."),
    mc("cpp-fsf-file-013", "preserve-caesar-case", "How should encrypted lowercase input be decrypted?", ["Back to lowercase", "Always uppercase", "As punctuation", "Case is unspecified"], "a", "Lowercase and uppercase alphabets are transformed in separate ranges."),
    mc("cpp-fsf-file-014", "state-csv-dialect", "Why must the simple CSV task explicitly say quotes have no special meaning?", ["A full CSV parser must otherwise handle quoted commas and escaped quotes", "Quotes cannot be stored in strings", "Commas are whitespace", "It makes every row rectangular"], "a", "The limitation prevents a naive comma split from claiming complete CSV support."),
    mc("cpp-fsf-file-014", "preserve-empty-csv-fields", "How many fields are in the simple CSV row `a,,c,`?", ["2", "3", "4", "5"], "c", "The adjacent commas create an empty middle field and the trailing comma creates an empty final field."),
    mc("cpp-fsf-file-014", "compute-table-widths", "Why does aligned output require parsing all rows before rendering?", ["Each column width depends on the longest field anywhere in that column", "Output streams cannot write early", "Rows must be alphabetically sorted", "Commas have unknown byte values"], "a", "A later field may increase the padding needed by earlier rows."),
    mc("cpp-fsf-file-014", "understand-setw", "What is important about `std::setw` when printing several fields?", ["It applies only to the next formatted field", "It permanently changes every stream", "It changes the file encoding", "It removes empty strings"], "a", "Width must be supplied again for each padded column."),
    mc("cpp-fsf-file-014", "reject-ragged-csv", "What should the specified rectangular-table function do when one row has fewer fields?", ["Return `nullopt`", "Silently invent values", "Drop the row", "Merge it with the next row"], "a", "Inconsistent column counts violate the declared input contract."),
    mc("cpp-fsf-file-015", "validate-complete-number-tokens", "Why must parsing `12x` check how many characters `std::stod` consumed?", ["Without the check it may accept the numeric prefix 12", "It prevents all integers", "It converts the token to hexadecimal", "It detects file size"], "a", "Complete-token validation rejects trailing junk."),
    mc("cpp-fsf-file-015", "ignore-invalid-number-tokens", "What average results from `10 20 bad 30` when invalid tokens are ignored?", ["15", "20", "30", "No result"],
       "b", "The three valid values sum to 60 and divide by a valid count of three."),
    mc("cpp-fsf-file-015", "distinguish-zero-average", "Why return `optional<double>` rather than using zero for “no valid numbers”?", ["A legitimate collection can have average zero", "Zero is not a double", "Optional performs file I/O", "It rounds every value"], "a", "Absence and a computed numeric zero are different outcomes."),
    mc("cpp-fsf-file-015", "reduce-average-roundoff", "Why accumulate into `long double` before converting the final mean to `double`?", ["It can reduce intermediate rounding error", "It rejects negative values", "It makes parsing case-insensitive", "It counts tokens automatically"], "a", "Wider intermediate precision can retain more information across many additions."),
    mc("cpp-fsf-file-015", "handle-number-stream-failures", "After token extraction ends, which condition distinguishes an I/O failure from normal EOF?", ["`input.bad()`", "`input.eof()`", "`count > 0`", "`token.empty()`"], "a", "Normal EOF is expected, whereas bad state reports a serious read error."),
]


def assessment(assessment_id, title, assessment_type, topic, questions):
    goal = "practice" if assessment_type == "quiz" else "evaluate"
    activity = "focusedPractice" if assessment_type == "quiz" else "formalTest"
    for index, question in enumerate(questions, 1):
        question["id"] = f"q{index:03d}"
    return {
        "schemaVersion": 1,
        "id": assessment_id,
        "title": title,
        "description": f"A topic-specific {len(questions)}-question {assessment_type} sourced from the reviewed C++ problem bank.",
        "assessmentType": assessment_type,
        "categoryId": "c++",
        "topicId": topic,
        "skills": sorted({skill for q in questions for skill in q["skills"]}),
        "difficulty": 2 if assessment_type == "quiz" else 3,
        "modeDefault": goal,
        "randomizeQuestions": False,
        "navigation": {
            "learningGoal": goal,
            "activityType": activity,
            "tags": ["c++", topic, assessment_type, "problem-bank", activity],
        },
        "attemptQuestionCount": len(questions),
        "questions": questions,
    }


def main():
    definitions = [
        assessment("cpp-strings-formatting-quiz", "C++ Strings and Formatting Quiz", "quiz", "cpp-strings-formatting", STRING_QUIZ),
        assessment("cpp-strings-formatting-test", "C++ Strings and Formatting Test", "test", "cpp-strings-formatting", STRING_TEST),
        assessment("cpp-working-with-files-quiz", "C++ Working with Files Quiz", "quiz", "cpp-working-with-files", FILE_QUIZ),
        assessment("cpp-working-with-files-test", "C++ Working with Files Test", "test", "cpp-working-with-files", FILE_TEST),
    ]
    for document in definitions:
        path = OUT / f"{document['id']}.yaml"
        path.write_text(
            yaml.dump(document, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=110),
            encoding="utf-8",
        )
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
