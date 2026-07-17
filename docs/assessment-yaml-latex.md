# Assessment YAML LaTeX Authoring

Use this reference whenever creating or editing assessment YAML that contains LaTeX.

## Classification Contract

Every assessment has one authoritative placement:

```yaml
categoryId: calculus-2
topicId: convergence-tests
```

`topicId` must be a non-empty scalar declared by that category and mapped to exactly one same-category area in `data/areas.yaml`. Do not use `subcategoryId`, `subcategoryIds`, or multiple topics. `skills` and `navigation.tags` are searchable attribution only and cannot place an assessment in additional topics or areas. Create a dedicated review/capstone topic for genuinely cumulative content.

## Core Rule

Do not put LaTeX backslashes inside double-quoted YAML strings.

Double-quoted YAML treats backslashes as escape characters. LaTeX commands such as `\vec`, `\hat`, `\int`, `\frac`, `\sin`, `\tan`, and `\,dx` can therefore cause YamlDotNet parse errors.

## Preferred Formats

### Use block scalars for prompts, explanations, worked-example problems, and longer text

```yaml
prompt: |
  Evaluate the integral.

  $$
  \int \sin^3(x)\,dx
  $$
```

```yaml
explanation: |
  Save one $\sin x\,dx$ and rewrite the remaining even power:

  $$
  \sin^2 x = 1-\cos^2 x.
  $$

  Then use $u=\cos x$.
```

### Use single quotes for short inline LaTeX strings

```yaml
prompt: 'What is $\vec{A}+\vec{B}$?'
hint: 'Use $\hat{i}$ for $x$, $\hat{j}$ for $y$, and $\hat{k}$ for $z$.'
text: '$-\cos x+\frac{\cos^3 x}{3}+C$'
```

Single-quoted YAML strings preserve LaTeX backslashes literally.

## Avoid

Do not write this:

```yaml
prompt: "What is $\vec{A}+\vec{B}$?"
```

Do not write this:

```yaml
hint: "Use $\int \frac{1}{x+a}\,dx=\ln|x+a|+C$."
```

Those are likely to fail because YAML sees backslashes inside double quotes.

## Symbolic Response Answers

For `symbolicResponse`, prefer plain scalars or single quotes for `expectedLatex`.

Good:

```yaml
answer:
  expectedLatex: -\cos x+C
  equivalenceMode: derivative
  variables:
    - x
  tolerance: 0.000001
```

Also good when the expression is easier to read quoted:

```yaml
answer:
  expectedLatex: '\frac{x^3}{3}+C'
  equivalenceMode: derivative
  variables:
    - x
  tolerance: 0.000001
```

Avoid:

```yaml
answer:
  expectedLatex: "\frac{x^3}{3}+C"
```

## Choice Text

Choice text containing LaTeX should use single quotes:

```yaml
choices:
  - id: a
    text: '$u=\cos x$, $du=-\sin x\,dx$'
  - id: b
    text: '$u=\sin x$, $du=\cos x\,dx$'
```

If a choice needs multiple sentences or display math, use a block scalar:

```yaml
choices:
  - id: a
    text: |
      Use the identity

      $$
      \sin^2 x = 1-\cos^2 x.
      $$
```

## Apostrophes Inside Single Quotes

In single-quoted YAML strings, apostrophes must be doubled:

```yaml
hint: 'Don''t combine unlike vector components.'
```

For longer text with apostrophes, prefer a block scalar instead.

## Quick Check

After adding assessment YAML, scan for double-quoted strings that contain backslashes:

```powershell
$files = Get-ChildItem data\assessments\*.yaml
foreach ($file in $files) {
  $lineNumber = 0
  foreach ($line in Get-Content $file) {
    $lineNumber++
    if ($line -match '".*\\.*"') {
      [PSCustomObject]@{
        File = $file.Name
        Line = $lineNumber
        Text = $line.Trim()
      }
    }
  }
}
```

Any result is not automatically wrong, but it should be reviewed. If the line contains LaTeX, convert it to a block scalar or a single-quoted scalar.

## Practical Checklist

- Use `|` block scalars for multi-line prompts and explanations.
- Use single quotes for short inline LaTeX.
- Never use double quotes around LaTeX unless every backslash escape has been intentionally reviewed.
- Keep display math inside `$$ ... $$`.
- Keep inline math inside `$ ... $`.
- For YAML examples, copy formatting from existing integration assessments that already load successfully.
