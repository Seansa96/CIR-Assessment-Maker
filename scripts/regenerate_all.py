import os

files = {
    'chemistry-measurements-sig-figs-concept-lesson.yaml': """schemaVersion: 1
id: chemistry-measurements-sig-figs-concept-lesson
title: "Significant Figures in Measurements"
assessmentType: conceptLesson
categoryId: chemistry
topicId: chemistry-measurements
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
        1. Non-zero digits are ALWAYS significant (e.g., 1.23 has 3 sig figs).

        2. Zeros between non-zero digits are ALWAYS significant (e.g., 1.03 has 3 sig figs).

        3. Leading zeros are NEVER significant; they are just placeholders (e.g., 0.0012 has 2 sig figs).

        4. Trailing zeros are significant ONLY IF there is a decimal point in the number (e.g., 100 has 1 sig fig, but 100. has 3 sig figs, and 1.20 has 3 sig figs).
questions:
  - id: sig-fig-count-1
    title: Counting Sig Figs
    type: multipleChoice
    skills:
      - sig-figs
    prompt: 'How many significant figures are in the measurement 0.04050 m?'
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
      explanation: 'The leading zeros (0.0...) are not significant. The 4 and 5 are significant. The zero between them is significant. The trailing zero is significant because there is a decimal point. Thus, 4 sig figs.'
""",

    'chemistry-measurements-sig-figs-worked-example.yaml': """schemaVersion: 1
id: chemistry-measurements-sig-figs-worked-example
title: "Calculations with Significant Figures"
assessmentType: workedExample
categoryId: chemistry
topicId: chemistry-measurements
modeDefault: study
workedExamples:
  - id: we-sig-fig-calc
    title: "Multiplication and Division with Sig Figs"
    problem: 'Calculate the density of an object with a mass of 14.2 g and a volume of 3.5 mL, and report the answer to the correct number of significant figures.'
    steps:
      - id: s1
        title: 'Identify the number of significant figures in the given values'
        instruction: >
          Mass = 14.2 g (3 significant figures)

          Volume = 3.5 mL (2 significant figures)
        type: freeResponse
        skills:
          - sig-figs
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s2
        title: 'Perform the calculation'
        instruction: >
          Density = Mass / Volume = 14.2 / 3.5 = 4.057... g/mL
        type: freeResponse
        skills:
          - sig-figs
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s3
        title: 'Round to the correct number of sig figs'
        instruction: >
          For multiplication and division, the result must have the same number of significant figures as the measurement with the **fewest** significant figures.
          
          Fewest sig figs = 2.
          
          Round 4.057... to 2 sig figs: **4.1 g/mL**.
        type: freeResponse
        skills:
          - sig-figs
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
questions:
  - id: q-sig-fig-calc
    title: "Apply the Rule"
    type: numericResponse
    skills:
      - sig-figs
    prompt: 'What is the product of 2.5 and 3.42 reported to the correct number of significant figures?'
    answer:
      value: 8.5
      tolerance: 0
""",

    'chemistry-units-dimensional-analysis-worked-example.yaml': """schemaVersion: 1
id: chemistry-units-dimensional-analysis-worked-example
title: "Dimensional Analysis and Conversions"
assessmentType: workedExample
categoryId: chemistry
topicId: chemistry-units
modeDefault: study
workedExamples:
  - id: we-dim-analysis
    title: "Converting Units"
    problem: 'Convert 4.5 hours into seconds.'
    steps:
      - id: s1
        title: 'Identify the given and desired units'
        instruction: >
          Given: 4.5 hours.
          
          Desired: seconds.
        type: freeResponse
        skills:
          - dimensional-analysis
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s2
        title: 'Determine the conversion factors'
        instruction: >
          1 hour = 60 minutes
          
          1 minute = 60 seconds
        type: freeResponse
        skills:
          - dimensional-analysis
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s3
        title: 'Set up the calculation'
        instruction: >
          Multiply the given value by conversion factors so that unwanted units cancel out.
          
          4.5 hours * (60 minutes / 1 hour) * (60 seconds / 1 minute) = 16200 seconds.
        type: freeResponse
        skills:
          - dimensional-analysis
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
questions:
  - id: dim-analysis-calc
    title: "Conversion Practice"
    type: numericResponse
    skills:
      - dimensional-analysis
    prompt: 'How many inches are in 2.5 feet? (1 foot = 12 inches)'
    answer:
      value: 30
      tolerance: 0
""",

    'chemistry-matter-classification-recall.yaml': """schemaVersion: 1
id: chemistry-matter-classification-recall
title: "Matter Classification Drill"
assessmentType: recallDrill
categoryId: chemistry
topicId: chemistry-matter
modeDefault: practice
items:
  - id: mc-drill-1
    type: typed
    skills:
      - matter-classification
    prompt: "A mixture that is uniform throughout, such as salt water, is called a _______ mixture."
    answer:
      expected: "homogeneous"
      aliases:
        - "solution"
  - id: mc-drill-2
    type: typed
    skills:
      - matter-classification
    prompt: "A substance that consists of only one type of atom is called an _______."
    answer:
      expected: "element"
  - id: mc-drill-3
    type: typed
    skills:
      - matter-classification
    prompt: "Water (H2O) is classified as a _______ because it is made of two different elements chemically bonded together."
    answer:
      expected: "compound"
  - id: mc-drill-4
    type: typed
    skills:
      - matter-classification
    prompt: "A mixture that is not uniform, such as sand and water, is called a _______ mixture."
    answer:
      expected: "heterogeneous"
""",

    'chemistry-gases-ideal-gas-law-worked-example.yaml': """schemaVersion: 1
id: chemistry-gases-ideal-gas-law-worked-example
title: "The Ideal Gas Law"
assessmentType: workedExample
categoryId: chemistry
topicId: chemistry-gases
modeDefault: study
workedExamples:
  - id: we-ideal-gas
    title: "Solving for Volume"
    problem: 'What volume does 0.500 moles of Oxygen gas occupy at 298 K and 1.20 atm? (Use R = 0.0821 L·atm/mol·K)'
    steps:
      - id: s1
        title: 'Identify the known variables and the unknown'
        instruction: >
          Known: n = 0.500 mol, T = 298 K, P = 1.20 atm, R = 0.0821 L·atm/mol·K.
          
          Unknown: V = ?
        type: freeResponse
        skills:
          - ideal-gas-law
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s2
        title: 'Rearrange the Ideal Gas Law equation'
        instruction: >
          The Ideal Gas Law is PV = nRT.
          
          Solving for V gives: V = nRT / P
        type: freeResponse
        skills:
          - ideal-gas-law
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s3
        title: 'Substitute values and calculate'
        instruction: >
          V = (0.500 * 0.0821 * 298) / 1.20
          
          V = 10.19... L.
          
          Rounding to three significant figures, V = 10.2 L.
        type: freeResponse
        skills:
          - ideal-gas-law
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
questions:
  - id: ideal-gas-calc
    title: "Calculate Volume"
    type: numericResponse
    skills:
      - ideal-gas-law
    prompt: 'If you have 2.0 moles of a gas at 1.5 atm and 300 K, what is its volume? (Use R = 0.0821 L·atm/mol·K)'
    answer:
      value: 32.84
      tolerance: 0.1
""",

    'chemistry-thermochemistry-enthalpy-concept-lesson.yaml': """schemaVersion: 1
id: chemistry-thermochemistry-enthalpy-concept-lesson
title: "Enthalpy and Heat of Reaction"
assessmentType: conceptLesson
categoryId: chemistry
topicId: chemistry-thermochemistry
modeDefault: study
lesson:
  introduction: "Thermochemistry studies the heat absorbed or released during chemical and physical changes. Central to this is Enthalpy (H)."
  sections:
    - id: sec-1
      title: "What is Enthalpy?"
      content: >
        Enthalpy (H) is a measure of the total heat content of a system at constant pressure. While we cannot measure absolute enthalpy, we can measure the **change in enthalpy (ΔH)** during a reaction.

        ΔH = H(products) - H(reactants)
    - id: sec-2
      title: "Exothermic vs Endothermic"
      content: >
        - **Exothermic Reactions**: Heat is released to the surroundings. The products have less enthalpy than the reactants, so ΔH is **negative** (ΔH < 0).

        - **Endothermic Reactions**: Heat is absorbed from the surroundings. The products have more enthalpy than the reactants, so ΔH is **positive** (ΔH > 0).
questions:
  - id: thermochem-exo-endo
    title: "Identifying Reaction Types"
    type: multipleChoice
    skills:
      - enthalpy-calorimetry
    prompt: 'A chemical cold pack feels cold to the touch when activated. What type of reaction is occurring, and what is the sign of ΔH?'
    choices:
      - id: a
        text: 'Exothermic, ΔH is negative'
      - id: b
        text: 'Exothermic, ΔH is positive'
      - id: c
        text: 'Endothermic, ΔH is negative'
      - id: d
        text: 'Endothermic, ΔH is positive'
    answer:
      choiceId: d
      explanation: 'Because it feels cold, the reaction is pulling heat FROM its surroundings (your hand). This means it is absorbing heat, making it Endothermic, which corresponds to a positive ΔH.'
""",

    'chem-periodic-trends-concept-lesson.yaml': """schemaVersion: 1
id: chem-periodic-trends-concept-lesson
title: "Periodic Trends: Atomic Radius and Ionization Energy"
assessmentType: conceptLesson
categoryId: chemistry
topicId: chem-periodic-trends
modeDefault: study
lesson:
  introduction: "The arrangement of the periodic table allows us to predict the properties of elements based on their position. These predictable patterns are called periodic trends."
  sections:
    - id: sec-1
      title: "Atomic Radius"
      content: >
        Atomic radius is the distance from the nucleus to the outermost electron shell.

        - **Down a Group**: Atomic radius **increases** because new electron shells are added.
        - **Across a Period (left to right)**: Atomic radius **decreases**. Although electrons are added to the same shell, protons are also added to the nucleus. This increases the effective nuclear charge, pulling the electrons closer.

    - id: sec-2
      title: "Ionization Energy"
      content: >
        Ionization energy is the energy required to remove an electron from a neutral atom in its gaseous state.

        - **Down a Group**: Ionization energy **decreases** because the outermost electrons are further from the nucleus and shielded by inner electrons, making them easier to remove.
        - **Across a Period (left to right)**: Ionization energy **increases** due to the increasing effective nuclear charge holding the electrons more tightly.
questions:
  - id: periodic-trends-radius
    title: "Comparing Atomic Radius"
    type: multipleChoice
    skills:
      - periodic-trends
    prompt: "Which of the following elements has the largest atomic radius?"
    choices:
      - id: a
        text: "Lithium (Li)"
      - id: b
        text: "Fluorine (F)"
      - id: c
        text: "Sodium (Na)"
      - id: d
        text: "Chlorine (Cl)"
    answer:
      choiceId: c
      explanation: "Radius increases down a group and decreases across a period. Sodium is below Lithium (larger) and to the left of Chlorine (larger). Fluorine is at the top right (smallest)."
""",

    'chem-ions-formation-concept-lesson.yaml': """schemaVersion: 1
id: chem-ions-formation-concept-lesson
title: "Ion Formation: Cations and Anions"
assessmentType: conceptLesson
categoryId: chemistry
topicId: chem-ions
modeDefault: study
lesson:
  introduction: "Atoms are neutral because they have an equal number of protons and electrons. When atoms gain or lose electrons to achieve a stable electron configuration, they become charged particles called ions."
  sections:
    - id: sec-1
      title: "Cations (Positive Ions)"
      content: >
        Metals tend to **lose** electrons to achieve a full outer shell (octet). When they lose negatively charged electrons, they are left with more protons than electrons, resulting in a **positive** charge.

    - id: sec-2
      title: "Anions (Negative Ions)"
      content: >
        Nonmetals tend to **gain** electrons to complete their valence shell. Gaining negatively charged electrons results in a **negative** charge.
questions:
  - id: ion-formation-1
    title: "Cation Identification"
    type: multipleChoice
    skills:
      - ion-formation
    prompt: "When a Magnesium (Mg) atom loses two electrons, what is the net charge of the resulting ion?"
    choices:
      - id: a
        text: "-2"
      - id: b
        text: "-1"
      - id: c
        text: "+1"
      - id: d
        text: "+2"
    answer:
      choiceId: d
      explanation: "Losing two negative electrons leaves the atom with a net positive charge of +2."
""",

    'chem-ionic-covalent-distinction-concept-lesson.yaml': """schemaVersion: 1
id: chem-ionic-covalent-distinction-concept-lesson
title: "Distinguishing Ionic and Covalent Bonds"
assessmentType: conceptLesson
categoryId: chemistry
topicId: chem-ionic-covalent-distinction
modeDefault: study
lesson:
  introduction: "Chemical bonds hold atoms together in compounds. The two primary types of intramolecular bonds are ionic and covalent, which differ fundamentally in how electrons are shared or transferred."
  sections:
    - id: sec-1
      title: "Ionic Bonds: Transfer of Electrons"
      content: >
        Ionic bonds occur when one or more electrons are **transferred** from one atom to another. This typically happens between a **metal** (which loses electrons to become a cation) and a **nonmetal** (which gains electrons to become an anion).
        
        The resulting oppositely charged ions attract each other via electrostatic forces, forming an ionic crystal lattice.

    - id: sec-2
      title: "Covalent Bonds: Sharing of Electrons"
      content: >
        Covalent bonds occur when atoms **share** pairs of electrons to achieve stable electron configurations. This typically happens between two **nonmetals**.
        
        The shared electrons hold the atoms together in discrete molecules.
questions:
  - id: bond-type-id
    title: "Identifying Bond Types"
    type: multipleChoice
    skills:
      - ionic-covalent-distinction
    prompt: "Which of the following compounds is primarily ionic?"
    choices:
      - id: a
        text: "CO2"
      - id: b
        text: "MgCl2"
      - id: c
        text: "H2O"
      - id: d
        text: "CH4"
    answer:
      choiceId: b
      explanation: "MgCl2 consists of a metal (Mg) and a nonmetal (Cl), making it an ionic compound. The others consist entirely of nonmetals (covalent)."
""",

    'chem-ionic-covalent-properties-worked-example.yaml': """schemaVersion: 1
id: chem-ionic-covalent-properties-worked-example
title: "Properties of Ionic vs Covalent Compounds"
assessmentType: workedExample
categoryId: chemistry
topicId: chem-ionic-covalent-distinction
modeDefault: study
workedExamples:
  - id: we-bond-properties
    title: "Predicting Properties Based on Bond Type"
    problem: "You are given two unknown white powders, Substance A and Substance B. Substance A melts at 800°C and conducts electricity when dissolved in water. Substance B melts at 150°C and does not conduct electricity in water. Classify each substance as ionic or covalent."
    steps:
      - id: s1
        title: "Analyze Substance A"
        instruction: >
          High melting point (800°C) and electrical conductivity in solution are classic properties of **ionic** compounds. The strong electrostatic forces in the crystal lattice require high energy to break, and the free-moving ions in water allow for conductivity.
        type: freeResponse
        skills:
          - ionic-covalent-distinction
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s2
        title: "Analyze Substance B"
        instruction: >
          Low melting point (150°C) and lack of electrical conductivity are properties of **covalent** (molecular) compounds. The weak intermolecular forces are easy to break, and they do not form ions in solution to conduct electricity.
        type: freeResponse
        skills:
          - ionic-covalent-distinction
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
questions:
  - id: prop-predict
    title: "Conductivity Prediction"
    type: multipleChoice
    skills:
      - ionic-covalent-distinction
    prompt: "Why does solid NaCl not conduct electricity, but aqueous NaCl does?"
    choices:
      - id: a
        text: "Water provides electrons to the NaCl."
      - id: b
        text: "Solid NaCl is covalent, but it becomes ionic in water."
      - id: c
        text: "The ions are locked in a lattice in the solid, but are free to move in solution."
      - id: d
        text: "Solid NaCl does not have any charged particles."
    answer:
      choiceId: c
      explanation: "Conductivity requires charged particles that are free to move. In solid NaCl, the ions are rigidly held in the lattice. In water, they dissociate and move freely."
""",

    'chemistry-reactions-classification-concept-lesson.yaml': """schemaVersion: 1
id: chemistry-reactions-classification-concept-lesson
title: "Classifying Chemical Reactions"
assessmentType: conceptLesson
categoryId: chemistry
topicId: chemistry-reactions
modeDefault: study
lesson:
  introduction: "Chemical reactions can be grouped into several major categories based on how the atoms rearrange themselves. Identifying the reaction type helps predict the products."
  sections:
    - id: sec-1
      title: "Synthesis and Decomposition"
      content: >
        - **Synthesis (Combination)**: Two or more simple substances combine to form a more complex substance. 
          General Form: A + B -> AB
        
        - **Decomposition**: A complex substance breaks down into two or more simpler substances.
          General Form: AB -> A + B

    - id: sec-2
      title: "Replacement Reactions"
      content: >
        - **Single Replacement**: An uncombined element replaces an element that is part of a compound.
          General Form: A + BC -> AC + B
          
        - **Double Replacement**: Two compounds react, and their cations (or anions) switch places.
          General Form: AB + CD -> AD + CB

    - id: sec-3
      title: "Combustion"
      content: >
        A hydrocarbon (or other organic molecule) reacts with Oxygen gas (O2) to produce Carbon Dioxide (CO2) and Water (H2O).
questions:
  - id: reaction-class-1
    title: "Identify the Reaction Type"
    type: multipleChoice
    skills:
      - chemical-reactions-types
    prompt: "Classify the following reaction: Zn(s) + 2HCl(aq) -> ZnCl2(aq) + H2(g)"
    choices:
      - id: a
        text: "Synthesis"
      - id: b
        text: "Decomposition"
      - id: c
        text: "Single Replacement"
      - id: d
        text: "Double Replacement"
    answer:
      choiceId: c
      explanation: "Zinc (an uncombined element) is replacing Hydrogen in the compound HCl. This is a classic single replacement reaction."
""",

    'chemistry-reactions-classification-recall.yaml': """schemaVersion: 1
id: chemistry-reactions-classification-recall
title: "Reaction Classification Drill"
assessmentType: recallDrill
categoryId: chemistry
topicId: chemistry-reactions
modeDefault: practice
items:
  - id: rc-drill-1
    type: typed
    skills:
      - chemical-reactions-types
    prompt: "The reaction 2H2 + O2 -> 2H2O is an example of a _______ reaction."
    answer:
      expected: "synthesis"
      aliases:
        - "combination"
  - id: rc-drill-2
    type: typed
    skills:
      - chemical-reactions-types
    prompt: "The reaction CH4 + 2O2 -> CO2 + 2H2O is an example of a _______ reaction."
    answer:
      expected: "combustion"
  - id: rc-drill-3
    type: typed
    skills:
      - chemical-reactions-types
    prompt: "The reaction AgNO3 + NaCl -> AgCl + NaNO3 is an example of a _______ replacement reaction."
    answer:
      expected: "double"
  - id: rc-drill-4
    type: typed
    skills:
      - chemical-reactions-types
    prompt: "The reaction CaCO3 -> CaO + CO2 is an example of a _______ reaction."
    answer:
      expected: "decomposition"
""",

    'chemistry-solutions-concentration-concept-lesson.yaml': """schemaVersion: 1
id: chemistry-solutions-concentration-concept-lesson
title: "Solution Concentration: Molarity"
assessmentType: conceptLesson
categoryId: chemistry
topicId: chemistry-solutions
modeDefault: study
lesson:
  introduction: "A solution is a homogeneous mixture of a solute dissolved in a solvent. To quantify how much solute is present, chemists use concentration."
  sections:
    - id: sec-1
      title: "What is Molarity?"
      content: >
        Molarity (M) is the most common unit of concentration in chemistry. It is defined as the number of moles of solute per liter of solution.
        
        M = moles of solute / Liters of solution

    - id: sec-2
      title: "Preparing a Solution"
      content: >
        To prepare a 1.0 M solution of NaCl, you cannot just add 1.0 mole of NaCl to 1.0 Liter of water. Instead, you must add 1.0 mole of NaCl to a flask, and then add *enough water* until the **total volume** of the solution is 1.0 Liter.
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
assessmentType: workedExample
categoryId: chemistry
topicId: chemistry-solutions
modeDefault: study
workedExamples:
  - id: we-molarity
    title: "Calculating Molarity from Grams"
    problem: "What is the molarity of a solution prepared by dissolving 11.7 g of NaCl (molar mass = 58.44 g/mol) in enough water to make 500 mL of solution?"
    steps:
      - id: s1
        title: "Convert grams to moles"
        instruction: >
          Moles of NaCl = 11.7 g / 58.44 g/mol = 0.200 moles
        type: freeResponse
        skills:
          - solutions-molarity
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s2
        title: "Convert volume to Liters"
        instruction: >
          500 mL = 0.500 L
        type: freeResponse
        skills:
          - solutions-molarity
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s3
        title: "Calculate Molarity"
        instruction: >
          M = 0.200 moles / 0.500 L = 0.400 M
        type: freeResponse
        skills:
          - solutions-molarity
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
questions:
  - id: q-molarity-calc
    title: "Calculate Molarity"
    type: numericResponse
    skills:
      - solutions-molarity
    prompt: "If you have 0.50 moles of HCl in 2.0 L of solution, what is the molarity (M)?"
    answer:
      value: 0.25
      tolerance: 0
""",

    'chem-aqueous-solutions-solubility-rules-recall.yaml': """schemaVersion: 1
id: chem-aqueous-solutions-solubility-rules-recall
title: "Solubility Rules Drill"
assessmentType: recallDrill
categoryId: chemistry
topicId: chem-aqueous-solutions
modeDefault: practice
items:
  - id: sr-nitrates
    type: typed
    skills:
      - solubility-rules
    prompt: "Are all Nitrate salts soluble or insoluble in water?"
    answer:
      expected: "soluble"
  - id: sr-group1
    type: typed
    skills:
      - solubility-rules
    prompt: "Salts containing Group 1 alkali metals are always _______."
    answer:
      expected: "soluble"
  - id: sr-silver-chloride
    type: typed
    skills:
      - solubility-rules
    prompt: "Is Silver Chloride (AgCl) soluble or insoluble?"
    answer:
      expected: "insoluble"
  - id: sr-sulfates
    type: typed
    skills:
      - solubility-rules
    prompt: "Most sulfates are soluble, except those of Barium, Strontium, Lead, and _______."
    answer:
      expected: "calcium"
      aliases:
        - "mercury"
""",

    'chem-aqueous-solutions-net-ionic-equations-worked-example.yaml': """schemaVersion: 1
id: chem-aqueous-solutions-net-ionic-equations-worked-example
title: "Writing Net Ionic Equations"
assessmentType: workedExample
categoryId: chemistry
topicId: chem-aqueous-solutions
modeDefault: study
workedExamples:
  - id: we-net-ionic
    title: "Precipitation of Silver Chloride"
    problem: "Write the net ionic equation for the reaction between aqueous Silver Nitrate (AgNO3) and aqueous Sodium Chloride (NaCl)."
    steps:
      - id: s1
        title: "Write the balanced molecular equation"
        instruction: >
          AgNO3(aq) + NaCl(aq) -> AgCl(s) + NaNO3(aq)
        type: freeResponse
        skills:
          - net-ionic-equations
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s2
        title: "Write the complete ionic equation"
        instruction: >
          Break all (aq) strong electrolytes into their ions. Keep (s), (l), or (g) intact.
          
          Ag+(aq) + NO3-(aq) + Na+(aq) + Cl-(aq) -> AgCl(s) + Na+(aq) + NO3-(aq)
        type: freeResponse
        skills:
          - net-ionic-equations
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s3
        title: "Cancel spectator ions"
        instruction: >
          Na+ and NO3- appear on both sides, so they are spectator ions. Canceling them yields the net ionic equation:
          
          Ag+(aq) + Cl-(aq) -> AgCl(s)
        type: freeResponse
        skills:
          - net-ionic-equations
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
questions:
  - id: q-net-ionic-spec
    title: "Identify Spectator Ions"
    type: multipleChoice
    skills:
      - net-ionic-equations
    prompt: "In the reaction Pb(NO3)2(aq) + 2KI(aq) -> PbI2(s) + 2KNO3(aq), what are the spectator ions?"
    choices:
      - id: a
        text: "Pb2+ and I-"
      - id: b
        text: "K+ and NO3-"
      - id: c
        text: "Pb2+ and NO3-"
      - id: d
        text: "K+ and I-"
    answer:
      choiceId: b
      explanation: "Spectator ions are those that remain aqueous (dissolved) on both sides of the reaction. KNO3 is soluble, so K+ and NO3- are the spectator ions."
""",

    'chem-aqueous-solutions-precipitates-concept-lesson.yaml': """schemaVersion: 1
id: chem-aqueous-solutions-precipitates-concept-lesson
title: "Precipitation Reactions"
assessmentType: conceptLesson
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
        3. If one compound is insoluble, it forms a precipitate.
questions:
  - id: precip-predict
    title: "Will it precipitate?"
    type: multipleChoice
    skills:
      - solubility-rules
    prompt: "If you mix solutions of KCl and NaNO3, will a precipitate form?"
    choices:
      - id: a
        text: "Yes, KNO3 will precipitate."
      - id: b
        text: "Yes, NaCl will precipitate."
      - id: c
        text: "No precipitate will form."
    answer:
      choiceId: c
      explanation: "The possible products are KNO3 and NaCl. Both contain Group 1 metals (K, Na) and one contains Nitrate, meaning both are highly soluble in water. No solid forms."
""",

    'chem-acids-strong-weak-concept-lesson.yaml': """schemaVersion: 1
id: chem-acids-strong-weak-concept-lesson
title: "Strong vs Weak Acids"
assessmentType: conceptLesson
categoryId: chemistry
topicId: chem-acids
modeDefault: study
lesson:
  introduction: "Acids are substances that donate protons (H+) in aqueous solution. Their 'strength' refers to how completely they dissociate into ions."
  sections:
    - id: sec-1
      title: "Strong Acids"
      content: >
        Strong acids dissociate **100%** in water. The reaction goes to completion.
        
        Example: HCl(aq) -> H+(aq) + Cl-(aq)
        
        The six common strong acids are: HCl, HBr, HI, HNO3, H2SO4, HClO4.

    - id: sec-2
      title: "Weak Acids"
      content: >
        Weak acids dissociate only **partially** (often less than 5%) in water, establishing an equilibrium.
        
        Example: HF(aq) <-> H+(aq) + F-(aq)
questions:
  - id: strong-weak-id
    title: "Identifying Acid Strength"
    type: multipleChoice
    skills:
      - acid-base-strength
    prompt: "Which of the following is a weak acid?"
    choices:
      - id: a
        text: "HCl"
      - id: b
        text: "HNO3"
      - id: c
        text: "H2SO4"
      - id: d
        text: "CH3COOH (Acetic acid)"
    answer:
      choiceId: d
      explanation: "Acetic acid is not on the list of the 6 strong acids, making it a weak acid."
""",

    'chem-acids-ph-poh-worked-example.yaml': """schemaVersion: 1
id: chem-acids-ph-poh-worked-example
title: "Calculating pH and pOH"
assessmentType: workedExample
categoryId: chemistry
topicId: chem-acids
modeDefault: study
workedExamples:
  - id: we-ph-calc
    title: "Calculating pH from [H+]"
    problem: "What is the pH of a 0.0025 M solution of HCl?"
    steps:
      - id: s1
        title: "Determine [H+]"
        instruction: >
          Since HCl is a strong acid, it dissociates completely.
          
          [H+] = 0.0025 M
        type: freeResponse
        skills:
          - ph-calculations
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
      - id: s2
        title: "Apply the pH formula"
        instruction: >
          pH = -log[H+]
          
          pH = -log(0.0025) = 2.60
        type: freeResponse
        skills:
          - ph-calculations
        prompt: "Did you understand this step?"
        answer:
          gradingMode: selfCheck
questions:
  - id: q-poh-calc
    title: "Calculate pOH"
    type: numericResponse
    skills:
      - ph-calculations
    prompt: "If the pH of a solution is 4.5, what is its pOH? (Remember: pH + pOH = 14)"
    answer:
      value: 9.5
      tolerance: 0
""",

    'chem-acids-conjugate-pairs-recall.yaml': """schemaVersion: 1
id: chem-acids-conjugate-pairs-recall
title: "Conjugate Acid-Base Pairs Drill"
assessmentType: recallDrill
categoryId: chemistry
topicId: chem-acids
modeDefault: practice
items:
  - id: ca-drill-1
    type: typed
    skills:
      - conjugate-pairs
    prompt: "What is the conjugate base of HCl?"
    answer:
      expected: "Cl-"
  - id: ca-drill-2
    type: typed
    skills:
      - conjugate-pairs
    prompt: "What is the conjugate base of H2O?"
    answer:
      expected: "OH-"
  - id: ca-drill-3
    type: typed
    skills:
      - conjugate-pairs
    prompt: "What is the conjugate acid of NH3?"
    answer:
      expected: "NH4+"
  - id: ca-drill-4
    type: typed
    skills:
      - conjugate-pairs
    prompt: "What is the conjugate acid of H2O?"
    answer:
      expected: "H3O+"
"""
}

for filename, content in files.items():
    filepath = os.path.join("data/assessments", filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\\n')
print("All 20 files regenerated cleanly!")
