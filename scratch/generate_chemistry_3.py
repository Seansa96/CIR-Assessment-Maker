import os
OUT_DIR = "data/assessments"

FILES = {
    "chem-lewis-symbols-worked-example.yaml": """schemaVersion: 1
id: chem-lewis-symbols-worked-example
title: Drawing Lewis Structures
assessmentType: workedExample
categoryId: chemistry
subcategoryId: chem-lewis-symbols
subcategoryIds:
  - chem-lewis-symbols
modeDefault: practice
randomizeQuestions: false
workedExamples:
  - id: ex-lewis-water
    title: Drawing the Lewis Structure for Water ($H_2O$)
    problem: |
      Draw the Lewis structure for a water molecule ($H_2O$), a critical solvent in wet etching and electroplating processes.
    steps:
      - id: step-1
        title: Step 1 — Count total valence electrons
        instruction: |
          Oxygen is in Group 16 (6A) and each Hydrogen is in Group 1 (1A).
          Total valence electrons = 6 (from O) + 2 * 1 (from H).
        question:
          type: numericResponse
          prompt: "What is the total number of valence electrons for $H_2O$?"
          answer:
            numericValue: 8
            numericTolerance: 0
            expected: "8"
          explanation: "$6 + 2(1) = 8$ valence electrons."

      - id: step-2
        title: Step 2 — Draw the skeleton and connect with single bonds
        instruction: |
          Oxygen is the central atom because hydrogen can only form one bond (it only needs 2 electrons to fill its $1s$ orbital).
          Draw $H - O - H$.
          Each single bond represents 2 electrons. You've used 4 electrons so far.
        question:
          type: numericResponse
          prompt: "How many valence electrons remain to be placed?"
          answer:
            numericValue: 4
            numericTolerance: 0
            expected: "4"
          explanation: "$8$ total $- 4$ used in bonds $= 4$ remaining."

      - id: step-3
        title: Step 3 — Complete the octets
        instruction: |
          Place the remaining 4 electrons as lone pairs on the central oxygen atom to complete its octet.
        question:
          type: multipleChoice
          prompt: "How many lone pairs (unshared pairs) of electrons are on the central oxygen atom in the final structure?"
          choices:
            - id: a
              text: "0"
            - id: b
              text: "1"
            - id: c
              text: "2"
            - id: d
              text: "4"
          answer:
            choiceId: c
          explanation: "There are 4 non-bonding electrons, which make up 2 lone pairs."
""",

    "chem-semiconductors-recall.yaml": """schemaVersion: 1
id: chem-semiconductors-recall
title: Electrical Engineering Materials Recall
assessmentType: recallDrill
categoryId: chemistry
subcategoryId: chem-periodic-trends
subcategoryIds:
  - chem-periodic-trends
modeDefault: practice
items:
  - id: drill-silicon
    type: flashcard
    prompt: "Primary semiconductor element (Group 14) used in almost all integrated circuits"
    answer:
      expected: "Silicon (Si)"

  - id: drill-copper
    type: flashcard
    prompt: "Highly conductive transition metal commonly used for PCB traces and wiring"
    answer:
      expected: "Copper (Cu)"

  - id: drill-gaas
    type: flashcard
    prompt: "Compound semiconductor used in high-frequency LEDs and solar cells (made from Group 13 and Group 15 elements)"
    answer:
      expected: "Gallium Arsenide (GaAs)"

  - id: drill-lithium
    type: flashcard
    prompt: "Alkali metal (Group 1) widely used in rechargeable batteries due to its high electrochemical potential"
    answer:
      expected: "Lithium (Li)"

  - id: drill-germanium
    type: flashcard
    prompt: "Group 14 metalloid used in early transistors, often alloyed with Silicon"
    answer:
      expected: "Germanium (Ge)"
"""
}

def write_files():
    for filename, content in FILES.items():
        filepath = os.path.join(OUT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created {filepath}")

if __name__ == "__main__":
    write_files()
