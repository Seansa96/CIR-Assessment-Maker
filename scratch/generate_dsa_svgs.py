import os

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# SVG templates
svg_linked_list = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 100">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#000" />
    </marker>
  </defs>
  <!-- Node 1 -->
  <rect x="20" y="30" width="80" height="40" fill="white" stroke="black" stroke-width="2"/>
  <line x1="60" y1="30" x2="60" y2="70" stroke="black" stroke-width="2"/>
  <text x="40" y="55" font-family="sans-serif" font-size="16" text-anchor="middle">12</text>
  <circle x="80" y="50" r="4" fill="black"/>
  <line x1="80" y1="50" x2="140" y2="50" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Node 2 -->
  <rect x="150" y="30" width="80" height="40" fill="white" stroke="black" stroke-width="2"/>
  <line x1="190" y1="30" x2="190" y2="70" stroke="black" stroke-width="2"/>
  <text x="170" y="55" font-family="sans-serif" font-size="16" text-anchor="middle">99</text>
  <circle x="210" y="50" r="4" fill="black"/>
  <line x1="210" y1="50" x2="270" y2="50" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Node 3 -->
  <rect x="280" y="30" width="80" height="40" fill="white" stroke="black" stroke-width="2"/>
  <line x1="320" y1="30" x2="320" y2="70" stroke="black" stroke-width="2"/>
  <text x="300" y="55" font-family="sans-serif" font-size="16" text-anchor="middle">37</text>
  <circle x="340" y="50" r="4" fill="black"/>
  <line x1="340" y1="50" x2="400" y2="50" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- Null -->
  <text x="420" y="55" font-family="sans-serif" font-size="16" font-style="italic">null</text>
</svg>"""

svg_stack_queue = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 250">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#000" />
    </marker>
  </defs>

  <!-- Stack -->
  <text x="100" y="30" font-family="sans-serif" font-size="18" font-weight="bold" text-anchor="middle">STACK (LIFO)</text>
  <path d="M 60 80 L 60 220 L 140 220 L 140 80" fill="none" stroke="black" stroke-width="3"/>
  <rect x="65" y="180" width="70" height="35" fill="#lightblue" stroke="black"/>
  <text x="100" y="202" font-family="sans-serif" font-size="14" text-anchor="middle">1st in</text>
  <rect x="65" y="140" width="70" height="35" fill="#lightblue" stroke="black"/>
  <rect x="65" y="100" width="70" height="35" fill="#ffcccb" stroke="black"/>
  <text x="100" y="122" font-family="sans-serif" font-size="14" text-anchor="middle">Last in</text>
  
  <path d="M 100 40 Q 150 40 120 80" fill="none" stroke="green" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="140" y="60" font-family="sans-serif" font-size="14" fill="green">Push</text>
  
  <path d="M 80 80 Q 50 40 100 40" fill="none" stroke="red" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="40" y="60" font-family="sans-serif" font-size="14" fill="red">Pop</text>

  <!-- Queue -->
  <text x="350" y="30" font-family="sans-serif" font-size="18" font-weight="bold" text-anchor="middle">QUEUE (FIFO)</text>
  <path d="M 230 110 L 470 110" fill="none" stroke="black" stroke-width="3"/>
  <path d="M 230 170 L 470 170" fill="none" stroke="black" stroke-width="3"/>
  
  <rect x="250" y="115" width="40" height="50" fill="#lightblue" stroke="black"/>
  <text x="270" y="145" font-family="sans-serif" font-size="14" text-anchor="middle">Last</text>
  <rect x="300" y="115" width="40" height="50" fill="#lightblue" stroke="black"/>
  <rect x="350" y="115" width="40" height="50" fill="#lightblue" stroke="black"/>
  <rect x="400" y="115" width="40" height="50" fill="#ffcccb" stroke="black"/>
  <text x="420" y="145" font-family="sans-serif" font-size="14" text-anchor="middle">1st</text>

  <line x1="200" y1="142" x2="230" y2="142" stroke="green" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="180" y="130" font-family="sans-serif" font-size="14" fill="green">Enqueue</text>

  <line x1="470" y1="142" x2="500" y2="142" stroke="red" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="480" y="130" font-family="sans-serif" font-size="14" fill="red">Dequeue</text>
</svg>"""

svg_hashmap = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 200">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#000" />
    </marker>
  </defs>

  <text x="250" y="30" font-family="sans-serif" font-size="18" font-weight="bold" text-anchor="middle">Hash Table (Linear Probing)</text>

  <!-- Array -->
  <rect x="50" y="80" width="50" height="40" fill="white" stroke="black" stroke-width="2"/>
  <text x="75" y="105" font-family="sans-serif" font-size="16" text-anchor="middle">A</text>
  <text x="75" y="75" font-family="sans-serif" font-size="12" text-anchor="middle" fill="gray">0</text>

  <rect x="100" y="80" width="50" height="40" fill="white" stroke="black" stroke-width="2"/>
  <text x="125" y="105" font-family="sans-serif" font-size="16" text-anchor="middle">B</text>
  <text x="125" y="75" font-family="sans-serif" font-size="12" text-anchor="middle" fill="gray">1</text>

  <rect x="150" y="80" width="50" height="40" fill="white" stroke="black" stroke-width="2"/>
  <text x="175" y="105" font-family="sans-serif" font-size="16" text-anchor="middle"></text>
  <text x="175" y="75" font-family="sans-serif" font-size="12" text-anchor="middle" fill="gray">2</text>

  <rect x="200" y="80" width="50" height="40" fill="#ffcccb" stroke="black" stroke-width="2"/>
  <text x="225" y="105" font-family="sans-serif" font-size="16" text-anchor="middle">X</text>
  <text x="225" y="75" font-family="sans-serif" font-size="12" text-anchor="middle" fill="gray">3</text>

  <rect x="250" y="80" width="50" height="40" fill="#lightgreen" stroke="black" stroke-width="2"/>
  <text x="275" y="105" font-family="sans-serif" font-size="16" text-anchor="middle">NEW</text>
  <text x="275" y="75" font-family="sans-serif" font-size="12" text-anchor="middle" fill="gray">4</text>

  <rect x="300" y="80" width="50" height="40" fill="white" stroke="black" stroke-width="2"/>
  <text x="325" y="75" font-family="sans-serif" font-size="12" text-anchor="middle" fill="gray">5</text>

  <!-- Hashing Action -->
  <text x="225" y="170" font-family="sans-serif" font-size="14" text-anchor="middle" fill="red">Collision at Index 3!</text>
  <path d="M 225 150 Q 250 120 270 130" fill="none" stroke="blue" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="280" y="150" font-family="sans-serif" font-size="12" fill="blue">Probe Next Empty (4)</text>

</svg>"""

svg_binary_tree = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
  <!-- Edges -->
  <line x1="200" y1="50" x2="120" y2="120" stroke="black" stroke-width="2"/>
  <line x1="200" y1="50" x2="280" y2="120" stroke="black" stroke-width="2"/>
  <line x1="120" y1="120" x2="60" y2="190" stroke="black" stroke-width="2"/>
  <line x1="120" y1="120" x2="160" y2="190" stroke="black" stroke-width="2"/>
  <line x1="280" y1="120" x2="340" y2="190" stroke="black" stroke-width="2"/>

  <!-- Nodes -->
  <circle cx="200" cy="50" r="25" fill="#lightblue" stroke="black" stroke-width="2"/>
  <text x="200" y="55" font-family="sans-serif" font-size="16" text-anchor="middle">10</text>
  <text x="200" y="20" font-family="sans-serif" font-size="12" text-anchor="middle" fill="gray">Root</text>

  <circle cx="120" cy="120" r="25" fill="white" stroke="black" stroke-width="2"/>
  <text x="120" y="125" font-family="sans-serif" font-size="16" text-anchor="middle">5</text>

  <circle cx="280" cy="120" r="25" fill="white" stroke="black" stroke-width="2"/>
  <text x="280" y="125" font-family="sans-serif" font-size="16" text-anchor="middle">15</text>

  <circle cx="60" cy="190" r="25" fill="#lightgreen" stroke="black" stroke-width="2"/>
  <text x="60" y="195" font-family="sans-serif" font-size="16" text-anchor="middle">2</text>
  <text x="60" y="230" font-family="sans-serif" font-size="12" text-anchor="middle" fill="gray">Leaf</text>

  <circle cx="160" cy="190" r="25" fill="#lightgreen" stroke="black" stroke-width="2"/>
  <text x="160" y="195" font-family="sans-serif" font-size="16" text-anchor="middle">7</text>
  <text x="160" y="230" font-family="sans-serif" font-size="12" text-anchor="middle" fill="gray">Leaf</text>

  <circle cx="340" cy="190" r="25" fill="#lightgreen" stroke="black" stroke-width="2"/>
  <text x="340" y="195" font-family="sans-serif" font-size="16" text-anchor="middle">20</text>
  <text x="340" y="230" font-family="sans-serif" font-size="12" text-anchor="middle" fill="gray">Leaf</text>

</svg>"""

svg_heap = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300">
  <text x="250" y="30" font-family="sans-serif" font-size="18" font-weight="bold" text-anchor="middle">Min-Heap to Array Mapping</text>

  <!-- Tree -->
  <line x1="250" y1="80" x2="150" y2="140" stroke="black" stroke-width="2"/>
  <line x1="250" y1="80" x2="350" y2="140" stroke="black" stroke-width="2"/>
  <line x1="150" y1="140" x2="100" y2="190" stroke="black" stroke-width="2"/>
  <line x1="150" y1="140" x2="200" y2="190" stroke="black" stroke-width="2"/>

  <circle cx="250" cy="80" r="20" fill="#lightblue" stroke="black" stroke-width="2"/>
  <text x="250" y="85" font-family="sans-serif" font-size="14" text-anchor="middle">1</text>
  <text x="275" y="70" font-family="sans-serif" font-size="12" fill="red">i=0</text>

  <circle cx="150" cy="140" r="20" fill="white" stroke="black" stroke-width="2"/>
  <text x="150" y="145" font-family="sans-serif" font-size="14" text-anchor="middle">3</text>
  <text x="125" y="130" font-family="sans-serif" font-size="12" fill="red">i=1</text>

  <circle cx="350" cy="140" r="20" fill="white" stroke="black" stroke-width="2"/>
  <text x="350" y="145" font-family="sans-serif" font-size="14" text-anchor="middle">6</text>
  <text x="375" y="130" font-family="sans-serif" font-size="12" fill="red">i=2</text>

  <circle cx="100" cy="190" r="20" fill="white" stroke="black" stroke-width="2"/>
  <text x="100" y="195" font-family="sans-serif" font-size="14" text-anchor="middle">5</text>
  <text x="75" y="180" font-family="sans-serif" font-size="12" fill="red">i=3</text>

  <circle cx="200" cy="190" r="20" fill="white" stroke="black" stroke-width="2"/>
  <text x="200" y="195" font-family="sans-serif" font-size="14" text-anchor="middle">9</text>
  <text x="225" y="180" font-family="sans-serif" font-size="12" fill="red">i=4</text>

  <!-- Array -->
  <rect x="100" y="240" width="50" height="40" fill="#lightblue" stroke="black" stroke-width="2"/>
  <text x="125" y="265" font-family="sans-serif" font-size="16" text-anchor="middle">1</text>
  <text x="125" y="235" font-family="sans-serif" font-size="12" text-anchor="middle" fill="red">0</text>

  <rect x="150" y="240" width="50" height="40" fill="white" stroke="black" stroke-width="2"/>
  <text x="175" y="265" font-family="sans-serif" font-size="16" text-anchor="middle">3</text>
  <text x="175" y="235" font-family="sans-serif" font-size="12" text-anchor="middle" fill="red">1</text>

  <rect x="200" y="240" width="50" height="40" fill="white" stroke="black" stroke-width="2"/>
  <text x="225" y="265" font-family="sans-serif" font-size="16" text-anchor="middle">6</text>
  <text x="225" y="235" font-family="sans-serif" font-size="12" text-anchor="middle" fill="red">2</text>

  <rect x="250" y="240" width="50" height="40" fill="white" stroke="black" stroke-width="2"/>
  <text x="275" y="265" font-family="sans-serif" font-size="16" text-anchor="middle">5</text>
  <text x="275" y="235" font-family="sans-serif" font-size="12" text-anchor="middle" fill="red">3</text>

  <rect x="300" y="240" width="50" height="40" fill="white" stroke="black" stroke-width="2"/>
  <text x="325" y="265" font-family="sans-serif" font-size="16" text-anchor="middle">9</text>
  <text x="325" y="235" font-family="sans-serif" font-size="12" text-anchor="middle" fill="red">4</text>
</svg>"""

svg_graph = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
  <!-- Edges -->
  <line x1="200" y1="50" x2="100" y2="150" stroke="black" stroke-width="3"/>
  <line x1="200" y1="50" x2="300" y2="150" stroke="black" stroke-width="3"/>
  <line x1="100" y1="150" x2="300" y2="150" stroke="black" stroke-width="3"/>
  <line x1="100" y1="150" x2="200" y2="250" stroke="black" stroke-width="3"/>
  <line x1="300" y1="150" x2="200" y2="250" stroke="black" stroke-width="3"/>

  <!-- Nodes -->
  <circle cx="200" cy="50" r="25" fill="#lightyellow" stroke="black" stroke-width="2"/>
  <text x="200" y="55" font-family="sans-serif" font-size="18" text-anchor="middle">A</text>

  <circle cx="100" cy="150" r="25" fill="#lightyellow" stroke="black" stroke-width="2"/>
  <text x="100" y="155" font-family="sans-serif" font-size="18" text-anchor="middle">B</text>

  <circle cx="300" cy="150" r="25" fill="#lightyellow" stroke="black" stroke-width="2"/>
  <text x="300" y="155" font-family="sans-serif" font-size="18" text-anchor="middle">C</text>

  <circle cx="200" cy="250" r="25" fill="#lightyellow" stroke="black" stroke-width="2"/>
  <text x="200" y="255" font-family="sans-serif" font-size="18" text-anchor="middle">D</text>

</svg>"""


out_dir = r"c:\Users\SeanS\Downloads\cir_app\frontend\public\media\dsa"
create_dir(out_dir)

def write_svg(filename, content):
    path = os.path.join(out_dir, filename)
    with open(path, "w") as f:
        f.write(content)
    print(f"Generated {filename}")

write_svg("singly-linked-list.svg", svg_linked_list)
write_svg("stack-queue-fifo-lifo.svg", svg_stack_queue)
write_svg("hashmap-linear-probing.svg", svg_hashmap)
write_svg("binary-tree-basic.svg", svg_binary_tree)
write_svg("min-heap-array-mapping.svg", svg_heap)
write_svg("undirected-graph-network.svg", svg_graph)
