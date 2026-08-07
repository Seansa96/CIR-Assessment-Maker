"""Generate the source-grounded Chemistry bonding learning bundles and contracts.

This permanent generator owns the canonical four-activity learning sequence for the
Chemical Bonding, Compounds, and Molecular Structure area. Learner wording is
original; the source is retained only as chunk provenance.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / "data" / "assessments"
REFERENCE = ROOT / "docs" / "assessment-reference"
SOURCE_ID = "src-20260720035703-91ea51b0d8"
SOURCE_SHA = "91ea51b0d87198f48679412a77bb9010f3296279b00b92b4a9e01ebcb37e6d0e"
SOURCE_DIR = ROOT / "data" / "source-library" / "sources" / SOURCE_ID


DEFINITIONS = {
    "valence electron": "An electron in the occupied outer shell that can participate in bonding or ion formation.",
    "Lewis symbol": "An element symbol surrounded by dots that represent its valence electrons.",
    "octet rule": "The useful main-group pattern in which atoms gain, lose, or share electrons to approach eight valence electrons.",
    "electron pair": "Two electrons occupying one Lewis-symbol side or one localized bonding or lone-pair region.",
    "unpaired electron": "A valence electron shown alone on one side of a Lewis symbol.",
    "lone pair": "A localized pair of valence electrons not shared between two atoms.",
    "bonding pair": "A pair of electrons shared between two bonded atoms.",
    "main-group element": "An element in the s or p blocks for which group position commonly predicts valence-electron count.",
    "noble-gas configuration": "A filled main-group valence shell matching the electron count of a nearby noble gas.",
    "Lewis ion symbol": "A bracketed Lewis symbol with the ion charge written outside the brackets.",
    "cation": "A positively charged species formed when the number of electrons is less than the number of protons.",
    "anion": "A negatively charged species formed when the number of electrons exceeds the number of protons.",
    "monatomic ion": "A charged species consisting of one atom.",
    "polyatomic ion": "A covalently connected group of atoms carrying a net charge.",
    "charge conservation": "The requirement that total electric charge remains the same before and after a process.",
    "isoelectronic": "Having the same number of electrons as another atom or ion.",
    "ionic bond": "Electrostatic attraction between oppositely charged ions in an ionic assembly.",
    "formula unit": "The lowest whole-number ratio of ions represented by an ionic compound formula.",
    "crystal lattice": "A repeating three-dimensional arrangement of particles in a crystalline solid.",
    "lattice energy": "The magnitude of the energy change associated with separating or assembling gaseous ions into an ionic solid.",
    "electrostatic attraction": "The force drawing opposite charges together and pushing like charges apart.",
    "coordination environment": "The neighboring ions surrounding a selected ion in a crystal.",
    "brittle": "Likely to fracture when displaced lattice layers bring like charges near one another.",
    "electrolyte": "A substance whose mobile ions allow a melt or solution to conduct electric current.",
    "covalent bond": "A bond produced by shared electron density between atoms.",
    "single bond": "One shared electron pair with bond order one.",
    "double bond": "Two shared electron pairs with bond order two.",
    "triple bond": "Three shared electron pairs with bond order three.",
    "bond order": "The number of shared electron pairs in a localized bond representation.",
    "bond length": "The internuclear distance at the minimum of a bond's potential-energy curve.",
    "bond energy": "The energy required to break a specified bond in the gas phase.",
    "shared pair": "A bonding electron pair counted by both bonded atoms in a Lewis representation.",
    "localized bond": "A model that assigns a bonding pair to a particular pair of atoms.",
    "molecule": "A discrete, electrically neutral collection of atoms joined by covalent bonds.",
    "network covalent solid": "An extended covalent structure without separate molecular units.",
    "ionic compound": "An electrically neutral substance made of cations and anions in a repeating assembly.",
    "molecular compound": "A substance composed of discrete covalently bonded molecules.",
    "conductivity": "The ability to carry electric current through mobile charged particles.",
    "melting point": "The temperature at which a solid and liquid coexist at a specified pressure.",
    "particle model": "A representation identifying the particles present and how they are connected or arranged.",
    "electronegativity": "An atom's tendency to attract shared electron density in a bond.",
    "bonding continuum": "The recognition that real bonds can have intermediate ionic and covalent character.",
    "empirical evidence": "Observed properties used to evaluate a proposed particle-level classification.",
    "composition rule": "A first-pass classification based on whether a formula contains metals, nonmetals, or recognized ions.",
}


def principle(identifier: str, title: str, content: str, correct: str, wrong_a: str, wrong_b: str) -> dict[str, str]:
    return {"id": identifier, "title": title, "content": content, "correct": correct, "wrongA": wrong_a, "wrongB": wrong_b}


FOUNDATIONS: dict[str, dict[str, Any]] = {
    "chem-lewis-symbols": {
        "title": "Lewis Symbols and the Octet Rule",
        "signal": "chemistry-bonding-valence-count-error",
        "chunks": ["0883", "0884", "0956"],
        "objective": "chem-bond-lewis-symbols",
        "visual": "/media/chemistry/bonding-lewis-symbol-workflow.svg",
        "principles": [
            principle("valence-count", "Count valence electrons", "For representative elements, the A-group position gives the usual valence-electron count. Core electrons are omitted because a Lewis symbol records the outer-shell inventory used in bonding.", "Sulfur is in group 6A, so its Lewis symbol contains six dots.", "Sulfur's atomic number requires sixteen Lewis dots.", "Sulfur receives two dots because it commonly forms a 2- ion."),
            principle("place-dots", "Place single dots before pairing", "Distribute one dot on each of four sides before making pairs. This bookkeeping mirrors the availability of unpaired valence electrons without claiming that a flat drawing is an orbital diagram.", "A five-electron symbol has one pair and three single dots.", "A five-electron symbol has two pairs and one single dot.", "All five dots belong on one side of the symbol."),
            principle("read-unpaired", "Interpret pairs and unpaired electrons", "The total dots give the valence count; their initial pairing pattern distinguishes lone pairs from unpaired electrons. Reorienting the sides does not create a different Lewis symbol.", "Nitrogen's five dots can be shown as one pair and three unpaired electrons.", "Nitrogen must show three pairs because it often forms three bonds.", "Rotating a Lewis symbol changes its electron count."),
            principle("ion-symbols", "Write Lewis symbols for ions", "Place an ion symbol in brackets, show the resulting valence shell, and write the charge outside. A main-group cation often loses its original valence dots, while a main-group anion commonly displays an octet.", "The oxide ion is bracketed with eight dots and a 2- charge.", "The oxide ion keeps oxygen's six dots because protons determine dots.", "The oxide ion is bracketed with two dots and a 2+ charge."),
            principle("octet-use", "Use the octet rule as a pattern", "The octet rule is a productive main-group model, not a universal law. It helps predict common ions and shared-pair structures but requires explicit exceptions for electron-deficient, odd-electron, and expanded-valence species.", "The octet rule is strongest as a main-group stability pattern with known exceptions.", "Every stable atom and molecule must contain exactly eight total electrons.", "Transition-metal compounds always follow a simple octet prediction."),
            principle("verify-symbol", "Verify the representation", "Check three things independently: the dot total matches the intended valence count, the pairing convention was followed, and any bracketed charge agrees with electron loss or gain.", "A chloride ion check gives eight dots and a 1- charge.", "A chloride ion check gives seven dots because chlorine has atomic number 17.", "A chloride ion check gives eight dots and a 1+ charge."),
        ],
        "terms": ["valence electron", "Lewis symbol", "octet rule", "electron pair", "unpaired electron", "lone pair", "bonding pair", "main-group element", "noble-gas configuration", "Lewis ion symbol", "cation", "anion", "monatomic ion", "charge conservation", "shared pair", "localized bond"],
        "examples": [
            ("Build and interpret sulfur's Lewis symbol", "Construct a Lewis symbol for sulfur and interpret its pairing pattern.", ["Locate sulfur in group 6A, giving six valence electrons.", "Place four single dots first, then pair two of them to obtain two pairs and two single dots.", "Verify six total dots; orientation may rotate, but the inventory and pairing pattern remain the same."]),
            ("Represent aluminum ion formation", "Use a Lewis symbol to represent formation of Al3+.", ["Neutral aluminum has three valence electrons because it is in group 3A.", "Removing three electrons leaves the common Al3+ cation with no displayed valence dots.", "Write the bracketed Al symbol with 3+ outside and verify that electron loss produces positive charge."]),
            ("Represent the oxide ion", "Construct and check the Lewis ion symbol for O2-.", ["Neutral oxygen begins with six valence electrons.", "Gaining two electrons completes an eight-electron outer shell.", "Bracket the eight-dot symbol with 2- outside; the two gained electrons account for the charge."]),
        ],
    },
    "chem-ions": {
        "title": "Ions",
        "signal": "chemistry-bonding-ion-charge-error",
        "chunks": ["0233", "0234", "0235", "0238", "0239"],
        "objective": "chem-bond-ions",
        "visual": "/media/chemistry/bonding-ion-formation-map.svg",
        "principles": [
            principle("charge-accounting", "Relate charge to protons and electrons", "Net charge equals positive proton charge plus negative electron charge. Changing electron count forms an ion; ordinary chemical ion formation does not change the nucleus.", "Losing two electrons forms a 2+ ion.", "Losing two electrons forms a 2- ion.", "Gaining two protons is the usual way to form an anion."),
            principle("cation-anion", "Distinguish cations and anions", "Cations contain fewer electrons than protons and are positive. Anions contain more electrons than protons and are negative. The sign describes the imbalance, not whether the species is attracted to an electrode in a particular diagram.", "A species with 12 protons and 10 electrons is a 2+ cation.", "A species with 12 protons and 10 electrons is a 2- anion.", "The species is neutral because both counts are even."),
            principle("main-group-charges", "Predict common main-group charges", "Metals on the left commonly lose their few valence electrons, while nonmetals near the right commonly gain enough electrons to approach a noble-gas count. State these as common patterns rather than universal oxidation states.", "Magnesium commonly forms Mg2+ by losing two electrons.", "Magnesium commonly forms Mg2- by gaining two electrons.", "Magnesium commonly forms Mg6+ to expose six core electrons."),
            principle("electron-config", "Check the resulting electron count", "A predicted monatomic ion should have an electron count consistent with the stated charge and, for many main-group ions, a nearby noble-gas configuration.", "Na+ and Ne are isoelectronic with ten electrons.", "Na+ and Ar are isoelectronic with eighteen electrons.", "Na+ retains all eleven electrons because charge changes protons."),
            principle("polyatomic", "Treat a polyatomic ion as one charged unit", "A polyatomic ion contains covalent bonds internally but carries a net charge as a whole. Preserve its atom grouping when counting units in a formula.", "Nitrate is a three-oxygen polyatomic anion with an overall 1- charge.", "Each atom in nitrate separately carries the full 1- ion charge.", "A polyatomic ion cannot appear inside an ionic compound."),
            principle("conserve-charge", "Conserve total charge", "Any formula or electron-transfer description must have the required net charge. For a neutral compound, total positive and negative contributions cancel exactly.", "One Ca2+ requires two Cl- ions for a neutral combination.", "One Ca2+ requires one Cl- because there are two element symbols.", "Two Ca2+ ions and one Cl- ion give a neutral combination."),
        ],
        "terms": ["cation", "anion", "monatomic ion", "polyatomic ion", "charge conservation", "isoelectronic", "valence electron", "noble-gas configuration", "Lewis ion symbol", "main-group element", "octet rule", "formula unit", "ionic compound", "composition rule", "electron pair", "electrostatic attraction"],
        "examples": [
            ("Determine magnesium ion charge", "Predict magnesium's common monatomic ion and verify its electron count.", ["Magnesium has two valence electrons outside a neon core.", "Losing those two electrons gives 12 protons and 10 electrons, so the charge is 2+.", "Write Mg2+ and verify that it is isoelectronic with neon."]),
            ("Determine nitride ion charge", "Predict the common ion formed by nitrogen.", ["Nitrogen has five valence electrons and needs three more to reach an octet.", "Gaining three electrons gives three more electrons than protons, so the charge is 3-.", "Write N3- and verify that the resulting ten-electron count matches neon."]),
            ("Balance ions in calcium nitrate", "Determine the neutral formula made from Ca2+ and nitrate, NO3-.", ["Treat nitrate as one polyatomic unit carrying 1- charge.", "Two nitrate ions provide 2- total charge to balance one Ca2+.", "Write Ca(NO3)2 and verify both charge cancellation and preservation of each nitrate group."]),
        ],
    },
    "chem-ionic-bonds": {
        "title": "Ionic Bonds and Compounds",
        "signal": "chemistry-bonding-ionic-model-error",
        "chunks": ["0885", "0886", "0887", "0890", "0893", "0895", "0898"],
        "objective": "chem-bond-ionic",
        "visual": "/media/chemistry/bonding-ionic-lattice-map.svg",
        "principles": [
            principle("transfer-attraction", "Connect electron transfer to attraction", "Electron transfer describes ion formation, while the ionic bond is the electrostatic attraction among the resulting oppositely charged ions. Do not draw one transferred electron as a permanent physical connector.", "NaCl formation produces Na+ and Cl- whose opposite charges attract.", "The transferred electron becomes a rigid rod joining one sodium to one chlorine.", "Na and Cl remain neutral but acquire an ionic label."),
            principle("lattice", "Model the extended lattice", "An ionic solid is an extended array, not a collection of isolated NaCl molecules. Its formula states the lowest charge-balanced ratio of ions.", "Solid MgCl2 contains a repeating 1:2 ratio of Mg2+ to Cl-.", "Each MgCl2 molecule contains one isolated magnesium-chlorine-chlorine unit.", "The formula means every magnesium touches exactly two chloride ions."),
            principle("properties", "Explain characteristic properties", "Strong lattice attractions contribute to high melting points. Ions are fixed in a solid but mobile in a melt or aqueous solution, explaining the change in conductivity.", "Molten NaCl conducts because its ions can move.", "Solid NaCl conducts best because its ions are locked in place.", "NaCl melts easily because opposite charges repel."),
            principle("brittleness", "Explain brittleness", "A displacement can align like-charged ions across a cleavage plane. Their repulsion drives the crystal apart rather than allowing layers to slide as in a metal.", "Shifting an ionic lattice can place like charges together and fracture it.", "Ionic crystals are brittle because all ionic attractions disappear at room temperature.", "Brittleness proves the solid contains neutral molecules."),
            principle("lattice-trends", "Predict qualitative lattice-energy trends", "Greater ionic charge and shorter ion separation strengthen electrostatic attraction. Compare one factor at a time and state that lattice energy is a property of the full ionic assembly.", "CaO is expected to have stronger lattice attraction than NaF because its ions have larger charge magnitudes.", "CsI must have stronger attraction than NaF because cesium and iodine are larger.", "Lattice energy is found by multiplying the two ion masses."),
            principle("energy-cycle", "Account for the complete formation process", "Forming separated ions can require energy, but assembling the lattice releases energy. A valid energetic argument includes both ion formation and lattice stabilization.", "Lattice formation can offset endothermic electron-removal steps.", "Electron transfer alone guarantees every ionic compound forms exothermically.", "Only atomic mass determines whether an ionic solid is stable."),
        ],
        "terms": ["ionic bond", "ionic compound", "formula unit", "crystal lattice", "lattice energy", "electrostatic attraction", "coordination environment", "brittle", "electrolyte", "cation", "anion", "charge conservation", "noble-gas configuration", "melting point", "conductivity", "particle model"],
        "examples": [
            ("Trace sodium chloride formation", "Connect electron transfer, ion formation, and lattice attraction for NaCl.", ["Sodium loses one electron to form Na+, while chlorine gains one to form Cl-.", "The 1+ and 1- charges require a 1:1 formula ratio.", "Describe solid NaCl as a repeating lattice stabilized by attractions in many directions, not isolated molecules."]),
            ("Compare lattice attraction", "Compare NaF, CsI, and CaO qualitatively.", ["NaF and CsI have the same charge product, so ion size distinguishes them; smaller NaF has stronger attraction.", "CaO has 2+ and 2- ions, giving a larger charge product than either 1+/1- salt.", "The expected increasing attraction is CsI, NaF, CaO; verify that both charge and distance were considered."]),
            ("Explain calcium chloride properties", "Relate CaCl2 composition and behavior to its particle model.", ["One Ca2+ requires two Cl- ions, so the formula unit is CaCl2.", "In the solid, ions occupy fixed lattice positions and cannot carry current through bulk motion.", "When molten or dissolved, mobile ions conduct; a shifted crystal can fracture when like charges align."]),
        ],
    },
    "chem-covalent-bonds": {
        "title": "Covalent Bonding",
        "signal": "chemistry-bonding-covalent-pair-error",
        "chunks": ["0900", "0901", "0902", "0903"],
        "objective": "chem-bond-covalent",
        "visual": "/media/chemistry/bonding-shared-pair-map.svg",
        "principles": [
            principle("shared-density", "Interpret shared electron density", "A covalent bond concentrates electron density between nuclei. In a Lewis model, one shared pair is represented by two dots or one line and is counted toward both atoms' valence shells.", "The H-H bond contains one shared pair between the nuclei.", "Each hydrogen permanently transfers one electron to the other.", "A bond line represents one proton shared by both atoms."),
            principle("single-bond", "Recognize single bonds", "A single bond contains one shared pair and has bond order one. Additional nonbonding valence electrons remain as lone pairs on the appropriate atoms.", "A Cl-Cl single bond is one shared pair plus three lone pairs on each chlorine.", "A Cl-Cl single bond contains three shared pairs.", "Chlorine loses every lone pair when it forms one bond."),
            principle("multiple-bonds", "Recognize multiple bonds", "When one shared pair does not complete the needed valence shells, atoms may share two or three pairs. A double bond has order two and a triple bond has order three.", "The N2 triple bond contains three shared pairs.", "A double bond contains one shared pair drawn with two lines.", "Bond order counts the atoms rather than shared pairs."),
            principle("bond-order-trends", "Relate order, length, and strength", "For the same atom pair, increasing bond order generally shortens and strengthens the bond because more shared density lies between the nuclei.", "A C=C bond is generally shorter and stronger than a C-C bond.", "A C=C bond is longer because it contains more electrons.", "Bond order has no relationship to length or strength."),
            principle("lone-pairs", "Keep lone pairs in the electron inventory", "Bond lines show shared pairs only. Remaining valence electrons must be placed as lone pairs so the total count and expected shells are satisfied.", "Water has two O-H bonding pairs and two lone pairs on oxygen.", "Water's four electron pairs are all shared between oxygen and hydrogen.", "Hydrogen carries two lone pairs in water."),
            principle("model-limits", "State the model's limits", "A localized Lewis structure is excellent electron bookkeeping but does not display orbital shape, exact electron density, resonance averaging, or a molecule's full three-dimensional geometry.", "A Lewis structure needs other models to predict three-dimensional shape.", "A Lewis structure is a measured photograph of stationary electrons.", "Every bond must be purely ionic or purely covalent in a Lewis drawing."),
        ],
        "terms": ["covalent bond", "shared pair", "bonding pair", "lone pair", "single bond", "double bond", "triple bond", "bond order", "bond length", "bond energy", "localized bond", "molecule", "valence electron", "octet rule", "electron pair", "network covalent solid"],
        "examples": [
            ("Account for bonding in chlorine", "Build the shared-pair description of Cl2.", ["Each chlorine supplies seven valence electrons, for fourteen total.", "Place one shared pair between the atoms and three lone pairs on each chlorine.", "Verify fourteen electrons and an octet around each chlorine; the Cl-Cl bond order is one."]),
            ("Build the nitrogen triple bond", "Explain why N2 requires a triple bond in a localized octet structure.", ["Two nitrogen atoms contribute ten valence electrons.", "Three shared pairs give each nitrogen six bonding electrons, while one lone pair remains on each atom.", "Verify ten electrons total and assign bond order three."]),
            ("Compare carbon-carbon bonds", "Compare C-C, C=C, and C triple C using bond order.", ["Assign bond orders one, two, and three from the number of shared pairs.", "For the same atom pair, predict decreasing length as bond order increases.", "Predict increasing strength with bond order, while noting that exact energies require measured data."]),
        ],
    },
    "chem-ionic-covalent-distinction": {
        "title": "Distinguishing Ionic and Covalent Compounds",
        "signal": "chemistry-bonding-classification-error",
        "chunks": ["0226", "0233", "0238", "0239", "0885", "0900", "0904", "0917"],
        "objective": "chem-bond-classification",
        "visual": "/media/chemistry/bonding-classification-evidence.svg",
        "principles": [
            principle("composition", "Use composition as a first pass", "A metal combined with a nonmetal or a formula containing recognized cations and anions usually indicates an ionic compound. Only nonmetals usually indicate a molecular or network-covalent substance.", "K2S is classified as ionic from K+ and S2- ions.", "K2S is molecular because it contains two element symbols.", "Every compound containing oxygen is ionic."),
            principle("particle-unit", "Identify the representative particle", "Ionic formulas describe ratios in an extended lattice; molecular formulas describe discrete molecules. Network covalent solids are extended but do not consist of ions.", "CO2 commonly represents discrete molecules, while NaCl represents a formula-unit ratio.", "NaCl consists of isolated NaCl molecules in its crystal.", "Every extended solid must be ionic."),
            principle("properties", "Use properties as evidence", "High melting point and conduction when molten or dissolved support mobile-ion behavior. Low melting molecular substances and poor electrical conduction support neutral particles, but no single property should be treated as conclusive alone.", "A high-melting solid that conducts when molten is consistent with an ionic model.", "Any solid that fails to conduct is necessarily molecular.", "A low melting point proves a substance contains metal ions."),
            principle("solutions", "Interpret conductivity carefully", "An ionic substance conducts in solution only if it dissolves and produces mobile ions. Some molecular substances react with water to form ions, so solution conductivity must be combined with chemical evidence.", "Conducting aqueous HCl does not mean pure HCl is an ionic lattice.", "Every conducting solution came from an ionic solid.", "Dissolving always leaves particles electrically neutral."),
            principle("continuum", "Avoid a rigid cutoff", "Electronegativity difference can support a bond-polarity argument, but bonding character is a continuum and bulk classification also depends on structure and particle organization.", "Electronegativity difference is evidence, not an infallible classification threshold.", "A difference of exactly 1.7 changes every bond discontinuously from covalent to ionic.", "Electronegativity cannot influence bonding character."),
            principle("exceptions", "Handle polyatomic and network cases", "A compound such as NH4NO3 is ionic between polyatomic ions even though every atom is a nonmetal. Diamond and SiO2 are extended covalent structures rather than molecular or ionic lattices.", "NH4NO3 contains covalent bonds within ions and ionic attraction between ions.", "NH4NO3 must be molecular because it contains no metal.", "SiO2 consists of separate triatomic molecules in quartz."),
        ],
        "terms": ["ionic compound", "molecular compound", "network covalent solid", "formula unit", "molecule", "particle model", "conductivity", "melting point", "electrolyte", "composition rule", "empirical evidence", "electronegativity", "bonding continuum", "polyatomic ion", "ionic bond", "covalent bond"],
        "examples": [
            ("Classify sodium chloride and carbon dioxide", "Use composition, particle model, and properties rather than one clue.", ["NaCl combines a metal and nonmetal and is modeled as Na+ and Cl- in a lattice.", "CO2 contains only nonmetals and exists as discrete covalent molecules under ordinary conditions.", "Use melting and conductivity evidence to support, not replace, the particle-level classifications."]),
            ("Classify quartz", "Decide whether solid SiO2 is ionic, molecular, or network covalent.", ["Silicon and oxygen form an extended connected structure rather than discrete SiO2 molecules.", "The atoms are connected by covalent bonds and are not organized as simple Si4+ and O2- ions.", "Classify quartz as network covalent and explain why its high melting point alone does not make it ionic."]),
            ("Analyze ammonium nitrate", "Classify NH4NO3 even though it contains only nonmetals.", ["Recognize NH4+ and NO3- as charged polyatomic units.", "Covalent bonds hold atoms together within each ion, while opposite ion charges attract between units.", "Classify the compound as ionic overall and reject a composition-only nonmetal shortcut."]),
        ],
    },
}


def mc_check(topic: dict[str, Any], section: dict[str, str], index: int) -> dict[str, Any]:
    return {
        "id": f"chk-{section['id']}",
        "type": "multipleChoice",
        "prompt": f"Which statement correctly applies the idea of {section['title'].lower()}?",
        "choices": [
            {"id": "a", "text": section["correct"], "issueSignals": []},
            {"id": "b", "text": section["wrongA"], "issueSignals": [{"id": topic["signal"]}]},
            {"id": "c", "text": section["wrongB"], "issueSignals": [{"id": topic["signal"]}]},
        ],
        "answer": {"choiceId": "a"},
        "explanation": f"Solution: {section['correct']} Why it works: {section['content']} Why the other choices fail: The other statements either reverse the relevant electron or charge accounting or apply a structural model outside its stated scope.",
    }


def concept_assessment(topic_id: str, topic: dict[str, Any]) -> dict[str, Any]:
    sections = []
    for i, item in enumerate(topic["principles"], 1):
        section = {
            "id": item["id"], "title": item["title"], "required": True,
            "content": item["content"], "check": mc_check(topic, item, i),
        }
        if i == 1:
            section["media"] = [{"type": "image", "src": topic["visual"], "alt": f"Instructional workflow for {topic['title'].lower()} showing the central particle-level decisions.", "caption": "Use the representation to connect observable evidence with electron and particle accounting."}]
        sections.append(section)
    return {
        "schemaVersion": 1, "id": f"{topic_id}-concept-lesson", "title": f"{topic['title']}: Concept Lesson",
        "assessmentType": "conceptLesson", "categoryId": "chemistry", "topicId": topic_id,
        "skills": ["Apply chemistry concepts", topic["title"]],
        "navigation": {"learningGoal": "learn", "activityType": "conceptLesson", "tags": ["chemistry", topic_id]},
        "modeDefault": "practice", "randomizeQuestions": False,
        "authoring": {"visualRequirement": "required", "visualRationale": "A particle or electron-level representation supports the topic's core decisions.", "sourceId": SOURCE_ID},
        "lesson": {"introduction": f"Build a reliable model of {topic['title'].lower()} by separating electron accounting, particle representation, and observable evidence.", "sections": sections},
    }


def glossary_assessment(topic_id: str, topic: dict[str, Any]) -> dict[str, Any]:
    entries = []
    for i, term in enumerate(topic["terms"], 1):
        definition = DEFINITIONS[term]
        entries.append({
            "id": f"term-{i:02d}", "term": term, "definition": definition,
            "drills": [{
                "id": f"g{i:02d}", "type": "flashcard",
                "prompt": f"State the meaning of {term} in this bonding unit.",
                "answer": {"expected": definition, "aliases": [term]},
                "explanation": f"Solution: {definition} Why it works: This meaning keeps the term tied to the particle or electron model used in the topic.",
            }],
        })
    return {
        "schemaVersion": 1, "id": f"{topic_id}-glossary", "title": f"{topic['title']} Glossary",
        "assessmentType": "glossary", "categoryId": "chemistry", "topicId": topic_id,
        "navigation": {"learningGoal": "learn", "activityType": "glossary", "tags": ["chemistry", topic_id]},
        "modeDefault": "practice", "randomizeQuestions": False,
        "authoring": {"visualRequirement": "notApplicable", "visualRationale": "The glossary reinforces definitions already represented in the concept visual.", "sourceId": SOURCE_ID},
        "glossary": {"introduction": "Use each term precisely enough to distinguish a symbol, a particle, an interaction, and an observed property.", "sections": [{"id": "core-terms", "title": "Core terms", "required": True, "content": "Connect each definition to a representation or decision from the lesson.", "entries": entries}]},
    }


def worked_assessment(topic_id: str, topic: dict[str, Any]) -> dict[str, Any]:
    examples = []
    for e_i, (title, problem, solutions) in enumerate(topic["examples"], 1):
        steps = []
        for s_i, solution in enumerate(solutions, 1):
            steps.append({
                "id": f"we{e_i}-step{s_i}", "title": f"Step {s_i}",
                "instruction": "Record the relevant electron, charge, particle, or evidence decision before continuing.",
                "type": "freeResponse", "prompt": f"Explain step {s_i} of the analysis in your own words.",
                "answer": {"gradingMode": "selfCheck", "keyPoints": [solution]},
                "explanation": f"Solution: {solution} Why it works: This step follows the topic's accounting rules and supplies a separate check before the final conclusion.",
            })
        examples.append({"id": f"example-{e_i}", "title": title, "problem": problem, "steps": steps})
    return {
        "schemaVersion": 1, "id": f"{topic_id}-worked-examples", "title": f"{topic['title']}: Worked Examples",
        "assessmentType": "workedExample", "categoryId": "chemistry", "topicId": topic_id,
        "skills": ["Apply chemistry concepts", topic["title"]],
        "navigation": {"learningGoal": "learn", "activityType": "guidedWorkedExample", "tags": ["chemistry", topic_id]},
        "modeDefault": "study", "randomizeQuestions": False,
        "authoring": {"visualRequirement": "required", "visualRationale": "The examples apply the same particle-level visual used by the lesson.", "sourceId": SOURCE_ID},
        "workedExamples": examples,
    }


def recall_assessment(topic_id: str, topic: dict[str, Any]) -> dict[str, Any]:
    prompts = [
        "Define {term} and name the representation in which it is used.",
        "What does {term} tell you to count or distinguish?",
        "State one condition that must be checked when using {term}.",
        "Connect {term} to an observable or particle-level consequence.",
    ]
    items = []
    for i, term in enumerate(topic["terms"][:12], 1):
        definition = DEFINITIONS[term]
        items.append({
            "id": f"r{i:03d}", "type": "typed", "prompt": prompts[(i - 1) % len(prompts)].format(term=term),
            "answer": {"expected": definition, "aliases": [term]},
            "explanation": f"Solution: {definition} Why it works: The definition identifies the exact model feature needed before applying a rule or drawing a conclusion.",
        })
    return {
        "schemaVersion": 1, "id": f"{topic_id}-recall-drill", "title": f"{topic['title']} Recall Drill",
        "assessmentType": "recallDrill", "categoryId": "chemistry", "topicId": topic_id,
        "navigation": {"learningGoal": "recall", "activityType": "mixedRecallSet", "tags": ["chemistry", topic_id]},
        "modeDefault": "practice", "randomizeQuestions": True,
        "authoring": {"visualRequirement": "notApplicable", "visualRationale": "Recall prompts retrieve rules and conditions without adding a new representation.", "sourceId": SOURCE_ID},
        "items": items,
    }


def write_yaml(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8")


def verify_source(profiles: dict[str, dict[str, Any]]) -> None:
    manifest = json.loads((SOURCE_DIR / "manifest.json").read_text(encoding="utf-8"))
    chunks = json.loads((SOURCE_DIR / "chunks.json").read_text(encoding="utf-8"))
    assert manifest["sha256"] == SOURCE_SHA
    assert manifest["extractor"] == "pypdf-v1" and manifest["extractionStatus"] == "completed"
    assert manifest["chunkCount"] == 5112 and len(chunks) == 5112
    by_id = {chunk["id"]: chunk for chunk in chunks}
    for topic in profiles.values():
        for ordinal in topic["chunks"]:
            chunk_id = f"{SOURCE_ID}:chunk-{ordinal}"
            assert chunk_id in by_id and by_id[chunk_id]["text"].strip(), chunk_id


def item_records(assessment: dict[str, Any]) -> list[tuple[str, str, str]]:
    records = []
    for section in assessment.get("lesson", {}).get("sections", []):
        check = section.get("check")
        if check:
            records.append((check["id"], check["type"], check["prompt"]))
    for section in assessment.get("glossary", {}).get("sections", []):
        for entry in section.get("entries", []):
            for drill in entry.get("drills", []):
                records.append((drill["id"], drill["type"], drill["prompt"]))
    for example in assessment.get("workedExamples", []):
        for step in example.get("steps", []):
            records.append((step["id"], step["type"], step["prompt"]))
    for item in assessment.get("items", []):
        records.append((item["id"], item["type"], item["prompt"]))
    return records


def write_contracts(profiles: dict[str, dict[str, Any]], assessments: dict[str, list[dict[str, Any]]]) -> None:
    curriculum = {
        "schemaVersion": 1, "id": "chemistry-bonding-learning-s2c", "categoryId": "chemistry", "sourceIds": [SOURCE_ID],
        "sourceReview": {"sha256": SOURCE_SHA, "extractor": "pypdf-v1", "status": "completed", "chunkCount": 5112, "licenseReview": "draft", "warning": "Inspect extracted equations and diagrams against source pages before approval."},
        "topics": [],
    }
    prereqs = {
        "chem-lewis-symbols": [], "chem-ions": ["chem-lewis-symbols"], "chem-ionic-bonds": ["chem-ions"],
        "chem-covalent-bonds": ["chem-lewis-symbols"],
        "chem-ionic-covalent-distinction": ["chem-ionic-bonds", "chem-covalent-bonds"],
        "chem-compound-nomenclature": ["chem-ions", "chem-ionic-covalent-distinction"],
        "chem-covalent-molecules": ["chem-covalent-bonds"],
        "chem-lewis-dot-structures": ["chem-covalent-molecules"],
        "chem-molecular-charges": ["chem-lewis-dot-structures"],
        "chem-polar-bonds-molecules": ["chem-molecular-shapes"],
        "chemistry-bonding-compounds-review": ["chem-compound-nomenclature", "chem-polar-bonds-molecules"],
        "chem-molecular-structure-review": ["chem-molecular-charges", "chem-molecular-shapes", "chem-polar-bonds-molecules"],
    }
    for topic_id, topic in profiles.items():
        ids = [assessment["id"] for assessment in assessments[topic_id]]
        curriculum["topics"].append({"topicId": topic_id, "prerequisiteIds": prereqs[topic_id], "objectiveIds": [topic["objective"]], "requiredSequence": ids})
        chunk_ids = [f"{SOURCE_ID}:chunk-{ordinal}" for ordinal in topic["chunks"]]
        packet_id = f"packet-{topic_id}-learning-v1"
        packet = {"schemaVersion": 1, "id": packet_id, "sourceId": SOURCE_ID, "categoryId": "chemistry", "topicId": topic_id, "objectiveIds": [topic["objective"]], "chunkIds": chunk_ids, "reviewState": "approved", "constraints": ["Original learner wording only", "Review source diagrams and equations before approval"]}
        (REFERENCE / "packets" / f"{packet_id}.json").write_text(json.dumps(packet, indent=2), encoding="utf-8")
        release = {"schemaVersion": 1, "id": f"{topic_id}-learning-release", "categoryId": "chemistry", "topicId": topic_id, "packetId": packet_id, "activities": []}
        blueprints = {"schemaVersion": 1, "id": f"{topic_id}-learning-blueprints", "packetId": packet_id, "records": []}
        for assessment in assessments[topic_id]:
            activity = assessment["navigation"]["activityType"]
            release["activities"].append({"assessmentId": assessment["id"], "activityType": activity, "publicationStatus": "published"})
            content_manifest = {"schemaVersion": 1, "assessmentId": assessment["id"], "categoryId": "chemistry", "topicId": topic_id, "packetId": packet_id, "objectiveIds": [topic["objective"]], "sourceId": SOURCE_ID, "sourceChunkIds": chunk_ids, "reviewState": "approved"}
            (REFERENCE / "content-manifests" / f"{assessment['id']}.json").write_text(json.dumps(content_manifest, indent=2), encoding="utf-8")
            for item_id, item_type, prompt in item_records(assessment):
                blueprints["records"].append({
                    "id": f"bp-{assessment['id']}-{item_id}", "assessmentId": assessment["id"], "questionId": item_id,
                    "objectiveId": topic["objective"], "sourceChunkIds": chunk_ids, "reviewState": "approved",
                    "questionType": item_type, "givens": prompt, "unknown": "The requested chemistry classification, count, representation, or explanation.",
                    "representation": "electron, particle, formula, or evidence representation as stated in the prompt",
                    "governingPrinciple": topic["principles"][0]["content"],
                    "methodSteps": ["Identify the representation and known quantities", "Apply electron, charge, or particle accounting", "Verify the conclusion against an independent condition"],
                    "likelyMisconception": topic["signal"], "answerVerificationMethod": "Independent electron, charge, formula, or particle-model check",
                    "variationAxes": {"scenario": item_id, "representation": item_type, "unknown": prompt[:80]},
                    "reasoningSignature": f"{topic_id}-{assessment['id']}-{item_id}",
                })
        write_yaml(REFERENCE / "assessment-release-manifests" / f"{topic_id}-learning-s2c.yaml", release)
        write_yaml(REFERENCE / "question-blueprints" / f"{topic_id}-learning-s2c.yaml", blueprints)
    write_yaml(REFERENCE / "curriculum-manifests" / "chemistry-bonding-learning-s2c.yaml", curriculum)


SVG_STYLE = """<style>.t{font:700 20px Arial;fill:#172554}.h{font:700 15px Arial;fill:#172554}.b{font:13px Arial;fill:#334155}.card{fill:#f8fafc;stroke:#2563eb;stroke-width:2}.atom{fill:#dbeafe;stroke:#1d4ed8;stroke-width:2}.e{fill:#dc2626}.arrow{stroke:#0f766e;stroke-width:3;marker-end:url(#a)}</style>"""


def write_visuals(profiles: dict[str, dict[str, Any]]) -> None:
    media = ROOT / "frontend" / "public" / "media" / "chemistry"
    media.mkdir(parents=True, exist_ok=True)
    cards = {
        "chem-lewis-symbols": ("Lewis symbol workflow", ["group position", "count valence dots", "place singles first", "verify ion charge"]),
        "chem-ions": ("Ion formation map", ["count protons/electrons", "determine sign", "check noble-gas count", "conserve charge"]),
        "chem-ionic-bonds": ("Ionic lattice reasoning", ["form ions", "balance ratio", "assemble lattice", "predict properties"]),
        "chem-covalent-bonds": ("Shared-pair model", ["count electrons", "place shared pairs", "assign lone pairs", "verify bond order"]),
        "chem-ionic-covalent-distinction": ("Classification by evidence", ["inspect composition", "identify particles", "use properties", "handle exceptions"]),
    }
    for topic_id, topic in profiles.items():
        title, labels = cards[topic_id]
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="260" viewBox="0 0 960 260"><title>{title}</title><desc>Four-stage chemistry reasoning diagram for {topic["title"]}.</desc>{SVG_STYLE}<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#0f766e"/></marker></defs><text x="30" y="34" class="t">{title}</text>']
        for i, label in enumerate(labels):
            x = 25 + i * 235
            parts.append(f'<rect x="{x}" y="70" width="190" height="120" rx="14" class="card"/><circle cx="{x+32}" cy="105" r="18" class="atom"/><text x="{x+26}" y="111" class="h">{i+1}</text><text x="{x+20}" y="150" class="h">{label}</text>')
            if i < 3:
                parts.append(f'<line x1="{x+195}" y1="130" x2="{x+225}" y2="130" class="arrow"/>')
        parts.append('<text x="30" y="232" class="b">Keep electron accounting, particle identity, and observable evidence as separate verification layers.</text></svg>')
        (ROOT / "frontend" / "public" / topic["visual"].lstrip("/")).write_text("".join(parts), encoding="utf-8")


def main() -> None:
    verify_source(FOUNDATIONS)
    generated: dict[str, list[dict[str, Any]]] = {}
    for topic_id, topic in FOUNDATIONS.items():
        bundle = [concept_assessment(topic_id, topic), glossary_assessment(topic_id, topic), worked_assessment(topic_id, topic), recall_assessment(topic_id, topic)]
        generated[topic_id] = bundle
        for assessment in bundle:
            write_yaml(ASSESSMENTS / f"{assessment['id']}.yaml", assessment)
    write_contracts(FOUNDATIONS, generated)
    write_visuals(FOUNDATIONS)
    print(f"Generated {sum(len(v) for v in generated.values())} foundational learning assessments.")


if __name__ == "__main__":
    main()
