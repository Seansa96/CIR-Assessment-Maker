import os

files = {
    'chemistry-measurements-sig-figs-concept-lesson.yaml': """schemaVersion: 1
id: chemistry-measurements-sig-figs-concept-lesson
title: "Significant Figures in Measurements"
type: conceptLesson
categoryId: chemistry
subcategoryIds:
  - chemistry-measurements
modeDefault: study
lesson:
  introduction: "In science, a measurement is only as accurate as the instrument used to make it. Significant figures communicate the precision of a measurement."
  sections:
    - id: sec-1
      title: "What are Significant Figures?"
      content: >
        Significant figures include all the digits in a measurement that are known with certainty, plus one estimated digit. When reading a ruler or graduated cylinder, you always estimate one decimal place beyond the smallest marked calibration.

    - id: sec-2
      title: "Rules for Counting Sig Figs"
      content: >
        1. Non-zero digits are ALWAYS significant (e.g., $1.23$ has 3 sig figs).

        2. Zeros between non-zero digits are ALWAYS significant (e.g., $1.03$ has 3 sig figs).

        3. Leading zeros are NEVER significant; they are just placeholders (e.g., $0.0012$ has 2 sig figs).

        4. Trailing zeros are significant ONLY IF there is a decimal point in the number (e.g., $100$ has 1 sig fig, but $100.$ has 3 sig figs, and $1.20$ has 3 sig figs).
questions:
  - id: sig-fig-count-1
    title: Counting Sig Figs
    type: multipleChoice
    skills:
      - sig-figs
    prompt: "How many significant figures are in the measurement $0.04050$ m?"
    choices:
      - id: a
        text: "3"
      - id: b
        text: "4"
      - id: c
        text: "5"
      - id: d
        text: "6"
    answer:
      choiceId: b
      explanation: "The leading zeros ($0.0...$) are not significant. The 4 and 5 are significant. The zero between them is significant. The trailing zero is significant because there is a decimal point. Thus, 4 sig figs."
""",
    'chemistry-measurements-sig-figs-worked-example.yaml': """schemaVersion: 1
id: chemistry-measurements-sig-figs-worked-example
title: "Calculations with Significant Figures"
type: workedExample
categoryId: chemistry
subcategoryIds:
  - chemistry-measurements
modeDefault: study
workedExamples:
  - id: we-sig-fig-calc
    title: "Multiplication and Division with Sig Figs"
    problem: "Calculate the density of an object with a mass of $14.2$ g and a volume of $3.5$ mL, and report the answer to the correct number of significant figures."
    steps:
      - id: s1
        title: "Identify the number of significant figures in the given values"
        content: >
          Mass = $14.2$ g (3 significant figures)

          Volume = $3.5$ mL (2 significant figures)
      - id: s2
        title: "Perform the calculation"
        content: >
          Density = $\\frac{\\text{Mass}}{\\text{Volume}} = \\frac{14.2}{3.5} = 4.05714285...$ g/mL
      - id: s3
        title: "Round to the correct number of sig figs"
        content: >
          For multiplication and division, the result must have the same number of significant figures as the measurement with the **fewest** significant figures.
          
          Fewest sig figs = 2.
          
          Round $4.057...$ to 2 sig figs: **$4.1$ g/mL**.
questions:
  - id: q-sig-fig-calc
    title: "Apply the Rule"
    type: typed
    skills:
      - sig-figs
    prompt: "What is the product of $2.5$ and $3.42$ reported to the correct number of significant figures?"
    answer:
      expected: "8.5"
""",
    'chemistry-units-dimensional-analysis-worked-example.yaml': """schemaVersion: 1
id: chemistry-units-dimensional-analysis-worked-example
title: "Dimensional Analysis and Conversions"
type: workedExample
categoryId: chemistry
subcategoryIds:
  - chemistry-units
modeDefault: study
workedExamples:
  - id: we-dim-analysis
    title: "Converting between metric units"
    problem: "A liquid has a volume of $450$ mL. Convert this volume to Liters (L)."
    steps:
      - id: s1
        title: "Identify the conversion factor"
        content: >
          We know that $1000 \\text{ mL} = 1 \\text{ L}$.
      - id: s2
        title: "Set up the dimensional analysis"
        content: >
          Write the given value, then multiply by a fraction that cancels out the old unit and introduces the new unit.
          
          $450 \\text{ mL} \\times \\frac{1 \\text{ L}}{1000 \\text{ mL}}$
      - id: s3
        title: "Calculate the result"
        content: >
          $450 \\div 1000 = 0.450 \\text{ L}$.
questions:
  - id: q-dim-analysis
    title: "Convert Grams to Kilograms"
    type: typed
    skills:
      - dimensional-analysis
    prompt: "Convert $1250$ g to kg."
    answer:
      expected: "1.25"
      aliases:
        - "1.250"
""",
    'chemistry-matter-classification-recall.yaml': """schemaVersion: 1
id: chemistry-matter-classification-recall
title: "Classification of Matter"
type: recallDrill
categoryId: chemistry
subcategoryIds:
  - chemistry-matter
modeDefault: practice
items:
  - id: matter-element
    type: typed
    skills:
      - matter-classification
    prompt: "A substance that cannot be broken down into simpler substances by chemical means is an _______."
    answer:
      expected: "element"
  - id: matter-compound
    type: typed
    skills:
      - matter-classification
    prompt: "A substance composed of two or more elements chemically combined in fixed proportions is a _______."
    answer:
      expected: "compound"
  - id: matter-homo-mixture
    type: typed
    skills:
      - matter-classification
    prompt: "A mixture that has a uniform composition throughout is called a _______ mixture."
    answer:
      expected: "homogeneous"
      aliases:
        - "solution"
  - id: matter-hetero-mixture
    type: typed
    skills:
      - matter-classification
    prompt: "A mixture in which the composition is not uniform throughout is a _______ mixture."
    answer:
      expected: "heterogeneous"
""",
    'chemistry-gases-ideal-gas-law-worked-example.yaml': """schemaVersion: 1
id: chemistry-gases-ideal-gas-law-worked-example
title: "Ideal Gas Law Applications"
type: workedExample
categoryId: chemistry
subcategoryIds:
  - chemistry-gases
modeDefault: study
workedExamples:
  - id: we-ideal-gas
    title: "Calculating Volume using PV=nRT"
    problem: "What is the volume occupied by $0.250$ moles of an ideal gas at $1.20$ atm and $300$ K? (Use $R = 0.08206$ L atm / mol K)"
    steps:
      - id: s1
        title: "Identify the given variables and the equation"
        content: >
          $n = 0.250 \\text{ mol}$

          $P = 1.20 \\text{ atm}$

          $T = 300 \\text{ K}$

          $R = 0.08206 \\text{ L atm / (mol K)}$

          Equation: $PV = nRT$
      - id: s2
        title: "Rearrange the equation for the unknown"
        content: >
          We need to solve for Volume ($V$).

          $V = \\frac{nRT}{P}$
      - id: s3
        title: "Substitute values and solve"
        content: >
          $V = \\frac{(0.250)(0.08206)(300)}{1.20}$

          $V = 5.12875 \\text{ L}$

          Rounding to 3 significant figures, $V = 5.13 \\text{ L}$.
questions:
  - id: q-ideal-gas
    title: "Calculate Moles"
    type: multipleChoice
    skills:
      - ideal-gas-law
    prompt: "How many moles of gas are in a $10.0$ L container at $2.00$ atm and $298$ K? ($R = 0.08206$)"
    choices:
      - id: c1
        text: "$0.818$ mol"
      - id: c2
        text: "$1.22$ mol"
      - id: c3
        text: "$0.409$ mol"
      - id: c4
        text: "$2.44$ mol"
    answer:
      choiceId: c1
      explanation: "$n = \\frac{PV}{RT} = \\frac{2.00 \\times 10.0}{0.08206 \\times 298} \\approx 0.818$ mol."
""",
    'chemistry-thermochemistry-enthalpy-concept-lesson.yaml': """schemaVersion: 1
id: chemistry-thermochemistry-enthalpy-concept-lesson
title: "Enthalpy and Heat of Reaction"
type: conceptLesson
categoryId: chemistry
subcategoryIds:
  - chemistry-thermochemistry
modeDefault: study
lesson:
  introduction: "Thermochemistry studies the heat absorbed or released during chemical and physical changes. Central to this is Enthalpy ($H$)."
  sections:
    - id: sec-1
      title: "What is Enthalpy?"
      content: >
        Enthalpy ($H$) is a measure of the total heat content of a system at constant pressure. While we cannot measure absolute enthalpy, we can measure the **change in enthalpy ($\\Delta H$)** during a reaction.

        $\\Delta H = H_{\\text{products}} - H_{\\text{reactants}}$
    - id: sec-2
      title: "Exothermic vs Endothermic"
      content: >
        - **Exothermic Reactions**: Heat is released to the surroundings. The products have less enthalpy than the reactants, so $\\Delta H$ is **negative** ($\\Delta H < 0$).

        - **Endothermic Reactions**: Heat is absorbed from the surroundings. The products have more enthalpy than the reactants, so $\\Delta H$ is **positive** ($\\Delta H > 0$).
questions:
  - id: thermochem-exo-endo
    title: "Identifying Reaction Types"
    type: multipleChoice
    skills:
      - enthalpy-calorimetry
    prompt: "A chemical cold pack feels cold to the touch when activated. What type of reaction is occurring, and what is the sign of $\\Delta H$?"
    choices:
      - id: a
        text: "Exothermic, $\\Delta H$ is negative"
      - id: b
        text: "Exothermic, $\\Delta H$ is positive"
      - id: c
        text: "Endothermic, $\\Delta H$ is negative"
      - id: d
        text: "Endothermic, $\\Delta H$ is positive"
    answer:
      choiceId: d
      explanation: "Because it feels cold, the reaction is pulling heat FROM its surroundings (your hand). This means it is absorbing heat, making it Endothermic, which corresponds to a positive $\\Delta H$."
"""
}

base_dir = "data/assessments"
os.makedirs(base_dir, exist_ok=True)

for filename, content in files.items():
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
