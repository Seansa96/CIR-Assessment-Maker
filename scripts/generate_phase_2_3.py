import os

files = {
    'chem-periodic-trends-concept-lesson.yaml': """schemaVersion: 1
id: chem-periodic-trends-concept-lesson
title: "Periodic Trends: Atomic Radius and Ionization Energy"
type: conceptLesson
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
type: conceptLesson
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
        
        Example: $Na \\rightarrow Na^+ + e^-$

    - id: sec-2
      title: "Anions (Negative Ions)"
      content: >
        Nonmetals tend to **gain** electrons to complete their valence shell. Gaining negatively charged electrons results in a **negative** charge.
        
        Example: $Cl + e^- \\rightarrow Cl^-$
questions:
  - id: ion-formation-1
    title: "Cation Identification"
    type: multipleChoice
    skills:
      - ion-formation
    prompt: "When a Magnesium (Mg) atom loses two electrons, what is the symbol for the resulting ion?"
    choices:
      - id: a
        text: "$Mg^{2-}$"
      - id: b
        text: "$Mg^-$"
      - id: c
        text: "$Mg^+$"
      - id: d
        text: "$Mg^{2+}$"
    answer:
      choiceId: d
      explanation: "Losing two negative electrons leaves the atom with a net positive charge of +2, written as $Mg^{2+}$."
""",
    'chem-ionic-covalent-distinction-concept-lesson.yaml': """schemaVersion: 1
id: chem-ionic-covalent-distinction-concept-lesson
title: "Distinguishing Ionic and Covalent Bonds"
type: conceptLesson
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
        
        The resulting oppositely charged ions attract each other via electrostatic forces, forming an ionic crystal lattice (e.g., $NaCl$).

    - id: sec-2
      title: "Covalent Bonds: Sharing of Electrons"
      content: >
        Covalent bonds occur when atoms **share** pairs of electrons to achieve stable electron configurations. This typically happens between two **nonmetals**.
        
        The shared electrons hold the atoms together in discrete molecules (e.g., $H_2O$, $CO_2$).
questions:
  - id: bond-type-id
    title: "Identifying Bond Types"
    type: multipleChoice
    skills:
      - ionic-covalent-distinction
    prompt: "Which of the following compounds is primarily ionic?"
    choices:
      - id: a
        text: "$CO_2$"
      - id: b
        text: "$MgCl_2$"
      - id: c
        text: "$H_2O$"
      - id: d
        text: "$CH_4$"
    answer:
      choiceId: b
      explanation: "$MgCl_2$ consists of a metal (Mg) and a nonmetal (Cl), making it an ionic compound. The others consist entirely of nonmetals (covalent)."
""",
    'chem-ionic-covalent-properties-worked-example.yaml': """schemaVersion: 1
id: chem-ionic-covalent-properties-worked-example
title: "Properties of Ionic vs Covalent Compounds"
type: workedExample
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
        content: >
          High melting point (800°C) and electrical conductivity in solution are classic properties of **ionic** compounds. The strong electrostatic forces in the crystal lattice require high energy to break, and the free-moving ions in water allow for conductivity.
      - id: s2
        title: "Analyze Substance B"
        content: >
          Low melting point (150°C) and lack of electrical conductivity are properties of **covalent** (molecular) compounds. The weak intermolecular forces are easy to break, and they do not form ions in solution to conduct electricity.
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
type: conceptLesson
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
          General Form: $A + B \\rightarrow AB$
        
        - **Decomposition**: A complex substance breaks down into two or more simpler substances.
          General Form: $AB \\rightarrow A + B$

    - id: sec-2
      title: "Replacement Reactions"
      content: >
        - **Single Replacement**: An uncombined element replaces an element that is part of a compound.
          General Form: $A + BC \\rightarrow AC + B$
          
        - **Double Replacement**: Two compounds react, and their cations (or anions) switch places.
          General Form: $AB + CD \\rightarrow AD + CB$

    - id: sec-3
      title: "Combustion"
      content: >
        A hydrocarbon (or other organic molecule) reacts with Oxygen gas ($O_2$) to produce Carbon Dioxide ($CO_2$) and Water ($H_2O$).
questions:
  - id: reaction-class-1
    title: "Identify the Reaction Type"
    type: multipleChoice
    skills:
      - reaction-classification
    prompt: "Classify the following reaction: $Zn(s) + 2HCl(aq) \\rightarrow ZnCl_2(aq) + H_2(g)$"
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
type: recallDrill
categoryId: chemistry
topicId: chemistry-reactions
modeDefault: practice
items:
  - id: rc-drill-1
    type: typed
    skills:
      - reaction-classification
    prompt: "The reaction $2H_2 + O_2 \\rightarrow 2H_2O$ is an example of a _______ reaction."
    answer:
      expected: "synthesis"
      aliases:
        - "combination"
  - id: rc-drill-2
    type: typed
    skills:
      - reaction-classification
    prompt: "The reaction $CH_4 + 2O_2 \\rightarrow CO_2 + 2H_2O$ is an example of a _______ reaction."
    answer:
      expected: "combustion"
  - id: rc-drill-3
    type: typed
    skills:
      - reaction-classification
    prompt: "The reaction $AgNO_3 + NaCl \\rightarrow AgCl + NaNO_3$ is an example of a _______ replacement reaction."
    answer:
      expected: "double"
  - id: rc-drill-4
    type: typed
    skills:
      - reaction-classification
    prompt: "The reaction $CaCO_3 \\rightarrow CaO + CO_2$ is an example of a _______ reaction."
    answer:
      expected: "decomposition"
"""
}

base_dir = "data/assessments"
for filename, content in files.items():
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
