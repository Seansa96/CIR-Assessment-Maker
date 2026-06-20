import { EditorView, basicSetup } from "codemirror";
import { keymap } from "@codemirror/view";
import { indentWithTab } from "@codemirror/commands";
import { python } from "@codemirror/lang-python";
import { cpp } from "@codemirror/lang-cpp";
import { autocompletion, CompletionContext, CompletionResult, snippetCompletion } from "@codemirror/autocomplete";

export interface ProjectFile {
  path: string;
  content: string;
}

export interface CodeEditorOptions {
  parent: HTMLElement;
  document: string;
  language: "python" | "cpp" | string;
  readOnly?: boolean;
  projectFiles?: ProjectFile[];
  activeFilePath?: string;
  onChange?: (content: string) => void;
}

function extractSymbols(code: string, language: string, boost: number): any[] {
  const symbols: any[] = [];
  
  if (language === "python") {
    // Basic def
    const defRegex = /def\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)/g;
    let match;
    while ((match = defRegex.exec(code)) !== null) {
      const name = match[1];
      const args = match[2].split(',').map(a => a.trim().split('=')[0]).filter(a => a && a !== 'self');
      const snippet = args.length > 0 ? `${name}(${args.map((a, i) => `\${${i+1}:${a}}`).join(', ')})` : `${name}()`;
      symbols.push(snippetCompletion(snippet, { label: name, type: "function", boost }));
    }
    
    // Basic class
    const classRegex = /class\s+([a-zA-Z_]\w*)/g;
    while ((match = classRegex.exec(code)) !== null) {
      symbols.push({ label: match[1], type: "class", boost });
    }
    
    // Basic variable assignments
    const varRegex = /^([a-zA-Z_]\w*)\s*=[^=]/gm;
    while ((match = varRegex.exec(code)) !== null) {
      symbols.push({ label: match[1], type: "variable", boost });
    }
  } else if (language === "cpp") {
    // Basic function (very naive)
    const funcRegex = /(?:[a-zA-Z_]\w*(?:<[^>]+>)?\s+)+([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*(?:const\s*)?\{/g;
    let match;
    while ((match = funcRegex.exec(code)) !== null) {
      const name = match[1];
      // Exclude control structures
      if (['if', 'for', 'while', 'switch', 'catch'].includes(name)) continue;
      const args = match[2].split(',').map(a => {
        const parts = a.trim().split(/\s+/);
        return parts[parts.length - 1].replace(/[*&]/g, '');
      }).filter(a => a && a !== 'void');
      const snippet = args.length > 0 ? `${name}(${args.map((a, i) => `\${${i+1}:${a}}`).join(', ')})` : `${name}()`;
      symbols.push(snippetCompletion(snippet, { label: name, type: "function", boost }));
    }
    
    // Basic class/struct
    const classRegex = /(?:class|struct)\s+([a-zA-Z_]\w*)/g;
    while ((match = classRegex.exec(code)) !== null) {
      symbols.push({ label: match[1], type: "class", boost });
    }
  }
  
  return symbols;
}

function createCompletionSource(language: string, projectFiles: ProjectFile[], activeFilePath: string) {
  return (context: CompletionContext): CompletionResult | null => {
    let word = context.matchBefore(/\w*/);
    if (!word || word.from === word.to && !context.explicit) return null;

    const options: any[] = [];
    
    // Keywords
    const keywords = language === "python" 
      ? ['def', 'class', 'import', 'from', 'if', 'else', 'elif', 'return', 'for', 'while', 'try', 'except', 'with', 'as', 'pass', 'break', 'continue']
      : ['int', 'float', 'double', 'char', 'void', 'class', 'struct', 'if', 'else', 'return', 'for', 'while', 'include', 'namespace', 'std', 'const', 'public', 'private'];
      
    for (const kw of keywords) {
      options.push({ label: kw, type: "keyword", boost: -1 });
    }

    // Active document
    const activeDoc = context.state.doc.toString();
    options.push(...extractSymbols(activeDoc, language, 2));

    // Other project files
    for (const file of projectFiles) {
      if (file.path !== activeFilePath) {
        options.push(...extractSymbols(file.content, language, 1));
      }
    }

    // Deduplicate by label
    const seen = new Set();
    const uniqueOptions = [];
    for (const opt of options) {
      if (!seen.has(opt.label)) {
        seen.add(opt.label);
        uniqueOptions.push(opt);
      }
    }

    return {
      from: word.from,
      options: uniqueOptions
    };
  };
}

export function createCodeEditor(options: CodeEditorOptions): EditorView {
  const languageExtension = options.language === "cpp" ? cpp() : python();
  
  const completionSource = createCompletionSource(
    options.language, 
    options.projectFiles || [], 
    options.activeFilePath || ""
  );

  const extensions = [
    basicSetup,
    keymap.of([indentWithTab]),
    languageExtension,
    EditorView.lineWrapping,
    autocompletion({
      override: [completionSource]
    })
  ];

  if (options.readOnly) {
    extensions.push(EditorView.editable.of(false));
  }

  if (options.onChange) {
    extensions.push(EditorView.updateListener.of((update) => {
      if (update.docChanged && options.onChange) {
        options.onChange(update.state.doc.toString());
      }
    }));
  }

  return new EditorView({
    doc: options.document,
    parent: options.parent,
    extensions
  });
}
