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
