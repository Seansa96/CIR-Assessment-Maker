import { unified } from "unified";
import remarkParse from "remark-parse";
import remarkMath from "remark-math";
import remarkRehype from "remark-rehype";
import rehypeKatex from "rehype-katex";
import rehypeStringify from "rehype-stringify";
import "katex/dist/contrib/mhchem.mjs";

async function test() {
    const processor = unified()
        .use(remarkParse)
        .use(remarkMath)
        .use(remarkRehype)
        .use(rehypeKatex, { strict: false })
        .use(rehypeStringify);
    
    const res = await processor.process("$\\ce{H2O}$");
    console.log(String(res));
}
test();
