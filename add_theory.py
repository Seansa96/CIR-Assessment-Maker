import glob, re

files = glob.glob('data/assessments/csharp-*.yaml')
csharp = [f.split('\\')[-1].replace('.yaml', '') for f in files]

files = glob.glob('data/assessments/python-*.yaml')
python = [f.split('\\')[-1].replace('.yaml', '') for f in files]

with open('backend/tests/QuizApp.Tests/FileAssessmentRepositoryTests.cs', 'r') as f:
    content = f.read()

csharp_data = '\n    '.join(f'[InlineData("{id}")]' for id in csharp)
python_data = '\n    '.join(f'[InlineData("{id}")]' for id in python)

csharp_test = f"""    [Theory]
    {csharp_data}
    public async Task Repository_validates_csharp_gaming_assessments(string assessmentId)
    {{
        var repository = new FileAssessmentRepository(
            new FileStorageOptions {{ DataRoot = FindRepositoryDataRoot() }},
            new AssessmentValidator());

        var validation = await repository.ValidateFileAsync($"{{assessmentId}}.yaml");

        Assert.True(validation.IsValid, string.Join("; ", validation.Issues.Select(issue => issue.Message)));
    }}"""

python_test = f"""    [Theory]
    {python_data}
    public async Task Repository_validates_python_gaming_assessments(string assessmentId)
    {{
        var repository = new FileAssessmentRepository(
            new FileStorageOptions {{ DataRoot = FindRepositoryDataRoot() }},
            new AssessmentValidator());

        var validation = await repository.ValidateFileAsync($"{{assessmentId}}.yaml");

        Assert.True(validation.IsValid, string.Join("; ", validation.Issues.Select(issue => issue.Message)));
    }}"""

if 'Repository_validates_csharp_gaming_assessments' not in content:
    content = content.replace('    private static string CreateDataRoot()', csharp_test + '\n\n' + python_test + '\n\n    private static string CreateDataRoot()')
    with open('backend/tests/QuizApp.Tests/FileAssessmentRepositoryTests.cs', 'w') as f:
        f.write(content)
