import os
import textwrap

OUT_DIR = "data/assessments"

FILES = {
    # -------------------------------------------------------------
    # 1. Concept Lessons
    # -------------------------------------------------------------
    "chem-em-spectrum-lesson.yaml": """schemaVersion: 1
id: chem-em-spectrum-lesson
title: The Electromagnetic Spectrum Concept Lesson
assessmentType: conceptLesson
categoryId: chemistry
subcategoryId: chem-em-spectrum
subcategoryIds:
  - chem-em-spectrum
modeDefault: practice
randomizeQuestions: false
lesson:
  introduction: |
    Light is a form of electromagnetic radiation. It has wave-like properties, and we can describe it using its wavelength ($\\lambda$) and frequency ($\\nu$). The entire range of electromagnetic radiation is called the electromagnetic spectrum. In electrical engineering, we often work with specific bands of this spectrum, such as microwaves or radio waves for communication, or visible light for LEDs.
  sections:
    - id: section-1
      title: Wavelength, Frequency, and Speed
      required: true
      content: |
        The **wavelength** ($\\lambda$) is the distance between two consecutive peaks or troughs in a wave. It is usually measured in meters, though often expressed in nanometers (nm) for visible light.
        The **frequency** ($\\nu$) is the number of wave cycles that pass a given point per second, measured in Hertz (Hz) or $s^{-1}$.

        In a vacuum, all electromagnetic waves travel at the speed of light ($c = 3.00 \\times 10^8$ m/s). The relationship is:
        $$ c = \\lambda \\nu $$
        This means wavelength and frequency are **inversely proportional**.
      check:
        id: chem-em-spectrum-check-1
        type: multipleChoice
        prompt: "If a radio wave used for wireless transmission has a very low frequency, what can we say about its wavelength?"
        choices:
          - id: a
            text: "It has a very short wavelength."
          - id: b
            text: "It has a very long wavelength."
          - id: c
            text: "Its wavelength is zero."
          - id: d
            text: "Its wavelength is exactly $3.00 \\times 10^8$ meters."
        answer:
          choiceId: b
          keyPoints:
            - "Wavelength and frequency are inversely proportional."
        explanation: |
          Since $c = \\lambda \\nu$, if frequency $\\nu$ is low, the wavelength $\\lambda$ must be high (long) for the product to remain constant at the speed of light.

    - id: section-2
      title: Energy of a Photon
      required: true
      content: |
        Electromagnetic radiation can also be viewed as a stream of particles called **photons**. The energy of a single photon is directly proportional to its frequency, given by Planck's equation:
        $$ E = h \\nu $$
        where $h$ is Planck's constant ($6.626 \\times 10^{-34}$ J·s).

        Substituting $\\nu = \\frac{c}{\\lambda}$, we also have:
        $$ E = \\frac{hc}{\\lambda} $$
        Therefore, high-frequency (short-wavelength) light, like X-rays, has high energy. Low-frequency (long-wavelength) light, like microwaves, has low energy.
      check:
        id: chem-em-spectrum-check-2
        type: multipleChoice
        prompt: "Which of the following types of electromagnetic radiation carries the most energy per photon?"
        choices:
          - id: a
            text: "Red light ($\\lambda \\approx 700$ nm)"
          - id: b
            text: "Blue light ($\\lambda \\approx 400$ nm)"
          - id: c
            text: "Microwaves ($\\lambda \\approx 1$ cm)"
          - id: d
            text: "Infrared ($\\lambda \\approx 1000$ nm)"
        answer:
          choiceId: b
          keyPoints:
            - "Energy is inversely proportional to wavelength."
        explanation: |
          Energy $E = \\frac{hc}{\\lambda}$. The shortest wavelength among the choices is blue light ($400$ nm), so it has the highest frequency and the highest energy per photon.
""",
    
    "chem-bohr-model-lesson.yaml": """schemaVersion: 1
id: chem-bohr-model-lesson
title: Line Spectra and the Bohr Model Lesson
assessmentType: conceptLesson
categoryId: chemistry
subcategoryId: chem-bohr-model
subcategoryIds:
  - chem-bohr-model
modeDefault: practice
randomizeQuestions: false
lesson:
  introduction: |
    When atoms in a gas are excited by electricity (like in a neon sign) or heat, they emit light. If you pass this light through a prism, you don't see a continuous rainbow. Instead, you see a **line emission spectrum**—only specific wavelengths (colors) of light are emitted. The Bohr Model explains why.
  sections:
    - id: section-1
      title: The Bohr Model
      required: true
      content: |
        Niels Bohr proposed that electrons in a hydrogen atom move in circular orbits around the nucleus. Crucially, he stated that **only certain orbits with specific radii are allowed**. 

        Each allowed orbit corresponds to a specific energy level, denoted by a principal quantum number ($n = 1, 2, 3, \\dots$). The lowest energy level ($n=1$) is the **ground state**. When an electron absorbs energy, it can jump to a higher energy level, called an **excited state**.
      check:
        id: chem-bohr-check-1
        type: multipleChoice
        prompt: "According to the Bohr model, what happens to an electron when it absorbs a specific quantum of energy?"
        choices:
          - id: a
            text: "It falls into the nucleus."
          - id: b
            text: "It transitions to a higher, allowed energy level."
          - id: c
            text: "It spirals outward continuously."
          - id: d
            text: "It stops moving."
        answer:
          choiceId: b
          keyPoints:
            - "Energy absorption causes an electron to move to a higher energy level (excited state)."
        explanation: |
          When energy is absorbed, the electron jumps from a lower energy orbit to a higher energy orbit.

    - id: section-2
      title: Emission of Light
      required: true
      content: |
        Excited states are unstable. When an electron "falls" back down from a higher energy level to a lower one, it emits the excess energy as a single photon of light.

        The energy of the emitted photon exactly equals the energy difference between the two levels:
        $$ \\Delta E = E_{high} - E_{low} = h \\nu = \\frac{hc}{\\lambda} $$
        Because only specific energy levels exist, only specific energy transitions are possible. This is why we see discrete lines in an emission spectrum.

        Electrical engineers utilize this principle in designing LEDs and lasers. For example, Gallium Arsenide (GaAs) and Gallium Nitride (GaN) are engineered to have specific "band gaps" (analogous to energy level differences) so that electrons falling across the gap emit specific colors of light (like blue or red).
      check:
        id: chem-bohr-check-2
        type: multipleChoice
        prompt: "If an electron falls from $n=3$ to $n=2$ in a hydrogen atom, it emits red light. If an electron falls from $n=4$ to $n=2$, the energy difference is larger. What color of light might you expect?"
        choices:
          - id: a
            text: "Infrared light (lower energy)"
          - id: b
            text: "Blue or green light (higher energy)"
          - id: c
            text: "Radio waves"
          - id: d
            text: "Red light of exactly the same wavelength"
        answer:
          choiceId: b
          keyPoints:
            - "A larger energy transition corresponds to higher energy (higher frequency, shorter wavelength) light."
        explanation: |
          A larger energy drop ($\\Delta E$) means a higher frequency photon is emitted ($E = h \\nu$). Since blue/green light is higher frequency (higher energy) than red light, this is the logical expectation. (In fact, the $n=4 \\rightarrow n=2$ transition is the blue-green line in hydrogen's Balmer series).
""",

    "chem-quantum-model-lesson.yaml": """schemaVersion: 1
id: chem-quantum-model-lesson
title: The Quantum Model and Orbitals Lesson
assessmentType: conceptLesson
categoryId: chemistry
subcategoryId: chem-quantum-model
subcategoryIds:
  - chem-quantum-model
modeDefault: practice
randomizeQuestions: false
lesson:
  introduction: |
    While the Bohr model worked well for hydrogen, it failed for multi-electron atoms. The modern **Quantum Mechanical Model** replaces circular orbits with **orbitals**: 3D regions of space where there is a high probability of finding an electron. This probabilistic view is driven by Heisenberg's Uncertainty Principle.
  sections:
    - id: section-1
      title: Heisenberg and Probability
      required: true
      content: |
        The **Heisenberg Uncertainty Principle** states that it is impossible to simultaneously know both the exact position and the exact momentum of an electron. Because electrons exhibit wave-like behavior, we cannot pinpoint their exact path.

        Instead of an orbit, we use wave functions to calculate an **orbital**—a cloud-like region where the electron is likely to be found 90% of the time.
      check:
        id: chem-quantum-check-1
        type: multipleChoice
        prompt: "How does an orbital differ from a Bohr orbit?"
        choices:
          - id: a
            text: "An orbital is a 2D circle, while an orbit is a 3D sphere."
          - id: b
            text: "An orbit represents an exact circular path, while an orbital represents a 3D probability map."
          - id: c
            text: "Orbitals only exist for hydrogen, while orbits exist for all elements."
          - id: d
            text: "Orbitals contain protons, while orbits contain electrons."
        answer:
          choiceId: b
          keyPoints:
            - "Orbitals are probability regions; orbits are exact paths."
        explanation: |
          Due to the uncertainty principle, we can only talk about the *probability* of finding an electron in a certain 3D region (the orbital).

    - id: section-2
      title: Types of Orbitals (s, p, d, f)
      required: true
      content: |
        Energy levels (principal quantum number, $n$) are divided into sublevels: $s, p, d,$ and $f$. Each sublevel contains a specific number of orbitals, and each orbital can hold a maximum of 2 electrons.

        - **$s$ sublevel**: 1 spherical orbital (holds 2 electrons max)
        - **$p$ sublevel**: 3 dumbbell-shaped orbitals (holds 6 electrons max)
        - **$d$ sublevel**: 5 complex orbitals (holds 10 electrons max)
        - **$f$ sublevel**: 7 complex orbitals (holds 14 electrons max)

        The transition metals (like Copper and Cobalt) are located in the d-block and utilize d-orbitals. Semiconductors like Silicon ($3s^2 3p^2$) and Germanium ($4s^2 4p^2$) rely heavily on the overlap of their outer s and p orbitals to form the lattice structures essential to modern electronics.
      check:
        id: chem-quantum-check-2
        type: multipleChoice
        prompt: "What is the maximum number of electrons that can occupy a single $p$ sublevel entirely?"
        choices:
          - id: a
            text: "2"
          - id: b
            text: "6"
          - id: c
            text: "10"
          - id: d
            text: "14"
        answer:
          choiceId: b
          keyPoints:
            - "A $p$ sublevel contains 3 orbitals, each holding 2 electrons."
        explanation: |
          Since there are 3 $p$ orbitals ($p_x, p_y, p_z$) in a $p$ sublevel, and each holds up to 2 electrons, the sublevel can hold a total of 6 electrons.
""",

    "chem-electron-configs-lesson.yaml": """schemaVersion: 1
id: chem-electron-configs-lesson
title: Electron Configurations Concept Lesson
assessmentType: conceptLesson
categoryId: chemistry
subcategoryId: chem-electron-configs
subcategoryIds:
  - chem-electron-configs
modeDefault: practice
randomizeQuestions: false
lesson:
  introduction: |
    An **electron configuration** is a shorthand notation that describes how electrons are distributed among the various orbitals of an atom. Understanding this distribution is crucial for predicting chemical bonds, reactivity, and electrical conductivity.
  sections:
    - id: section-1
      title: Rules for Filling Orbitals
      required: true
      content: |
        We determine electron configurations using three main rules:
        1. **Aufbau Principle**: Electrons fill the lowest energy orbitals first (e.g., $1s$ before $2s$).
        2. **Pauli Exclusion Principle**: A maximum of two electrons can occupy a single orbital, and they must have opposite spins.
        3. **Hund's Rule**: When filling degenerate orbitals (like the three $p$ orbitals), put one electron into each orbital before pairing them up.

        For example, Carbon (6 electrons) is: $1s^2 2s^2 2p^2$.
      check:
        id: chem-config-check-1
        type: multipleChoice
        prompt: "According to Hund's Rule, how should the three electrons in the $2p$ sublevel of Nitrogen be arranged?"
        choices:
          - id: a
            text: "Two in the first $p$ orbital, one in the second, none in the third."
          - id: b
            text: "One in each of the three $p$ orbitals, all with parallel spins."
          - id: c
            text: "Three electrons in the first $p$ orbital."
          - id: d
            text: "They immediately jump to the $3s$ orbital."
        answer:
          choiceId: b
          keyPoints:
            - "Hund's rule maximizes unpaired electrons in degenerate orbitals."
        explanation: |
          To minimize electron-electron repulsion, one electron goes into each $p$ orbital ($p_x, p_y, p_z$) before any pairing occurs.

    - id: section-2
      title: Valence vs Core Electrons
      required: true
      content: |
        **Valence electrons** are the electrons in the outermost principal energy level ($n$). They are the electrons involved in bonding and determining the chemical properties of an element.
        **Core electrons** are the inner electrons.

        For example, Silicon (atomic number 14) has the configuration: $1s^2 2s^2 2p^6 3s^2 3p^2$.
        The highest energy level is $n=3$. Therefore, Si has $2 + 2 = 4$ valence electrons. The remaining 10 are core electrons. This tetravalency is exactly why Silicon forms crystalline structures critical for semiconductor doping.
      check:
        id: chem-config-check-2
        type: multipleChoice
        prompt: "How many valence electrons does Aluminum ($1s^2 2s^2 2p^6 3s^2 3p^1$) have?"
        choices:
          - id: a
            text: "1"
          - id: b
            text: "3"
          - id: c
            text: "13"
          - id: d
            text: "8"
        answer:
          choiceId: b
          keyPoints:
            - "Valence electrons are in the highest principle energy level."
        explanation: |
          The highest level is $n=3$. There are 2 electrons in $3s$ and 1 in $3p$, totaling 3 valence electrons.
""",

    "chem-lewis-symbols-lesson.yaml": """schemaVersion: 1
id: chem-lewis-symbols-lesson
title: Lewis Symbols and the Octet Rule Lesson
assessmentType: conceptLesson
categoryId: chemistry
subcategoryId: chem-lewis-symbols
subcategoryIds:
  - chem-lewis-symbols
modeDefault: practice
randomizeQuestions: false
lesson:
  introduction: |
    To visualize valence electrons, chemists use **Lewis symbols** (or electron dot diagrams). These symbols show the element's chemical symbol surrounded by dots representing its valence electrons. This helps us predict how atoms will interact to achieve stability.
  sections:
    - id: section-1
      title: Drawing Lewis Symbols
      required: true
      content: |
        For main-group elements, the number of valence electrons corresponds to the element's Group number (using the 1A-8A system). 
        
        To draw a Lewis symbol:
        1. Write the element's symbol.
        2. Determine the number of valence electrons (Group number).
        3. Place one dot on each of the four sides of the symbol (top, bottom, left, right) before pairing them up.

        For example, Phosphorus is in Group 15 (or 5A), so it has 5 valence electrons. You would place one dot on all four sides, and then pair one up, resulting in 1 pair and 3 unpaired dots.
      check:
        id: chem-lewis-check-1
        type: multipleChoice
        prompt: "How many dots would surround the symbol for Oxygen (Group 16 / 6A) in its Lewis symbol?"
        choices:
          - id: a
            text: "2"
          - id: b
            text: "4"
          - id: c
            text: "6"
          - id: d
            text: "8"
        answer:
          choiceId: c
          keyPoints:
            - "Group 16 elements have 6 valence electrons."
        explanation: |
          Oxygen is in Group 16 (6A) and has 6 valence electrons. Its Lewis symbol would have two pairs of dots and two single dots.

    - id: section-2
      title: The Octet Rule
      required: true
      content: |
        Noble gases (Group 18 / 8A) are exceptionally stable because their outermost $s$ and $p$ sublevels are completely full (8 valence electrons).

        The **Octet Rule** states that atoms tend to gain, lose, or share electrons until they are surrounded by eight valence electrons, achieving a noble gas configuration. 
        - **Metals** (like Lithium or Aluminum) tend to *lose* their few valence electrons to achieve an octet in the next lowest shell.
        - **Nonmetals** (like Oxygen or Chlorine) tend to *gain* or *share* electrons to complete their current shell.
      check:
        id: chem-lewis-check-2
        type: multipleChoice
        prompt: "To achieve an octet, what is the most likely behavior of an atom of Magnesium (Group 2 / 2A)?"
        choices:
          - id: a
            text: "Gain 6 electrons"
          - id: b
            text: "Lose 2 electrons"
          - id: c
            text: "Share 4 electrons"
          - id: d
            text: "Lose 8 electrons"
        answer:
          choiceId: b
          keyPoints:
            - "Metals with 1, 2, or 3 valence electrons typically lose them to achieve an octet."
        explanation: |
          Magnesium has 2 valence electrons. It is energetically much easier to lose 2 electrons (forming a $Mg^{2+}$ ion) than to gain 6.
""",

    "chem-ionic-bonds-lesson.yaml": """schemaVersion: 1
id: chem-ionic-bonds-lesson
title: Ionic Bonds and Compounds Concept Lesson
assessmentType: conceptLesson
categoryId: chemistry
subcategoryId: chem-ionic-bonds
subcategoryIds:
  - chem-ionic-bonds
modeDefault: practice
randomizeQuestions: false
lesson:
  introduction: |
    An **ionic bond** is the electrostatic attraction that holds oppositely charged ions together. Ionic compounds form when a metal transfers electrons to a nonmetal.
  sections:
    - id: section-1
      title: Electron Transfer
      required: true
      content: |
        When a metal reacts with a nonmetal, electrons are transferred. 
        For example, when Lithium (Li) reacts with Fluorine (F):
        - Lithium has 1 valence electron ($2s^1$). It loses it to become $Li^+$.
        - Fluorine has 7 valence electrons ($2s^2 2p^5$). It gains 1 to become $F^-$.
        
        The resulting $Li^+$ and $F^-$ ions are strongly attracted to each other. Because lithium-ion batteries rely on the movement of $Li^+$ ions between the anode and cathode, understanding ion formation is the core of modern battery technology.
      check:
        id: chem-ionic-check-1
        type: multipleChoice
        prompt: "When Aluminum (Group 13 / 3A) reacts with Oxygen (Group 16 / 6A), what ions are formed?"
        choices:
          - id: a
            text: "$Al^{3-}$ and $O^{2+}$"
          - id: b
            text: "$Al^{3+}$ and $O^{2-}$"
          - id: c
            text: "$Al^{+}$ and $O^{-}$"
          - id: d
            text: "$Al^{2+}$ and $O^{3-}$"
        answer:
          choiceId: b
          keyPoints:
            - "Metals lose electrons to become cations; nonmetals gain electrons to become anions."
        explanation: |
          Aluminum has 3 valence electrons and loses them to form $Al^{3+}$. Oxygen has 6 valence electrons and gains 2 to form $O^{2-}$.

    - id: section-2
      title: Predicting Ionic Formulas
      required: true
      content: |
        Ionic compounds are electrically neutral. Therefore, the total positive charge from the cations must perfectly balance the total negative charge from the anions.

        Using the Aluminum and Oxygen example ($Al^{3+}$ and $O^{2-}$):
        - We need two $Al^{3+}$ ions for a total charge of $+6$.
        - We need three $O^{2-}$ ions for a total charge of $-6$.
        - The formula is $Al_2O_3$ (Aluminum oxide, the material often used as an insulator or substrate in microelectronics).

        A quick trick is the **criss-cross method**: the numerical value of the cation's charge becomes the subscript for the anion, and vice versa. (Always reduce to the lowest whole number ratio).
      check:
        id: chem-ionic-check-2
        type: multipleChoice
        prompt: "What is the correct empirical formula for a compound made of Magnesium ($Mg^{2+}$) and Chlorine ($Cl^{-}$)?"
        choices:
          - id: a
            text: "$MgCl$"
          - id: b
            text: "$Mg_2Cl$"
          - id: c
            text: "$MgCl_2$"
          - id: d
            text: "$Mg_2Cl_2$"
        answer:
          choiceId: c
          keyPoints:
            - "Charges must balance to zero."
        explanation: |
          To balance the $+2$ charge of Magnesium, you need two $-1$ Chlorine ions. This gives $MgCl_2$.
""",

    "chem-covalent-bonds-lesson.yaml": """schemaVersion: 1
id: chem-covalent-bonds-lesson
title: Covalent Bonding Concept Lesson
assessmentType: conceptLesson
categoryId: chemistry
subcategoryId: chem-covalent-bonds
subcategoryIds:
  - chem-covalent-bonds
modeDefault: practice
randomizeQuestions: false
lesson:
  introduction: |
    Unlike ionic bonds where electrons are completely transferred, **covalent bonds** occur when atoms *share* electrons. This typically happens between two nonmetals.
  sections:
    - id: section-1
      title: Sharing to Reach an Octet
      required: true
      content: |
        When two nonmetals bond, neither is willing to completely give up an electron. Instead, they overlap their valence orbitals and share electron pairs.

        For example, in a Fluorine molecule ($F_2$), each F atom has 7 valence electrons. By sharing one pair of electrons between them, both atoms get to "count" the shared pair towards their own octet, resulting in 8 electrons for both.
        
        This shared pair of electrons is a **single covalent bond**, often represented by a line in Lewis structures (F—F).
      check:
        id: chem-covalent-check-1
        type: multipleChoice
        prompt: "In a single covalent bond, how many electrons are shared between two atoms?"
        choices:
          - id: a
            text: "1"
          - id: b
            text: "2"
          - id: c
            text: "4"
          - id: d
            text: "8"
        answer:
          choiceId: b
          keyPoints:
            - "A single bond consists of 1 shared pair of electrons."
        explanation: |
          A single bond represents one shared pair of electrons, which is a total of 2 electrons.

    - id: section-2
      title: Multiple Bonds
      required: true
      content: |
        Sometimes sharing one pair of electrons isn't enough to satisfy the octet rule for both atoms.
        
        - **Double bond**: Two atoms share two pairs (4 total) of electrons (e.g., $O_2$, O=O).
        - **Triple bond**: Two atoms share three pairs (6 total) of electrons (e.g., $N_2$, N$\\equiv$N).
        
        Multiple bonds are shorter and stronger than single bonds. Silicon, while capable of forming multiple bonds, primarily forms single covalent bonds in its crystal lattice ($Si$ bonded to four other $Si$ atoms), giving it its semiconducting properties.
      check:
        id: chem-covalent-check-2
        type: multipleChoice
        prompt: "Nitrogen (Group 15) has 5 valence electrons. How many electrons does a Nitrogen atom need to share in a diatomic $N_2$ molecule to achieve an octet?"
        choices:
          - id: a
            text: "1 pair (single bond)"
          - id: b
            text: "2 pairs (double bond)"
          - id: c
            text: "3 pairs (triple bond)"
          - id: d
            text: "4 pairs"
        answer:
          choiceId: c
          keyPoints:
            - "Nitrogen needs 3 more electrons, so it shares 3 pairs."
        explanation: |
          Since Nitrogen starts with 5 valence electrons, it needs 3 more to reach 8. It achieves this by forming a triple bond (sharing 3 pairs, or 6 electrons total).
""",

    "chem-acids-lesson.yaml": """schemaVersion: 1
id: chem-acids-lesson
title: Acids - An Introduction
assessmentType: conceptLesson
categoryId: chemistry
subcategoryId: chem-acids
subcategoryIds:
  - chem-acids
modeDefault: practice
randomizeQuestions: false
lesson:
  introduction: |
    Acids are a specific type of covalent compound that behave unusually when dissolved in water: they ionize to release hydrogen ions ($H^+$). Because they release charged ions into the solution, acids can act as electrolytes.
  sections:
    - id: section-1
      title: Recognizing Acids
      required: true
      content: |
        A compound is typically classified as an acid if its chemical formula starts with Hydrogen (e.g., $HCl, H_2SO_4, HNO_3$). 
        
        When these covalent molecules dissolve in water, the bond between hydrogen and the rest of the molecule breaks, leaving the electron behind. The hydrogen atom becomes an $H^+$ ion (a bare proton).

        In electrical engineering, understanding acid behavior is important for battery design (like the sulfuric acid in lead-acid batteries) and printed circuit board (PCB) etching (using acidic solutions to remove copper).
      check:
        id: chem-acids-check-1
        type: multipleChoice
        prompt: "Which of the following compounds is an acid?"
        choices:
          - id: a
            text: "$CH_4$"
          - id: b
            text: "$NaOH$"
          - id: c
            text: "$H_3PO_4$"
          - id: d
            text: "$NH_3$"
        answer:
          choiceId: c
          keyPoints:
            - "Acid formulas generally begin with H."
        explanation: |
          $H_3PO_4$ (phosphoric acid) begins with H. ($CH_4$ and $NH_3$ have hydrogen but are not acids; $NaOH$ is a base).

    - id: section-2
      title: Strong vs. Weak Acids
      required: true
      content: |
        Acids are classified by how completely they ionize in water.
        
        - **Strong Acids**: Ionize 100% in water. Every single acid molecule breaks apart into ions. They are strong electrolytes and conduct electricity extremely well. (There are 7 common strong acids: $HCl, HBr, HI, HNO_3, H_2SO_4, HClO_3, HClO_4$).
        - **Weak Acids**: Ionize only partially (often less than 5%). Most of the molecules remain intact. They are weak electrolytes. (e.g., Acetic acid, $CH_3COOH$).
      check:
        id: chem-acids-check-2
        type: multipleChoice
        prompt: "If you have a 1.0 M solution of a strong acid like Hydrochloric acid ($HCl$), what exists in the solution?"
        choices:
          - id: a
            text: "Mostly intact $HCl$ molecules"
          - id: b
            text: "Almost exclusively $H^+$ and $Cl^-$ ions"
          - id: c
            text: "Equal amounts of $HCl$ and ions"
          - id: d
            text: "Only water molecules"
        answer:
          choiceId: b
          keyPoints:
            - "Strong acids ionize completely."
        explanation: |
          Because $HCl$ is a strong acid, it dissociates 100%. Therefore, essentially no intact $HCl$ molecules remain; the solution is filled with $H^+$ and $Cl^-$ ions.
""",

    # -------------------------------------------------------------
    # 2. Worked Examples
    # -------------------------------------------------------------
    "chem-electron-configs-worked-example.yaml": """schemaVersion: 1
id: chem-electron-configs-worked-example
title: Writing Electron Configurations
assessmentType: workedExample
categoryId: chemistry
subcategoryId: chem-electron-configs
subcategoryIds:
  - chem-electron-configs
modeDefault: practice
randomizeQuestions: false
workedExamples:
  - id: ex-electron-configs
    title: Determining the configuration of Cobalt (Co)
    problem: |
      Write the full and noble gas shorthand electron configuration for Cobalt (Co), a metal commonly used in magnetic alloys and lithium-ion batteries.
    steps:
      - id: step-1
        title: Step 1 — Determine the number of electrons
        instruction: |
          Find Cobalt on the periodic table. Its atomic number tells you the number of protons, which is equal to the number of electrons in a neutral atom.
        question:
          type: numericResponse
          prompt: "What is the atomic number (and thus the number of electrons) for neutral Cobalt?"
          answer:
            numericValue: 27
            numericTolerance: 0
            expected: "27"
          explanation: "Cobalt (Co) is atomic number 27."

      - id: step-2
        title: Step 2 — Fill orbitals according to the Aufbau Principle
        instruction: |
          Follow the order of orbital filling: $1s, 2s, 2p, 3s, 3p, 4s, 3d$.
          Remember the maximum capacities: $s=2, p=6, d=10$.
          Keep a running tally until you hit 27 electrons.
          
          $1s^2$ (2 e-)
          $2s^2$ (4 e-)
          $2p^6$ (10 e-)
          $3s^2$ (12 e-)
          $3p^6$ (18 e-)
          $4s^2$ (20 e-)
          
          We need 7 more electrons. They go into the $3d$ sublevel.
        question:
          type: multipleChoice
          prompt: "What is the full electron configuration for Cobalt?"
          choices:
            - id: a
              text: "$1s^2 2s^2 2p^6 3s^2 3p^6 4s^2 3d^7$"
            - id: b
              text: "$1s^2 2s^2 2p^6 3s^2 3p^6 3d^9$"
            - id: c
              text: "$1s^2 2s^2 2p^6 3s^2 3p^6 4s^2 4p^7$"
          answer:
            choiceId: a
          explanation: "Filling order gives $1s^2 2s^2 2p^6 3s^2 3p^6 4s^2 3d^7$."

      - id: step-3
        title: Step 3 — Write the noble gas shorthand
        instruction: |
          To write the shorthand, find the noble gas in the period *above* Cobalt.
          Cobalt is in period 4, so look at the end of period 3. The noble gas is Argon (Ar), which has 18 electrons ($1s^2 2s^2 2p^6 3s^2 3p^6$).
          
          Replace that inner core portion of the configuration with $[Ar]$.
        question:
          type: multipleChoice
          prompt: "What is the noble gas shorthand configuration for Cobalt?"
          choices:
            - id: a
              text: "$[Kr] 4s^2 3d^7$"
            - id: b
              text: "$[Ar] 4s^2 3d^7$"
            - id: c
              text: "$[Ar] 3d^9$"
          answer:
            choiceId: b
          explanation: "The core is Argon ($18$ e-), leaving $4s^2 3d^7$."
""",

    "chem-ionic-formulas-worked-example.yaml": """schemaVersion: 1
id: chem-ionic-formulas-worked-example
title: Predicting Ionic Formulas
assessmentType: workedExample
categoryId: chemistry
subcategoryId: chem-ionic-bonds
subcategoryIds:
  - chem-ionic-bonds
modeDefault: practice
randomizeQuestions: false
workedExamples:
  - id: ex-ionic-formulas
    title: Aluminum Sulfide
    problem: |
      Predict the chemical formula for the ionic compound formed by Aluminum and Sulfur.
    steps:
      - id: step-1
        title: Step 1 — Determine the charge of the cation
        instruction: |
          Find Aluminum on the periodic table. It is a metal in Group 13 (3A). Metals lose their valence electrons to achieve an octet.
        question:
          type: multipleChoice
          prompt: "What ion will Aluminum form?"
          choices:
            - id: a
              text: "$Al^+$"
            - id: b
              text: "$Al^{2+}$"
            - id: c
              text: "$Al^{3+}$"
          answer:
            choiceId: c
          explanation: "Aluminum has 3 valence electrons. It loses all three to form $Al^{3+}$."

      - id: step-2
        title: Step 2 — Determine the charge of the anion
        instruction: |
          Find Sulfur on the periodic table. It is a nonmetal in Group 16 (6A). It has 6 valence electrons and needs to gain electrons to reach an octet (8).
        question:
          type: multipleChoice
          prompt: "What ion will Sulfur form?"
          choices:
            - id: a
              text: "$S^{6-}$"
            - id: b
              text: "$S^{2-}$"
            - id: c
              text: "$S^{-}$"
          answer:
            choiceId: b
          explanation: "Sulfur gains 2 electrons to reach 8, forming $S^{2-}$ (sulfide)."

      - id: step-3
        title: Step 3 — Balance the charges
        instruction: |
          You have $Al^{3+}$ and $S^{2-}$. The total charge must be zero. 
          The lowest common multiple of 3 and 2 is 6.
          You need two Aluminum ions ($2 \\times +3 = +6$).
          You need three Sulfide ions ($3 \\times -2 = -6$).
        question:
          type: multipleChoice
          prompt: "What is the final empirical formula for Aluminum Sulfide?"
          choices:
            - id: a
              text: "$AlS$"
            - id: b
              text: "$Al_3S_2$"
            - id: c
              text: "$Al_2S_3$"
          answer:
            choiceId: c
          explanation: "$Al_2S_3$ gives a perfectly neutral compound."
""",

    "chem-acids-naming-worked-example.yaml": """schemaVersion: 1
id: chem-acids-naming-worked-example
title: Naming Acids
assessmentType: workedExample
categoryId: chemistry
subcategoryId: chem-acids
subcategoryIds:
  - chem-acids
modeDefault: practice
randomizeQuestions: false
workedExamples:
  - id: ex-acids-naming
    title: Naming rules for binary vs oxyacids
    problem: |
      Determine the correct name for the acid $HNO_3$, a strong acid used heavily in etching and manufacturing explosives.
    steps:
      - id: step-1
        title: Step 1 — Determine the type of acid
        instruction: |
          Does the acid contain oxygen?
          - If NO: It is a binary acid. The name format is *hydro-* + root + *-ic acid*.
          - If YES: It is an oxyacid. Do not use the hydro- prefix.
        question:
          type: multipleChoice
          prompt: "Is $HNO_3$ a binary acid or an oxyacid?"
          choices:
            - id: a
              text: "Binary acid"
            - id: b
              text: "Oxyacid"
          answer:
            choiceId: b
          explanation: "It contains an oxygen atom (in fact, three), so it is an oxyacid."

      - id: step-2
        title: Step 2 — Identify the polyatomic anion
        instruction: |
          For an oxyacid, the name of the acid depends entirely on the name of the polyatomic anion inside it.
          Remove the $H^+$ to see the anion: $NO_3^{-}$.
        question:
          type: multipleChoice
          prompt: "What is the name of the $NO_3^{-}$ ion?"
          choices:
            - id: a
              text: "Nitride"
            - id: b
              text: "Nitrite"
            - id: c
              text: "Nitrate"
          answer:
            choiceId: c
          explanation: "$NO_3^{-}$ is the nitrate ion."

      - id: step-3
        title: Step 3 — Apply the suffix rule
        instruction: |
          Rule for oxyacids:
          - If the anion ends in **-ate**, change it to **-ic acid**. (I *ate* something *ic*ky).
          - If the anion ends in **-ite**, change it to **-ous acid**.
        question:
          type: multipleChoice
          prompt: "Given that the anion is 'nitrate', what is the name of $HNO_3$?"
          choices:
            - id: a
              text: "Hydronitric acid"
            - id: b
              text: "Nitrous acid"
            - id: c
              text: "Nitric acid"
          answer:
            choiceId: c
          explanation: "'Nitrate' ends in -ate, so it becomes 'Nitric acid'."
""",

    # -------------------------------------------------------------
    # 3. Recall Drills
    # -------------------------------------------------------------
    "chem-em-spectrum-recall.yaml": """schemaVersion: 1
id: chem-em-spectrum-recall
title: EM Spectrum & Equations Recall
assessmentType: recallDrill
categoryId: chemistry
subcategoryId: chem-em-spectrum
subcategoryIds:
  - chem-em-spectrum
modeDefault: practice
items:
  - id: drill-speed-of-light
    type: flashcard
    prompt: "Equation relating wavelength and frequency"
    answer:
      expected: "$c = \\lambda \\nu$"
      expectedLatex: "c = \\lambda \\nu"

  - id: drill-plancks-equation
    type: flashcard
    prompt: "Equation relating Energy to frequency"
    answer:
      expected: "$E = h \\nu$"
      expectedLatex: "E = h \\nu"

  - id: drill-spectrum-order
    type: flashcard
    prompt: "Order of the EM spectrum from lowest energy to highest energy"
    answer:
      expected: "Radio, Microwave, Infrared, Visible, Ultraviolet, X-ray, Gamma ray"
      aliases:
        - "Radio, Microwaves, IR, Visible, UV, X-rays, Gamma rays"
""",

    "chem-quantum-numbers-recall.yaml": """schemaVersion: 1
id: chem-quantum-numbers-recall
title: Orbitals and Sublevels Recall
assessmentType: recallDrill
categoryId: chemistry
subcategoryId: chem-quantum-model
subcategoryIds:
  - chem-quantum-model
modeDefault: practice
items:
  - id: drill-s-capacity
    type: flashcard
    prompt: "Max number of electrons in an $s$ sublevel"
    answer:
      expected: "2"

  - id: drill-p-capacity
    type: flashcard
    prompt: "Max number of electrons in a $p$ sublevel"
    answer:
      expected: "6"

  - id: drill-d-capacity
    type: flashcard
    prompt: "Max number of electrons in a $d$ sublevel"
    answer:
      expected: "10"

  - id: drill-f-capacity
    type: flashcard
    prompt: "Max number of electrons in an $f$ sublevel"
    answer:
      expected: "14"
""",

    "chem-polyatomic-ions-recall.yaml": """schemaVersion: 1
id: chem-polyatomic-ions-recall
title: Common Polyatomic Ions Recall
assessmentType: recallDrill
categoryId: chemistry
subcategoryId: chem-ions
subcategoryIds:
  - chem-ions
modeDefault: practice
items:
  - id: drill-nitrate
    type: flashcard
    prompt: "Nitrate formula and charge"
    answer:
      expected: "$NO_3^-$"
      expectedLatex: "NO_3^-"

  - id: drill-sulfate
    type: flashcard
    prompt: "Sulfate formula and charge"
    answer:
      expected: "$SO_4^{2-}$"
      expectedLatex: "SO_4^{2-}"

  - id: drill-carbonate
    type: flashcard
    prompt: "Carbonate formula and charge"
    answer:
      expected: "$CO_3^{2-}$"
      expectedLatex: "CO_3^{2-}"

  - id: drill-hydroxide
    type: flashcard
    prompt: "Hydroxide formula and charge"
    answer:
      expected: "$OH^-$"
      expectedLatex: "OH^-"

  - id: drill-phosphate
    type: flashcard
    prompt: "Phosphate formula and charge"
    answer:
      expected: "$PO_4^{3-}$"
      expectedLatex: "PO_4^{3-}"

  - id: drill-ammonium
    type: flashcard
    prompt: "Ammonium formula and charge"
    answer:
      expected: "$NH_4^+$"
      expectedLatex: "NH_4^+"
""",

    "chem-acids-recall.yaml": """schemaVersion: 1
id: chem-acids-recall
title: Strong Acids Recall
assessmentType: recallDrill
categoryId: chemistry
subcategoryId: chem-acids
subcategoryIds:
  - chem-acids
modeDefault: practice
items:
  - id: drill-hydrochloric
    type: flashcard
    prompt: "Hydrochloric Acid formula"
    answer:
      expected: "$HCl$"

  - id: drill-sulfuric
    type: flashcard
    prompt: "Sulfuric Acid formula"
    answer:
      expected: "$H_2SO_4$"

  - id: drill-nitric
    type: flashcard
    prompt: "Nitric Acid formula"
    answer:
      expected: "$HNO_3$"

  - id: drill-strong-acids
    type: flashcard
    prompt: "What are the 7 strong acids?"
    answer:
      expected: "$HCl, HBr, HI, HNO_3, H_2SO_4, HClO_3, HClO_4$"
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
