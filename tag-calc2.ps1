$files = Get-ChildItem -Path "c:\Users\SeanS\Downloads\cir_app\data\assessments" -Filter "calc2-*.yaml"
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    
    $name = $file.Name
    $skill = ""
    if ($name -match '^calc2-(.+?)-(?:concept-lesson|quiz|worked-example|interactive|recall|test|exam|prediction|exploration|interactive-exploration)(?:-[a-z])?\.yaml$') {
        $skill = $matches[1]
    } else {
        $skill = $name -replace '^calc2-', '' -replace '\.yaml$', ''
    }
    
    # Top level injection
    if ($content -notmatch '(?m)^skills:') {
        if ($content -match '(?m)^modeDefault:') {
            $content = $content -replace '(?m)^modeDefault:', "skills:`n- $skill`nmodeDefault:"
        } elseif ($content -match '(?m)^randomizeQuestions:') {
            $content = $content -replace '(?m)^randomizeQuestions:', "skills:`n- $skill`nrandomizeQuestions:"
        } elseif ($content -match '(?m)^questions:') {
            $content = $content -replace '(?m)^questions:', "skills:`n- $skill`nquestions:"
        } elseif ($content -match '(?m)^items:') {
            $content = $content -replace '(?m)^items:', "skills:`n- $skill`nitems:"
        } elseif ($content -match '(?m)^workedExamples:') {
            $content = $content -replace '(?m)^workedExamples:', "skills:`n- $skill`nworkedExamples:"
        } elseif ($content -match '(?m)^lesson:') {
            $content = $content -replace '(?m)^lesson:', "skills:`n- $skill`nlession:"
        } elseif ($content -match '(?m)^exploration:') {
            $content = $content -replace '(?m)^exploration:', "skills:`n- $skill`nexploration:"
        }
    }
    
    # Question/Item level injection
    # Match type: <type> followed by newline, IF the next line is not skills:
    $regexSafe = '(?m)^(\s+)type:\s*(multipleChoice|selectAll|freeResponse|numericResponse|symbolicResponse|symbolic|code|circuit|multipart|typed|flashcard|cloze)\s*\r?\n(?!\1skills:)'
    $content = [System.Text.RegularExpressions.Regex]::Replace($content, $regexSafe, "`${1}type: `${2}`n`${1}skills:`n`${1}- $skill`n")
    
    Set-Content $file.FullName -Value $content
}
