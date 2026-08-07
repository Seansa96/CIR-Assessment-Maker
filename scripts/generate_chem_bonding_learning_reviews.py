"""Generate the two cumulative Chemistry bonding review learning bundles."""

from __future__ import annotations

from typing import Any

import yaml

from generate_chem_bonding_learning import (
    ASSESSMENTS, FOUNDATIONS, REFERENCE, ROOT, SOURCE_ID,
    concept_assessment, glossary_assessment, principle, recall_assessment,
    verify_source, worked_assessment, write_contracts, write_yaml,
)
from generate_chem_bonding_learning_refresh import DEFINITIONS, IDS, REFRESH


def p(identifier: str, title: str, content: str, correct: str, wrong: str) -> dict[str, str]:
    return principle(identifier, title, content, correct, wrong, "The response uses a valid rule from a different stage of the analysis and therefore does not answer the stated question.")


REVIEWS: dict[str, dict[str, Any]] = {
    "chemistry-bonding-compounds-review": {
        "title": "Bonding, Molecular Geometry, and Compounds Review", "signal": "chemistry-bonding-review-method-error",
        "chunks": ["0233", "0238", "0242", "0250", "0883", "0885", "0900", "0904", "0920", "0928", "0989", "1012"],
        "objective": "chem-bond-integrated-review", "visual": "/media/chemistry/bonding-integrated-review-map.svg",
        "principles": [
            p("classify-first", "Classify before selecting a method", "Composition and particle evidence decide whether to use ion-charge, molecular-prefix, or network-covalent reasoning.", "Fe2O3 requires ionic charge analysis before naming.", "Fe2O3 should receive molecular prefixes because it has five atoms."),
            p("formula-name", "Connect charge balance to nomenclature", "For ionic substances, charge balance determines subscripts and a variable metal's Roman numeral; prefixes instead preserve molecular atom counts.", "Iron(III) oxide is consistent with Fe3+ and O2- in Fe2O3.", "The Roman numeral in iron(III) oxide reports three iron atoms."),
            p("lewis-account", "Build and verify Lewis structures", "Count valence electrons, establish connectivity, distribute pairs, and verify the electron total and formal-charge sum before using the drawing downstream.", "A Lewis structure check must agree with both electron total and species charge.", "A visually symmetric drawing is valid even if it uses the wrong electron total."),
            p("shape", "Convert a Lewis structure to local geometry", "Count bond directions and central lone pairs at the requested center, distinguish electron geometry from molecular geometry, and refine angles qualitatively.", "SO2 is locally bent at sulfur after counting three domains.", "SO2 is linear because its formula has three atoms."),
            p("polarity", "Add bond dipoles using geometry", "Assign local dipole directions and add them as vectors. Polar bonds can cancel in a symmetric geometry or reinforce in an asymmetric one.", "Bent SO2 has a nonzero molecular dipole.", "Every molecule with two identical terminal atoms is nonpolar."),
            p("properties", "Return to observable properties", "Use the particle model to explain melting, conductivity, brittleness, or molecular behavior without claiming that one observation uniquely proves a model.", "Molten ionic material conducts because ions become mobile.", "A high melting point by itself proves that a substance is ionic."),
        ],
        "terms": ["particle model", "ionic compound", "molecular compound", "network covalent solid", "formula unit", "chemical nomenclature", "charge balance", "Lewis structure", "formal charge", "resonance contributor", "molecular geometry", "bond dipole", "molecular polarity", "conductivity", "melting point", "empirical evidence"],
        "examples": [
            ("Analyze iron(III) oxide from formula to properties", "Use Fe2O3 to connect classification, charge, name, and particle behavior.", ["Classify Fe2O3 as ionic from its metal-nonmetal composition and ion model.", "Two Fe ions must supply 6+ against three O2-, so each iron is Fe3+ and the name is iron(III) oxide.", "Describe the solid as a lattice of ions rather than discrete Fe2O3 molecules.", "Predict no bulk ionic conduction in the solid but possible conduction when ions become mobile in a melt."]),
            ("Analyze ammonium nitrate across bond types", "Explain formula, naming, and bonding in NH4NO3.", ["Recognize NH4+ and NO3- as polyatomic ions even though every atom is a nonmetal.", "A 1:1 ion ratio balances charge, giving ammonium nitrate.", "Distinguish covalent bonds within each ion from ionic attraction between ions.", "Use the mixed particle model to reject a simple all-nonmetal molecular shortcut."]),
            ("Analyze sulfur dioxide from electrons to polarity", "Integrate Lewis structure, formal charge, geometry, and polarity for SO2.", ["Count 18 valence electrons and construct resonance-related Lewis contributors.", "Verify formal-charge sums of zero and recognize delocalized S-O bonding.", "Count two bond directions plus one sulfur lone pair to predict a bent local shape.", "Add the two S-O dipoles in the bent geometry to obtain a nonzero molecular dipole."]),
        ],
    },
    "chem-molecular-structure-review": {
        "title": "Lewis Structures, Molecular Shape, and Polarity Review", "signal": "chemistry-bonding-review-method-error",
        "chunks": ["0920", "0926", "0928", "0933", "0936", "0941", "0989", "0995", "1002", "1010", "1012", "1014"],
        "objective": "chem-bond-molecular-structure-review", "visual": "/media/chemistry/bonding-multicenter-review-map.svg",
        "principles": [
            p("electron-inventory", "Establish the complete electron inventory", "Count all valence electrons and adjust for charge before drawing any bonds or assigning geometry.", "Acetate has one extra electron because of its 1- charge.", "A negative ion has one fewer electron than its neutral atom total."),
            p("connectivity-charge", "Choose connectivity and check formal charge", "A chemically defensible skeleton and formal-charge accounting must precede geometry analysis; geometry cannot repair a wrong electron count.", "Formal charges must sum to the molecular or ionic charge.", "Choose the structure with the most formal charges to make charge visible."),
            p("resonance", "Separate resonance from isomerism", "Resonance changes electron placement while preserving atom connectivity. Equivalent contributors imply delocalized charge and equivalent bonds.", "Acetate resonance moves the C=O bond, not an oxygen atom.", "Resonance contributors are different compounds rapidly interconverting."),
            p("local-centers", "Analyze one local center at a time", "A multicenter molecule has separate electron-domain and molecular geometries at different atoms.", "Acetic acid contains tetrahedral and trigonal-planar carbon centers.", "Every atom in acetic acid shares one global VSEPR geometry."),
            p("vector-addition", "Build the molecular dipole", "Orient bond dipoles using each local geometry, then add them across the complete molecule.", "Asymmetric carbonyl and hydroxyl dipoles give acetic acid a nonzero net dipole.", "Counting polar bonds without their directions determines the dipole exactly."),
            p("structure-property", "Connect structure to behavior", "Use polarity and accessible interaction sites to support a property prediction while keeping intermolecular-force claims distinct from the intramolecular structure.", "A polar O-H region can support strong attraction to polar surroundings.", "An O-H bond means the oxygen and hydrogen are separate ions in the molecule."),
        ],
        "terms": ["valence electron", "Lewis structure", "formal charge", "formal-charge sum", "resonance contributor", "resonance hybrid", "delocalization", "central atom", "molecular geometry", "local polarity", "bond dipole", "vector sum", "molecular dipole", "molecular polarity", "symmetry", "particle model"],
        "examples": [
            ("Map the centers in acetic acid", "Analyze CH3COOH center by center.", ["Count the methyl carbon's four bonding domains and identify tetrahedral local geometry.", "Count the carbonyl carbon's three bonding directions and identify trigonal-planar local geometry.", "Treat the hydroxyl oxygen as a separate bent local center with two bonds and two lone pairs.", "Orient the C=O and O-H dipoles and conclude that the asymmetric molecule has a nonzero net dipole."]),
            ("Analyze urea as a delocalized multicenter molecule", "Connect Lewis contributors, local geometry, and polarity in CO(NH2)2.", ["Construct the carbonyl-centered skeleton and verify the complete valence-electron count.", "Use formal charge to compare contributors that delocalize each nitrogen lone pair toward the carbonyl center.", "Analyze carbonyl carbon and each nitrogen locally rather than assigning one global shape.", "Combine the strong C=O direction with the remaining bond vectors to predict a polar molecule."]),
            ("Analyze dimethyl ether", "Apply the local workflow to CH3OCH3.", ["Give each carbon four bonding domains and a tetrahedral local arrangement.", "Give oxygen two bonds and two lone pairs, producing a bent local molecular geometry.", "Orient both C-O bond dipoles toward oxygen.", "Add the angled vectors to obtain a nonzero molecular dipole despite two identical methyl groups."]),
        ],
    },
}


def load_existing() -> dict[str, list[dict[str, Any]]]:
    generated: dict[str, list[dict[str, Any]]] = {}
    for topic_id in FOUNDATIONS:
        generated[topic_id] = [yaml.safe_load((ASSESSMENTS / f"{topic_id}-{suffix}.yaml").read_text(encoding="utf-8")) for suffix in ["concept-lesson", "glossary", "worked-examples", "recall-drill"]]
    for topic_id, ids in IDS.items():
        generated[topic_id] = [yaml.safe_load((ASSESSMENTS / f"{assessment_id}.yaml").read_text(encoding="utf-8")) for assessment_id in ids]
    return generated


def write_visuals() -> None:
    specs = {
        "bonding-integrated-review-map.svg": ("Integrated bonding decision chain", ["classify particles", "name or write formula", "build structure and geometry", "predict polarity and properties"]),
        "bonding-multicenter-review-map.svg": ("Multicenter structure map", ["count total electrons", "check each local center", "orient local dipoles", "combine evidence"]),
    }
    media = ROOT / "frontend" / "public" / "media" / "chemistry"
    for filename, (title, labels) in specs.items():
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="280" viewBox="0 0 960 280"><title>{title}</title><desc>Four-stage transfer map for {title.lower()}.</desc><style>.t{{font:700 21px Arial;fill:#172554}}.h{{font:700 14px Arial;fill:#172554}}.c{{fill:#f0fdfa;stroke:#0f766e;stroke-width:2}}.a{{stroke:#7c3aed;stroke-width:3;marker-end:url(#m)}}</style><defs><marker id="m" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#7c3aed"/></marker></defs><text x="28" y="36" class="t">{title}</text>']
        for i, label in enumerate(labels):
            x = 25 + i * 235
            parts.append(f'<rect x="{x}" y="84" width="190" height="118" rx="14" class="c"/><text x="{x+18}" y="138" class="h">{i+1}. {label}</text>')
            if i < 3: parts.append(f'<line x1="{x+195}" y1="143" x2="{x+225}" y2="143" class="a"/>')
        parts.append('</svg>')
        (media / filename).write_text("".join(parts), encoding="utf-8")


def main() -> None:
    combined = {**FOUNDATIONS, **REFRESH, **REVIEWS}
    verify_source(combined)
    generated = load_existing()
    for topic_id, profile in REVIEWS.items():
        bundle = [concept_assessment(topic_id, profile), glossary_assessment(topic_id, profile), worked_assessment(topic_id, profile), recall_assessment(topic_id, profile)]
        generated[topic_id] = bundle
        for assessment in bundle:
            write_yaml(ASSESSMENTS / f"{assessment['id']}.yaml", assessment)
    water_path = ASSESSMENTS / "chemistry-water-molecule-concept-lesson.yaml"
    water = yaml.safe_load(water_path.read_text(encoding="utf-8"))
    water["navigation"]["activityType"] = "interactiveExploration"
    write_yaml(water_path, water)
    write_contracts(combined, generated)
    write_visuals()
    print("Generated two cumulative review learning bundles.")


if __name__ == "__main__":
    main()
