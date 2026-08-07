import assert from "node:assert/strict";
import { renderMarkdown } from "./src/scripts/markdownRenderer.js";

const rendered = await renderMarkdown(`Plain paragraph with $x^2$.

$$
\\int_0^1 x\\,dx
$$

| Molecule | Formula |
| --- | --- |
| Water | $\\ce{H2O}$ |

~~Deprecated~~`);

assert.match(rendered, /<p>Plain paragraph with/);
assert.match(rendered, /class="math math-inline"/);
assert.match(rendered, /class="math math-display"/);
assert.match(rendered, /markdown-table-scroll/);
assert.match(rendered, /<table>/);
assert.match(rendered, /aria-label="Scrollable table"/);
assert.match(rendered, /mathvariant="normal">H</);
assert.match(rendered, /<del>Deprecated<\/del>/);

console.log("Markdown rendering checks passed.");
