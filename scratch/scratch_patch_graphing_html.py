import re

index_path = 'frontend/src/pages/index.astro'

with open(index_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the HTML block
old_html = """<p class="input-help"><strong>Graphing Tool:</strong> Select a tool and click on the grid to place points (e.g. 2 for a line/circle/parabola, 3 for an ellipse). You can drag placed points or the shape itself to adjust it.</p>
                <div class="graphing-toolbar">
                  <button type="button" class="graph-btn" data-tool="point">Point</button>
                  <button type="button" class="graph-btn" data-tool="line">Line</button>
                  <button type="button" class="graph-btn" data-tool="circle">Circle</button>
                  <button type="button" class="graph-btn" data-tool="parabola">Parabola</button>
                  <button type="button" class="graph-btn" data-tool="ellipse">Ellipse</button>
                  <button type="button" class="graph-btn secondary" data-tool="undo">Undo Point</button>
                  <button type="button" class="graph-btn danger-light" data-tool="clear">Clear All</button>
                </div>"""

new_html = """<p class="input-help"><strong>Graphing Tool:</strong> Select a tool, then click and drag on the grid to draw the shape. You can drag placed points or the shape itself using the Select tool.</p>
                <div class="graphing-toolbar">
                  <button type="button" class="graph-btn" data-tool="select">Select/Move</button>
                  <button type="button" class="graph-btn" data-tool="point">Point</button>
                  <button type="button" class="graph-btn" data-tool="line">Line</button>
                  <button type="button" class="graph-btn" data-tool="circle">Circle</button>
                  <button type="button" class="graph-btn" data-tool="parabola">Parabola</button>
                  <button type="button" class="graph-btn" data-tool="ellipse">Ellipse</button>
                  <button type="button" class="graph-btn danger-light" data-tool="clear">Clear</button>
                </div>"""

if old_html in content:
    content = content.replace(old_html, new_html)
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully patched index.astro")
else:
    print("Could not find the HTML block to replace")
