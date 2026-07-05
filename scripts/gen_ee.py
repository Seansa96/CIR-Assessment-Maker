import os

# 1. Create electrical-engineering.yaml
cat_content = """schemaVersion: 1
id: electrical-engineering
title: Electrical Engineering
subcategories:
  - id: ee-semiconductor-physics
    title: Semiconductor Physics
  - id: ee-dielectrics-insulators
    title: Dielectrics and Insulators
  - id: ee-magnetic-materials
    title: Magnetic Materials
  - id: ee-magnetic-circuits
    title: Magnetic Circuits
  - id: ee-transformers
    title: Transformers
  - id: ee-power-electronics
    title: Power Electronics
  - id: ee-voltage-regulation
    title: Voltage Regulation
  - id: ee-power-systems
    title: Power Systems
  - id: ee-signals-systems
    title: Signals and Systems
  - id: ee-fourier-analysis
    title: Fourier Analysis
  - id: ee-z-transform
    title: Z-Transform
  - id: ee-digital-filters
    title: Digital Filters
  - id: ee-discrete-fourier
    title: Discrete Fourier Transform
"""

with open("data/categories/electrical-engineering.yaml", "w", encoding="utf-8") as f:
    f.write(cat_content.strip() + "\n")


# 2. Create the assessments
files = {
    'ee-signals-systems-concept-lesson.yaml': """schemaVersion: 1
id: ee-signals-systems-concept-lesson
title: "Introduction to Signals and Systems"
assessmentType: conceptLesson
categoryId: electrical-engineering
subcategoryIds:
  - ee-signals-systems
modeDefault: study
lesson:
  introduction: "Digital Signal Processing (DSP) begins with understanding the properties of signals and the systems that process them."
  sections:
    - id: sec-1
      title: "Continuous vs. Discrete Signals"
      content: >
        A continuous-time signal x(t) is defined for every point in time. 
        A discrete-time signal x[n] is defined only at integer multiples of a sampling period.
        
        The bridge between them is the Sampling Theorem, which states that a continuous signal must be sampled at more than twice its highest frequency (the Nyquist rate) to avoid aliasing.

    - id: sec-2
      title: "Linear Time-Invariant (LTI) Systems"
      content: >
        An LTI system satisfies two properties:
        1. **Linearity**: The response to a linear combination of inputs is the linear combination of their responses (Superposition).
        2. **Time-Invariance**: A time shift in the input causes an identical time shift in the output.
        
        LTI systems are completely characterized by their impulse response, h[n].
questions:
  - id: lti-property
    title: "LTI Properties"
    type: multipleChoice
    skills:
      - lti-systems
    prompt: "Which property dictates that if input x1[n] produces y1[n] and x2[n] produces y2[n], then x1[n]+x2[n] produces y1[n]+y2[n]?"
    choices:
      - id: a
        text: "Time-Invariance"
      - id: b
        text: "Linearity"
      - id: c
        text: "Causality"
      - id: d
        text: "Stability"
    answer:
      choiceId: b
      explanation: "This is the principle of superposition, which defines linearity."
""",
    
    'ee-semiconductor-physics-concept-lesson.yaml': """schemaVersion: 1
id: ee-semiconductor-physics-concept-lesson
title: "Band Gap and Doping"
assessmentType: conceptLesson
categoryId: electrical-engineering
subcategoryIds:
  - ee-semiconductor-physics
modeDefault: study
lesson:
  introduction: "The behavior of modern electronics relies on manipulating the conductivity of semiconductors, primarily Silicon."
  sections:
    - id: sec-1
      title: "The Band Gap"
      content: >
        In a semiconductor, the valence band (bound electrons) and the conduction band (free electrons) are separated by a small energy gap (Eg).
        At absolute zero, the valence band is full and the conduction band is empty, making it an insulator. At room temperature, thermal energy excites some electrons across the gap, creating electron-hole pairs.

    - id: sec-2
      title: "Doping"
      content: >
        Doping introduces impurities to increase conductivity.
        
        - **N-type**: Doping with Group V elements (e.g., Phosphorus) introduces extra electrons (majority carriers).
        - **P-type**: Doping with Group III elements (e.g., Boron) creates "holes" (majority carriers).
questions:
  - id: doping-carriers
    title: "Majority Carriers"
    type: multipleChoice
    skills:
      - semiconductor-doping
    prompt: "In a P-type semiconductor, what are the majority charge carriers?"
    choices:
      - id: a
        text: "Electrons"
      - id: b
        text: "Protons"
      - id: c
        text: "Holes"
      - id: d
        text: "Neutrons"
    answer:
      choiceId: c
      explanation: "Group III dopants have one less valence electron, creating a vacancy or 'hole' that acts as a positive charge carrier."
""",

    'ee-transformers-worked-example.yaml': """schemaVersion: 1
id: ee-transformers-worked-example
title: "Ideal Transformer Calculations"
assessmentType: workedExample
categoryId: electrical-engineering
subcategoryIds:
  - ee-transformers
modeDefault: study
workedExamples:
  - id: we-ideal-transformer
    title: "Calculating Secondary Voltage"
    problem: 'An ideal transformer has 500 primary turns and 50 secondary turns. If the primary voltage is 120 V AC, what is the secondary voltage?'
    steps:
      - id: s1
        title: 'Identify the turns ratio'
        instruction: >
          Turns Ratio (a) = N_primary / N_secondary
          
          a = 500 / 50 = 10
        type: freeResponse
        skills:
          - transformer-turns-ratio
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s2
        title: 'Apply the ideal transformer voltage equation'
        instruction: >
          V_primary / V_secondary = N_primary / N_secondary
          
          120 / V_secondary = 10
        type: freeResponse
        skills:
          - transformer-turns-ratio
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s3
        title: 'Solve for secondary voltage'
        instruction: >
          V_secondary = 120 / 10 = 12 V AC.
          
          Because the secondary voltage is lower than the primary, this is a **step-down** transformer.
        type: freeResponse
        skills:
          - transformer-turns-ratio
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
questions:
  - id: trans-calc
    title: "Calculate Secondary Voltage"
    type: numericResponse
    skills:
      - transformer-turns-ratio
    prompt: 'An ideal transformer has 200 primary turns and 800 secondary turns. If the primary voltage is 24 V, what is the secondary voltage?'
    answer:
      value: 96
      tolerance: 0
""",
    
    'ee-voltage-regulation-concept-lesson.yaml': """schemaVersion: 1
id: ee-voltage-regulation-concept-lesson
title: "Linear vs Switching Regulators"
assessmentType: conceptLesson
categoryId: electrical-engineering
subcategoryIds:
  - ee-voltage-regulation
modeDefault: study
lesson:
  introduction: "Voltage regulators maintain a constant output voltage despite variations in input voltage or load current. They are essential for protecting sensitive electronic components."
  sections:
    - id: sec-1
      title: "Linear Regulators"
      content: >
        Linear regulators act like a variable resistor, burning off excess voltage as heat to maintain the output. 
        
        **Pros**: Very low noise, simple, cheap.
        
        **Cons**: Low efficiency, especially when the difference between input and output voltage is large. The power dissipated is P = (Vin - Vout) * I.

    - id: sec-2
      title: "Switching Regulators (DC-DC Converters)"
      content: >
        Switching regulators rapidly turn an energy storage element (inductor or capacitor) on and off to transfer energy to the output.
        
        **Pros**: Highly efficient (often > 90%), can step-up (boost) or step-down (buck) voltage.
        
        **Cons**: Complex design, introduces high-frequency switching noise into the circuit.
questions:
  - id: regulator-choice
    title: "Choosing a Regulator"
    type: multipleChoice
    skills:
      - voltage-regulation
    prompt: "If you need to step down a 12V battery to 3.3V at 2 Amps for a noisy motor controller where efficiency is critical, which regulator should you choose?"
    choices:
      - id: a
        text: "Linear Regulator"
      - id: b
        text: "Buck Switching Regulator"
      - id: c
        text: "Boost Switching Regulator"
      - id: d
        text: "Ideal Transformer"
    answer:
      choiceId: b
      explanation: "A switching regulator is highly efficient and a Buck converter steps down voltage. A linear regulator would dissipate (12-3.3)*2 = 17.4W of heat!"
"""
}

for filename, content in files.items():
    filepath = os.path.join("data/assessments", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
print("All files generated successfully!")
