import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import remarkRehype from "remark-rehype";
import rehypeKatex from "rehype-katex";
import rehypeStringify from "rehype-stringify";
import "katex/dist/contrib/mhchem.mjs";

function rehypeWrapTables() {
  return (tree) => {
    const wrapTables = (node) => {
      if (!Array.isArray(node.children)) return;

      node.children = node.children.map((child) => {
        wrapTables(child);
        if (child.type !== "element" || child.tagName !== "table") return child;

        return {
          type: "element",
          tagName: "div",
          properties: {
            className: ["markdown-table-scroll"],
            role: "region",
            tabIndex: 0,
            ariaLabel: "Scrollable table"
          },
          children: [child]
        };
      });
    };

    wrapTables(tree);
  };
}

const markdownProcessor = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkMath)
  .use(remarkRehype)
  .use(rehypeKatex, { strict: false })
  .use(rehypeWrapTables)
  .use(rehypeStringify);

export async function renderMarkdown(value) {
  const normalized = (value ?? "").replace(
    /^((?:Solution|Why it works|Why the other choices fail):[^\r\n]*?)\s*\$\$([^\r\n]*?)\$\$\s*$/gm,
    (_match, lead, math) => `${lead}\n\n$$${math}$$`
  );
  const processed = await markdownProcessor.process(normalized);
  return String(processed);
}
