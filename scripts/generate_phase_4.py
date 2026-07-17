import os

files = {
    'chemistry-solutions-concentration-concept-lesson.yaml': """schemaVersion: 1
id: chemistry-solutions-concentration-concept-lesson
title: "Solution Concentration: Molarity"
type: conceptLesson
categoryId: chemistry
topicId: chemistry-solutions
modeDefault: study
lesson:
  introduction: "A solution is a homogeneous mixture of a solute dissolved in a solvent. To quantify how much solute is present, chemists use concentration."
  sections:
    - id: sec-1
      title: "What is Molarity?"
      content: >
        Molarity ($M$) is the most common unit of concentration in chemistry. It is defined as the number of moles of solute per liter of solution.
        
        $M = \\frac{\\text{moles of solute}}{\\text{Liters of solution}}$

    - id: sec-2
      title: "Preparing a Solution"
      content: >
        To prepare a $1.0 \\text{ M}$ solution of $NaCl$, you cannot just add $1.0$ mole of $NaCl$ to $1.0$ Liter of water. Instead, you must add $1.0$ mole of $NaCl$ to a flask, and then add *enough water* until the **total volume** of the solution is $1.0$ Liter.
questions:
  - id: molarity-def
    title: "Molarity Definition"
    type: multipleChoice
    skills:
      - solutions-molarity
    prompt: "Which of the following is the correct formula for Molarity?"
    choices:
      - id: a
        text: "moles of solute / kilograms of solvent"
      - id: b
        text: "grams of solute / Liters of solution"
      - id: c
        text: "moles of solute / Liters of solution"
      - id: d
        text: "moles of solute / Liters of solvent"
    answer:
      choiceId: c
      explanation: "Molarity is strictly moles of solute divided by the TOTAL Liters of the solution."
""",
    'chemistry-solutions-molarity-worked-example.yaml': """schemaVersion: 1
id: chemistry-solutions-molarity-worked-example
title: "Calculating Molarity"
type: workedExample
categoryId: chemistry
topicId: chemistry-solutions
modeDefault: study
workedExamples:
  - id: we-molarity
    title: "Calculating Molarity from Grams"
    problem: "What is the molarity of a solution prepared by dissolving $11.7$ g of $NaCl$ (molar mass = $58.44$ g/mol) in enough water to make $500$ mL of solution?"
    steps:
      - id: s1
        title: "Convert grams to moles"
        content: >
          $\\text{Moles of } NaCl = \\frac{11.7 \\text{ g}}{58.44 \\text{ g/mol}} \\approx 0.200 \\text{ moles}$
      - id: s2
        title: "Convert volume to Liters"
        content: >
          $500 \\text{ mL} = 0.500 \\text{ L}$
      - id: s3
        title: "Calculate Molarity"
        content: >
          $M = \\frac{0.200 \\text{ moles}}{0.500 \\text{ L}} = 0.400 \\text{ M}$
questions:
  - id: q-molarity-calc
    title: "Calculate Molarity"
    type: typed
    skills:
      - solutions-molarity
    prompt: "If you have $0.50$ moles of $HCl$ in $2.0$ L of solution, what is the molarity ($M$)?"
    answer:
      expected: "0.25"
""",
    'chem-aqueous-solutions-solubility-rules-recall.yaml': """schemaVersion: 1
id: chem-aqueous-solutions-solubility-rules-recall
title: "Solubility Rules Drill"
type: recallDrill
categoryId: chemistry
topicId: chem-aqueous-solutions
modeDefault: practice
items:
  - id: sr-nitrates
    type: typed
    skills:
      - solubility-rules
    prompt: "Are all Nitrate ($NO_3^-$) salts soluble or insoluble in water?"
    answer:
      expected: "soluble"
  - id: sr-group1
    type: typed
    skills:
      - solubility-rules
    prompt: "Salts containing Group 1 alkali metals (like $Na^+$ or $K^+$) are always _______."
    answer:
      expected: "soluble"
  - id: sr-silver-chloride
    type: typed
    skills:
      - solubility-rules
    prompt: "Is Silver Chloride ($AgCl$) soluble or insoluble?"
    answer:
      expected: "insoluble"
  - id: sr-sulfates
    type: typed
    skills:
      - solubility-rules
    prompt: "Most sulfates ($SO_4^{2-}$) are soluble, except those of Barium, Strontium, Lead, and _______."
    answer:
      expected: "calcium"
      aliases:
        - "mercury"
""",
    'chem-aqueous-solutions-net-ionic-equations-worked-example.yaml': """schemaVersion: 1
id: chem-aqueous-solutions-net-ionic-equations-worked-example
title: "Writing Net Ionic Equations"
type: workedExample
categoryId: chemistry
topicId: chem-aqueous-solutions
modeDefault: study
workedExamples:
  - id: we-net-ionic
    title: "Precipitation of Silver Chloride"
    problem: "Write the net ionic equation for the reaction between aqueous Silver Nitrate ($AgNO_3$) and aqueous Sodium Chloride ($NaCl$)."
    steps:
      - id: s1
        title: "Write the balanced molecular equation"
        content: >
          $AgNO_3(aq) + NaCl(aq) \\rightarrow AgCl(s) + NaNO_3(aq)$
      - id: s2
        title: "Write the complete ionic equation"
        content: >
          Break all $(aq)$ strong electrolytes into their ions. Keep $(s)$, $(l)$, or $(g)$ intact.
          
          $Ag^+(aq) + NO_3^-(aq) + Na^+(aq) + Cl^-(aq) \\rightarrow AgCl(s) + Na^+(aq) + NO_3^-(aq)$
      - id: s3
        title: "Cancel spectator ions"
        content: >
          $Na^+$ and $NO_3^-$ appear on both sides, so they are spectator ions. Canceling them yields the net ionic equation:
          
          $Ag^+(aq) + Cl^-(aq) \\rightarrow AgCl(s)$
questions:
  - id: q-net-ionic-spec
    title: "Identify Spectator Ions"
    type: multipleChoice
    skills:
      - net-ionic-equations
    prompt: "In the reaction $Pb(NO_3)_2(aq) + 2KI(aq) \\rightarrow PbI_2(s) + 2KNO_3(aq)$, what are the spectator ions?"
    choices:
      - id: a
        text: "$Pb^{2+}$ and $I^-$"
      - id: b
        text: "$K^+$ and $NO_3^-$"
      - id: c
        text: "$Pb^{2+}$ and $NO_3^-$"
      - id: d
        text: "$K^+$ and $I^-$"
    answer:
      choiceId: b
      explanation: "Spectator ions are those that remain aqueous (dissolved) on both sides of the reaction. $KNO_3$ is soluble, so $K^+$ and $NO_3^-$ are the spectator ions."
""",
    'chem-aqueous-solutions-precipitates-concept-lesson.yaml': """schemaVersion: 1
id: chem-aqueous-solutions-precipitates-concept-lesson
title: "Precipitation Reactions"
type: conceptLesson
categoryId: chemistry
topicId: chem-aqueous-solutions
modeDefault: study
lesson:
  introduction: "When two aqueous solutions are mixed, they sometimes form a solid that settles out of solution. This solid is called a precipitate."
  sections:
    - id: sec-1
      title: "Why do Precipitates Form?"
      content: >
        Precipitates form when the electrostatic attraction between the newly mixed cations and anions is stronger than the attraction between those ions and water molecules. The result is an insoluble ionic solid.

    - id: sec-2
      title: "Predicting Precipitation"
      content: >
        To predict if a precipitate will form:
        1. Perform a double replacement (swap the ions).
        2. Check the solubility rules for the two new compounds.
        3. If one compound is insoluble, it forms a precipitate $(s)$.
questions:
  - id: precip-predict
    title: "Will it precipitate?"
    type: multipleChoice
    skills:
      - solubility-rules
    prompt: "If you mix solutions of $KCl$ and $NaNO_3$, will a precipitate form?"
    choices:
      - id: a
        text: "Yes, $KNO_3$ will precipitate."
      - id: b
        text: "Yes, $NaCl$ will precipitate."
      - id: c
        text: "No precipitate will form."
    answer:
      choiceId: c
      explanation: "The possible products are $KNO_3$ and $NaCl$. Both contain Group 1 metals (K, Na) and one contains Nitrate, meaning both are highly soluble in water. No solid forms."
""",
    'chem-acids-strong-weak-concept-lesson.yaml': """schemaVersion: 1
id: chem-acids-strong-weak-concept-lesson
title: "Strong vs Weak Acids"
type: conceptLesson
categoryId: chemistry
topicId: chem-acids
modeDefault: study
lesson:
  introduction: "Acids are substances that donate protons ($H^+$) in aqueous solution. Their 'strength' refers to how completely they dissociate into ions."
  sections:
    - id: sec-1
      title: "Strong Acids"
      content: >
        Strong acids dissociate **100%** in water. The reaction goes to completion.
        
        Example: $HCl(aq) \\rightarrow H^+(aq) + Cl^-(aq)$
        
        The six common strong acids are: $HCl$, $HBr$, $HI$, $HNO_3$, $H_2SO_4$, $HClO_4$.

    - id: sec-2
      title: "Weak Acids"
      content: >
        Weak acids dissociate only **partially** (often less than 5%) in water, establishing an equilibrium.
        
        Example: $HF(aq) \\rightleftharpoons H^+(aq) + F^-(aq)$
questions:
  - id: strong-weak-id
    title: "Identifying Acid Strength"
    type: multipleChoice
    skills:
      - acid-base-strength
    prompt: "Which of the following is a weak acid?"
    choices:
      - id: a
        text: "$HCl$"
      - id: b
        text: "$HNO_3$"
      - id: c
        text: "$H_2SO_4$"
      - id: d
        text: "$CH_3COOH$ (Acetic acid)"
    answer:
      choiceId: d
      explanation: "Acetic acid is not on the list of the 6 strong acids, making it a weak acid."
""",
    'chem-acids-ph-poh-worked-example.yaml': """schemaVersion: 1
id: chem-acids-ph-poh-worked-example
title: "Calculating pH and pOH"
type: workedExample
categoryId: chemistry
topicId: chem-acids
modeDefault: study
workedExamples:
  - id: we-ph-calc
    title: "Calculating pH from [H+]"
    problem: "What is the pH of a $0.0025 \\text{ M}$ solution of $HCl$?"
    steps:
      - id: s1
        title: "Determine [H+]"
        content: >
          Since $HCl$ is a strong acid, it dissociates completely.
          
          $[H^+] = 0.0025 \\text{ M}$
      - id: s2
        title: "Apply the pH formula"
        content: >
          $pH = -\\log_{10}[H^+]$
          
          $pH = -\\log_{10}(0.0025) \approx 2.60$
questions:
  - id: q-poh-calc
    title: "Calculate pOH"
    type: typed
    skills:
      - ph-calculations
    prompt: "If the pH of a solution is 4.5, what is its pOH? (Remember: $pH + pOH = 14$)"
    answer:
      expected: "9.5"
""",
    'chem-acids-conjugate-pairs-recall.yaml': """schemaVersion: 1
id: chem-acids-conjugate-pairs-recall
title: "Conjugate Acid-Base Pairs Drill"
type: recallDrill
categoryId: chemistry
topicId: chem-acids
modeDefault: practice
items:
  - id: ca-drill-1
    type: typed
    skills:
      - conjugate-pairs
    prompt: "What is the conjugate base of $HCl$?"
    answer:
      expected: "Cl-"
  - id: ca-drill-2
    type: typed
    skills:
      - conjugate-pairs
    prompt: "What is the conjugate base of $H_2O$?"
    answer:
      expected: "OH-"
  - id: ca-drill-3
    type: typed
    skills:
      - conjugate-pairs
    prompt: "What is the conjugate acid of $NH_3$?"
    answer:
      expected: "NH4+"
  - id: ca-drill-4
    type: typed
    skills:
      - conjugate-pairs
    prompt: "What is the conjugate acid of $H_2O$?"
    answer:
      expected: "H3O+"
"""
}

base_dir = "data/assessments"
for filename, content in files.items():
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
