with open('data/assessments/calc2-parametric-curves-test.yaml', 'a', encoding='utf-8') as f:
    f.write(r'''
- id: q-param-curves-test-graph-1
  type: graphingResponse
  title: Graph the Parametric Curve
  prompt: |
    Draw the parametric curve $x(t) = 3\cos(t), y(t) = 2\sin(t)$ for $0 \le t \le 2\pi$. 
    Use the ellipse tool to draw the shape, and use the point tool to plot the starting point at $t=0$.
  answer:
    graphingAnswer:
      features:
        - type: ShapeType
          stringValue: ellipse
          weight: 1.0
        - type: Vertex
          x: 3.0
          y: 0.0
          tolerance: 0.2
          weight: 0.5
        - type: Vertex
          x: -3.0
          y: 0.0
          tolerance: 0.2
          weight: 0.5
        - type: Vertex
          x: 0.0
          y: 2.0
          tolerance: 0.2
          weight: 0.5
        - type: Vertex
          x: 0.0
          y: -2.0
          tolerance: 0.2
          weight: 0.5
        - type: PassesThrough
          x: 3.0
          y: 0.0
          tolerance: 0.2
          weight: 1.0
  explanation: |
    The parametric equations $x = 3\cos(t)$ and $y = 2\sin(t)$ describe an ellipse centered at the origin with a horizontal semi-axis of $3$ and a vertical semi-axis of $2$. At $t=0$, $x = 3\cos(0) = 3$ and $y = 2\sin(0) = 0$, so the starting point is $(3, 0)$.
  skills:
  - parametric-curves
''')

with open('data/assessments/calc2-parametric-derivatives-test.yaml', 'a', encoding='utf-8') as f:
    f.write(r'''
  - id: q-param-deriv-test-graph-1
    type: graphingResponse
    title: Tangent Line Graphing
    prompt: |
      Consider the parametric curve $x(t) = t^2, y(t) = t^3 - 3t$.
      At $t = 2$, the position is $(4, 2)$. The derivative vector is $\langle x'(2), y'(2) \rangle = \langle 4, 9 \rangle$.
      Use the line tool to draw the tangent line to the curve at $t = 2$.
    answer:
      graphingAnswer:
        features:
          - type: ShapeType
            stringValue: line
            weight: 1.0
          - type: PassesThrough
            x: 4.0
            y: 2.0
            tolerance: 0.2
            weight: 1.0
          - type: PassesThrough
            x: 8.0
            y: 11.0
            tolerance: 0.2
            weight: 1.0
    explanation: |
      The tangent line must pass through the point of tangency $(4, 2)$. Since the slope is $dy/dx = 9/4$, another point on the line is $(4+4, 2+9) = (8, 11)$.
    skills:
      - parametric-derivatives
''')

with open('data/assessments/calc2-polar-curves-test.yaml', 'a', encoding='utf-8') as f:
    f.write(r'''
  - id: q-polar-curves-test-graph-1
    type: graphingResponse
    title: Graph the Polar Circle
    prompt: |
      Consider the polar equation $r = 4\cos\theta$.
      Convert this to a Cartesian equation, and then use the ellipse tool to draw the shape on the graph.
    answer:
      graphingAnswer:
        features:
          - type: ShapeType
            stringValue: ellipse
            weight: 1.0
          - type: Vertex
            x: 2.0
            y: 2.0
            tolerance: 0.2
            weight: 0.5
          - type: Vertex
            x: 2.0
            y: -2.0
            tolerance: 0.2
            weight: 0.5
          - type: Vertex
            x: 4.0
            y: 0.0
            tolerance: 0.2
            weight: 0.5
          - type: Vertex
            x: 0.0
            y: 0.0
            tolerance: 0.2
            weight: 0.5
    explanation: |
      Multiplying both sides by $r$ gives $r^2 = 4r\cos\theta$, which translates to $x^2 + y^2 = 4x$.
      Completing the square gives $(x-2)^2 + y^2 = 4$.
      This is a circle (ellipse) centered at $(2, 0)$ with a radius of $2$.
    skills:
      - polar-curves
''')

with open('data/assessments/calc2-parametric-polar-conics-hard-test.yaml', 'a', encoding='utf-8') as f:
    f.write(r'''
- id: q-conics-hard-test-graph-1
  type: graphingResponse
  title: Graphing the Conic Section
  prompt: |
    A conic section is defined parametrically as $x(t) = 4 + 3\cos(t)$ and $y(t) = 1 + 3\sin(t)$.
    Determine the Cartesian equation of this conic section and draw it using the ellipse tool.
  answer:
    graphingAnswer:
      features:
        - type: ShapeType
          stringValue: ellipse
          weight: 1.0
        - type: Vertex
          x: 7.0
          y: 1.0
          tolerance: 0.2
          weight: 0.5
        - type: Vertex
          x: 1.0
          y: 1.0
          tolerance: 0.2
          weight: 0.5
        - type: Vertex
          x: 4.0
          y: 4.0
          tolerance: 0.2
          weight: 0.5
        - type: Vertex
          x: 4.0
          y: -2.0
          tolerance: 0.2
          weight: 0.5
  explanation: |
    Subtracting the constants and using $\cos^2 t + \sin^2 t = 1$, we get $(x-4)^2/9 + (y-1)^2/9 = 1$, which is the circle $(x-4)^2 + (y-1)^2 = 9$. This circle is centered at $(4, 1)$ with a radius of $3$.
  skills:
  - parametric-curves
''')
