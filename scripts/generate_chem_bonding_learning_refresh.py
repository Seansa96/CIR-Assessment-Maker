"""Refresh the five partially authored Chemistry bonding learning bundles."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from generate_chem_bonding_learning import (
    ASSESSMENTS, DEFINITIONS, FOUNDATIONS, REFERENCE, ROOT, SOURCE_ID,
    concept_assessment, glossary_assessment, principle, recall_assessment,
    verify_source, worked_assessment, write_contracts, write_yaml,
)


DEFINITIONS.update({
    "chemical nomenclature": "A rule system for assigning names to substances and translating names into formulas.",
    "binary compound": "A compound whose formula contains two different elements.",
    "fixed-charge metal": "A metal whose common ion has one predictable charge in the naming context.",
    "variable-charge metal": "A metal that can form more than one cation and therefore requires a charge designation in its name.",
    "Roman numeral": "The parenthetical numeral in an ionic name that states a variable-charge metal ion's charge.",
    "monatomic anion": "A one-atom negative ion named with an ide ending.",
    "oxyanion": "A polyatomic anion containing oxygen and another element.",
    "molecular prefix": "A prefix such as di, tri, or tetra that states the number of atoms in a molecular formula.",
    "subscript": "A formula number that states how many atoms or polyatomic-ion units are present.",
    "charge balance": "The equality of total positive and negative charge in a neutral ionic formula.",
    "retained name": "A conventional substance name, such as water or ammonia, used alongside systematic nomenclature.",
    "parentheses in formulas": "Grouping marks used when more than one copy of a polyatomic ion is required.",
    "orbital overlap": "The interpenetration of atomic-orbital regions that concentrates bonding electron density between nuclei.",
    "sigma bond": "A bond with electron density concentrated along the internuclear axis.",
    "pi bond": "A bond with electron density in regions on opposite sides of the internuclear axis.",
    "restricted rotation": "Resistance to rotation caused by the need to disrupt pi overlap in a multiple bond.",
    "bond enthalpy": "The enthalpy required to break one mole of a specified gas-phase bond.",
    "potential-energy curve": "A graph of interaction energy versus internuclear separation whose minimum identifies equilibrium bond length.",
    "formal charge": "The bookkeeping charge obtained by assigning each atom all nonbonding electrons and half the bonding electrons.",
    "formal-charge sum": "The requirement that all atomic formal charges add to the species' net charge.",
    "dominant contributor": "A Lewis contributor favored by small formal charges, appropriate charge placement, and complete shells when possible.",
    "resonance contributor": "One of two or more valid Lewis structures with the same atom arrangement but different electron placement.",
    "resonance hybrid": "The actual delocalized structure represented collectively by its resonance contributors.",
    "delocalization": "Distribution of bonding or charge over more than one localized atom pair or position.",
    "fractional bond order": "An average bond order produced when equivalent bonds are represented across resonance contributors.",
    "equivalent bond": "A bond experimentally indistinguishable from another because of symmetry or delocalization.",
    "Lewis structure": "An electron-bookkeeping drawing showing bonds, lone pairs, and sometimes formal charges.",
    "skeletal arrangement": "The atom connectivity selected before distributing remaining valence electrons.",
    "central atom": "The atom connected to multiple surrounding atoms in a Lewis or geometry analysis.",
    "terminal atom": "An atom attached to only one other atom in the selected skeletal arrangement.",
    "multiple bond": "A double or triple bond created by sharing more than one electron pair.",
    "incomplete octet": "A valid electron-deficient arrangement with fewer than eight electrons around an atom such as boron.",
    "odd-electron species": "A molecule or ion with an odd total number of valence electrons.",
    "expanded valence shell": "A Lewis description with more than eight electrons around a period-three-or-lower central atom.",
    "electron-count check": "Verification that every valence electron supplied by the formula and charge appears exactly once.",
    "bond dipole": "A vector pointing toward the more electronegative end of a polar bond.",
    "partial charge": "A nonintegral charge label indicating unequal sharing rather than complete electron transfer.",
    "molecular dipole": "The vector sum of all bond dipoles and relevant lone-pair contributions in a molecule.",
    "molecular polarity": "A nonzero separation of charge across an entire molecule.",
    "dipole cancellation": "A zero vector sum produced by equal bond dipoles arranged symmetrically.",
    "symmetry": "A spatial relationship that can make equal bond-dipole vectors cancel.",
    "dipole moment": "A quantitative measure of charge separation with both magnitude and direction.",
    "local polarity": "Unequal electron sharing in a particular bond or local structural region.",
    "polar covalent bond": "A covalent bond in which unequal sharing creates partial positive and partial negative ends.",
    "nonpolar covalent bond": "A covalent bond with equal or nearly equal sharing and no meaningful bond dipole.",
    "molecular geometry": "The three-dimensional arrangement of bonded atom positions around a selected center.",
    "vector sum": "The magnitude and direction obtained by adding all component vectors with their spatial orientations.",
})


def p(identifier: str, title: str, content: str, correct: str, wrong: str) -> dict[str, str]:
    return principle(identifier, title, content, correct, wrong, "The conclusion follows from counting element symbols rather than applying the required electron, charge, or vector check.")


REFRESH: dict[str, dict[str, Any]] = {
    "chem-compound-nomenclature": {
        "title": "Chemical Nomenclature and Formula Writing", "signal": "chemistry-bonding-nomenclature-path-error",
        "chunks": ["0242", "0243", "0244", "0246", "0250", "0251", "0252", "0255"], "objective": "chem-bond-nomenclature",
        "visual": "/media/chemistry/bonding-nomenclature-workflow.svg",
        "principles": [
            p("ionic-vs-covalent", "Choose the naming path", "Classify the particle type before naming. Ionic names identify ions and charges; molecular names use atom-count prefixes.", "FeCl3 follows the variable-charge ionic path.", "FeCl3 uses molecular prefixes because its formula has four atoms."),
            p("type-i-ionic", "Name fixed-charge ionic compounds", "Name the cation unchanged, then change a monatomic anion ending to ide. A fixed-charge metal does not receive a Roman numeral.", "K2S is potassium sulfide.", "K2S is dipotassium monosulfide."),
            p("type-ii-ionic", "Determine variable metal charge", "Use anion charge and formula subscripts to infer the metal charge, then write that charge as a Roman numeral.", "Fe2O3 is iron(III) oxide.", "Fe2O3 is iron(II) oxide because the iron subscript is two."),
            p("polyatomic-formulas", "Preserve polyatomic ions", "Recognize a polyatomic ion as one unit. Use parentheses only when more than one copy is required.", "Calcium nitrate is Ca(NO3)2.", "Calcium nitrate is CaNO32 because parentheses never matter."),
            p("molecular-naming", "Use molecular prefixes", "For two nonmetals, prefixes state atom counts; omit mono on the first element and give the second element an ide ending.", "N2O5 is dinitrogen pentoxide.", "N2O5 is nitrogen(V) oxide."),
            p("special-names", "Recognize retained names", "A small set of conventional names remains standard. Treat these as vocabulary while keeping systematic rules available for unfamiliar compounds.", "NH3 is commonly called ammonia.", "Every molecular compound has a retained name that replaces systematic naming."),
        ],
        "terms": ["chemical nomenclature", "binary compound", "fixed-charge metal", "variable-charge metal", "Roman numeral", "monatomic anion", "polyatomic ion", "oxyanion", "molecular prefix", "subscript", "charge balance", "formula unit", "parentheses in formulas", "retained name", "ionic compound", "molecular compound"],
        "examples": [
            ("Name fixed- and variable-charge salts", "Name CaCl2 and FeCl3 using the correct ionic path.", ["Classify both formulas as ionic because each begins with a metal.", "Calcium has a fixed 2+ charge, so CaCl2 is calcium chloride.", "Three Cl- require Fe3+, so FeCl3 is iron(III) chloride.", "Verify that each name communicates the ion ratio without molecular prefixes."]),
            ("Write formulas from ionic names", "Write aluminum oxide, copper(II) nitrate, and ammonium sulfate.", ["Balance Al3+ with O2- to obtain Al2O3.", "Balance Cu2+ with two nitrate ions to obtain Cu(NO3)2.", "Balance two NH4+ ions with SO4 2- to obtain (NH4)2SO4."]),
            ("Select and apply the molecular path", "Name N2O4 and write the formula for phosphorus pentachloride.", ["Two nonmetals select the molecular-prefix system.", "N2O4 becomes dinitrogen tetroxide after applying the vowel contraction.", "Phosphorus pentachloride becomes PCl5; the omitted mono prefix implies one phosphorus."]),
        ],
    },
    "chem-covalent-molecules": {
        "title": "Covalent Molecules and Bonding", "signal": "chemistry-bonding-covalent-pair-error",
        "chunks": ["0946", "0947", "0949", "1016", "1017", "1029", "1030", "1033"], "objective": "chem-bond-covalent-molecules",
        "visual": "/media/chemistry/bonding-sigma-pi-map.svg",
        "principles": [
            p("sec-what-is-covalent", "Connect overlap to a bond", "Covalent bonding lowers energy when attractive electron-nucleus interactions outweigh repulsions at an equilibrium separation.", "The bond-length minimum marks a stable separation.", "The nuclei collapse together because attraction has no repulsive limit."),
            p("sec-bond-order", "Relate order, length, and strength", "For the same atom pair, higher bond order generally means shorter, stronger bonding.", "A carbon triple bond is shorter than a carbon single bond.", "A carbon triple bond is longer because it contains more electrons."),
            p("sec-sigma-pi", "Count sigma and pi bonds", "Every localized single bond is sigma; a double bond adds one pi and a triple bond adds two pi bonds.", "A C triple C bond contains one sigma and two pi bonds.", "A C triple C bond contains three sigma bonds."),
            p("sec-rotation", "Explain restricted rotation", "Rotating a double bond would disrupt side-by-side pi overlap, so rotation is restricted unless the pi interaction is broken.", "A carbon-carbon double bond resists free rotation.", "A sigma bond prevents all rotation because its density is cylindrical."),
            p("sec-bond-energy-enthalpy", "Estimate reaction enthalpy", "An average-bond-enthalpy estimate subtracts energy released by formed bonds from energy required for broken bonds.", "Delta H is approximately bonds broken minus bonds formed.", "Delta H is bonds formed minus bonds broken regardless of sign convention."),
            p("sec-model-limits", "Use average data cautiously", "Average bond enthalpies depend on molecular environment, so they estimate rather than exactly reproduce a reaction enthalpy.", "A bond-enthalpy result should be labeled an estimate.", "One tabulated C-H value is exact in every molecule."),
        ],
        "terms": ["orbital overlap", "sigma bond", "pi bond", "restricted rotation", "bond order", "bond length", "bond energy", "bond enthalpy", "potential-energy curve", "single bond", "double bond", "triple bond", "shared pair", "localized bond", "molecule", "covalent bond"],
        "examples": [
            ("Count sigma and pi bonds", "Analyze HCN, ethene, and ethyne.", ["HCN has two sigma bonds and two pi bonds.", "Ethene has five sigma bonds and one pi bond.", "Ethyne has three sigma bonds and two pi bonds."]),
            ("Estimate hydrogenation enthalpy", "Use supplied average bond enthalpies for ethene plus hydrogen forming ethane.", ["Identify the net broken interactions as one C=C and one H-H.", "Identify the net formed interactions as one C-C and two C-H.", "Compute broken minus formed and retain the sign as the predicted heat direction."]),
            ("Connect a potential curve to bond properties", "Interpret two bond-energy curves with different minima.", ["The horizontal coordinate of each minimum gives its equilibrium bond length.", "The deeper minimum identifies the larger dissociation energy.", "Use both axes to conclude which bond is shorter and stronger without confusing depth with position."]),
        ],
    },
    "chem-molecular-charges": {
        "title": "Formal Charges and Resonance", "signal": "chemistry-bonding-formal-charge-error",
        "chunks": ["0926", "0928", "0931", "0932", "0933", "0936", "0939"], "objective": "chem-bond-formal-resonance",
        "visual": "/media/chemistry/bonding-formal-resonance-map.svg",
        "principles": [
            p("sec-formal-charge", "Calculate formal charge", "Formal charge equals valence electrons minus nonbonding electrons minus one-half of bonding electrons.", "Oxygen with one bond and three lone pairs has formal charge 1-.", "Oxygen with one bond and three lone pairs has formal charge 1+."),
            p("sec-charge-sum", "Verify the charge sum", "Atomic formal charges must add to the molecule or ion's stated net charge.", "Formal charges in nitrate must sum to 1-.", "Every atom in a polyatomic ion must carry the full ion charge."),
            p("sec-best-lewis", "Compare candidate contributors", "Prefer complete shells, small formal-charge magnitudes, and negative charge on more electronegative atoms when other constraints are comparable.", "A structure with minimized charge separation is usually favored.", "The contributor with the greatest number of formal charges is always dominant."),
            p("sec-resonance-structures", "Generate resonance contributors", "Resonance contributors keep atom positions fixed and move only electrons, bonds, or lone pairs.", "Equivalent nitrate contributors differ in which oxygen has the double bond.", "Resonance moves an oxygen atom to a new attachment point."),
            p("sec-resonance-hybrid", "Interpret the hybrid", "The real electron distribution is delocalized; a molecule does not alternate back and forth among contributor drawings.", "Equivalent nitrate N-O bonds have equal intermediate character.", "A nitrate ion contains one permanently short and two permanently long N-O bonds."),
            p("sec-fractional-order", "Determine fractional bond order", "For equivalent bonds, average the localized bond orders represented across equivalent contributors.", "Three equivalent nitrate N-O bonds have average order 4/3.", "Every resonance bond must have integer bond order in the actual ion."),
        ],
        "terms": ["formal charge", "formal-charge sum", "dominant contributor", "resonance contributor", "resonance hybrid", "delocalization", "fractional bond order", "equivalent bond", "Lewis structure", "lone pair", "bonding pair", "valence electron", "electronegativity", "charge conservation", "multiple bond", "particle model"],
        "examples": [
            ("Compare sulfur trioxide contributors", "Calculate formal charges for candidate SO3 Lewis structures.", ["Count sulfur and oxygen valence electrons and confirm the full electron inventory.", "Apply the formal-charge formula atom by atom in the all-single-bond contributor.", "Compare a contributor with S=O bonding and select the lower-charge description subject to the allowed valence model.", "Verify that every contributor's charges sum to zero."]),
            ("Describe nitrate resonance", "Construct and interpret the resonance contributors of NO3-.", ["Count 24 valence electrons and keep the N-O atom skeleton fixed.", "Draw three equivalent contributors by moving the N=O bond and associated lone pair.", "Verify a 1- charge sum and conclude that the three actual N-O bonds are equivalent."]),
            ("Calculate carbonate bond order", "Use three carbonate contributors to infer C-O bond order.", ["Each contributor contains one C=O and two C-O bonds.", "Across three equivalent positions the total localized order is four.", "Divide four by three bonds to obtain an average C-O bond order of 4/3 and connect it to equal bond lengths."]),
        ],
    },
    "chem-lewis-dot-structures": {
        "title": "Lewis Dot Structures in Depth", "signal": "chemistry-bonding-covalent-pair-error",
        "chunks": ["0920", "0923", "0924", "0926", "0941", "0943", "0946"], "objective": "chem-bond-lewis-structures",
        "visual": "/media/chemistry/bonding-lewis-structure-algorithm.svg",
        "principles": [
            p("sec-procedure", "Follow the electron-accounting algorithm", "Count valence electrons, choose connectivity, place single bonds, complete terminal shells, place leftovers centrally, and form multiple bonds if needed.", "A valid procedure ends with an electron-total and charge check.", "Start by guessing double bonds before counting electrons."),
            p("sec-polyatomic", "Adjust for ion charge", "Add one electron per negative charge and subtract one per positive charge, then bracket the completed ion.", "SO4 2- includes two electrons beyond the neutral-atom total.", "SO4 2- contains two fewer electrons because its charge is negative."),
            p("sec-multiple-bonds", "Form multiple bonds when needed", "Convert a neighboring lone pair into an additional shared pair when the central atom lacks an octet and the electron total is already exhausted.", "HCN requires a C triple N bond in its standard structure.", "Add new electrons from outside the counted total to make a multiple bond."),
            p("sec-incomplete-octets", "Recognize incomplete octets", "Hydrogen needs two electrons, while compounds such as BF3 can leave boron with six without inventing extra electrons.", "BF3 can be represented with six electrons around boron.", "Every BF3 drawing must add a nonexistent lone pair to boron."),
            p("sec-expanded-octets", "Recognize expanded valence shells", "Period-three and heavier centers can be represented with more than eight electrons in common Lewis structures; second-period centers cannot.", "SF6 is commonly drawn with twelve electrons around sulfur.", "Carbon routinely expands to twelve electrons in CO2."),
            p("sec-radicals", "Handle odd-electron species", "An odd valence-electron total guarantees at least one unpaired electron; do not force an octet by creating or deleting an electron.", "NO has an odd-electron Lewis description.", "Every molecule must have an even electron count."),
        ],
        "terms": ["Lewis structure", "valence electron", "skeletal arrangement", "central atom", "terminal atom", "bonding pair", "lone pair", "single bond", "multiple bond", "formal charge", "electron-count check", "incomplete octet", "odd-electron species", "expanded valence shell", "polyatomic ion", "octet rule"],
        "examples": [
            ("Draw standard molecular structures", "Construct H2O, NH3, and HCN with independent checks.", ["H2O uses two O-H bonds and two oxygen lone pairs.", "NH3 uses three N-H bonds and one nitrogen lone pair.", "HCN uses H-C and a C triple N bond with one nitrogen lone pair."]),
            ("Handle expanded centers", "Construct PCl5 and SF4.", ["PCl5 uses five P-Cl bonds and no central lone pair.", "SF4 uses four S-F bonds and one central lone pair.", "Verify that both totals use only the supplied valence electrons and allow an expanded sulfur or phosphorus shell."]),
            ("Handle polyatomic ions", "Construct sulfate and ammonium structures.", ["Include charge electrons before drawing either ion.", "Bracket each completed structure and show its net charge.", "Verify electron totals, formal-charge sums, and atom connectivity independently."]),
        ],
    },
    "chem-polar-bonds-molecules": {
        "title": "Polar Bonds and Molecular Polarity", "signal": "chemistry-bonding-polarity-vector-error",
        "chunks": ["0904", "0906", "0908", "0910", "0913", "1012", "1014", "1015"], "objective": "chem-bond-polarity",
        "visual": "/media/chemistry/bonding-polarity-vectors.svg",
        "principles": [
            p("sec-electronegativity", "Use electronegativity direction", "A bond dipole points toward the more electronegative atom, which carries partial negative character.", "An H-F bond dipole points toward fluorine.", "An H-F bond dipole points toward hydrogen because hydrogen is positive."),
            p("sec-bond-polarity", "Separate partial from full charge", "Polar covalent sharing produces partial charges; it does not automatically create free ions.", "HF has unequal sharing without being an isolated H+ and F- pair.", "Every polar bond is fully ionic."),
            p("sec-molecular-polarity", "Add dipoles as vectors", "Molecular polarity depends on vector sum, not the mere presence of polar bonds.", "Linear CO2 has cancelling C-O dipoles.", "CO2 is polar because it contains two polar bonds."),
            p("sec-symmetry", "Use symmetry with geometry", "Equal dipoles cancel only when the three-dimensional arrangement makes their vectors balance.", "Tetrahedral CCl4 is nonpolar because four equal vectors cancel.", "Any molecule with four bonds is automatically nonpolar."),
            p("sec-polarity-applications", "Recognize asymmetric substitution", "Replacing one member of a symmetric set can prevent complete cancellation even when the central geometry remains similar.", "CHCl3 is polar while CCl4 is nonpolar.", "CHCl3 is nonpolar because both formulas contain carbon and chlorine."),
            p("sec-multicenter", "Analyze local and net polarity", "For a multicenter molecule, identify local bond dipoles and geometry, then add their contributions over the whole structure.", "Local polar bonds can produce either a zero or nonzero molecular dipole.", "One polar bond guarantees the entire molecule is polar."),
        ],
        "terms": ["electronegativity", "bond dipole", "partial charge", "dipole moment", "molecular dipole", "molecular polarity", "dipole cancellation", "symmetry", "local polarity", "bonding continuum", "polar covalent bond", "nonpolar covalent bond", "molecular geometry", "particle model", "covalent bond", "vector sum"],
        "examples": [
            ("Compare carbon dioxide and water", "Use geometry to compare two molecules with polar bonds.", ["Assign each bond dipole toward oxygen.", "Add the opposite collinear CO2 vectors to obtain zero.", "Add the angled H2O vectors to obtain a nonzero resultant toward oxygen.", "State that bond polarity alone did not determine the molecular result."]),
            ("Compare CCl4 and CHCl3", "Determine how substitution changes a tetrahedral vector sum.", ["Four equal C-Cl vectors in tetrahedral CCl4 cancel by symmetry.", "Replacing one chlorine with hydrogen makes the bond-vector set unequal.", "The remaining vectors in CHCl3 do not cancel, so the molecule is polar."]),
            ("Analyze a multicenter molecule", "Predict polarity for acetic acid from local structures.", ["Identify polar C=O and O-H regions and their dipole directions.", "Use local geometries to orient rather than merely count those vectors.", "Conclude that the asymmetric vector set has a nonzero molecular dipole."]),
        ],
    },
}


IDS = {
    "chem-compound-nomenclature": ("chemistry-compounds-concept-lesson", "chem-compound-nomenclature-glossary", "chemistry-compounds-worked-example", "chemistry-compounds-recall"),
    "chem-covalent-molecules": ("chem-covalent-molecules-concept-lesson", "chem-covalent-molecules-glossary", "chem-covalent-molecules-worked-example", "chem-covalent-molecules-recall-drill"),
    "chem-molecular-charges": ("chem-molecular-charges-concept-lesson", "chem-molecular-charges-glossary", "chem-molecular-charges-worked-example", "chem-molecular-charges-recall-drill"),
    "chem-lewis-dot-structures": ("chem-lewis-dot-structures-concept-lesson", "chem-lewis-dot-structures-glossary", "chem-lewis-dot-structures-worked-example", "chem-lewis-dot-structures-recall-drill"),
    "chem-polar-bonds-molecules": ("chem-polar-bonds-molecules-concept-lesson", "chem-polar-bonds-molecules-glossary", "chem-polar-bonds-molecules-worked-example", "chem-polar-bonds-molecules-recall-drill"),
}

STEP_IDS = {
    "chem-compound-nomenclature": ["step-naming-type-i-ii-1", "step-naming-type-i-ii-2", "step-naming-type-i-ii-3", "step-naming-type-i-ii-4", "step-formula-from-name-1", "step-formula-from-name-2", "step-formula-from-name-3", "step-identify-compound-type-1", "step-identify-compound-type-2", "step-identify-compound-type-3"],
    "chem-covalent-molecules": ["s1-hcn", "s2-c2h4", "s3-c2h2", "s4-identify-bonds-broken", "s5-identify-bonds-formed", "s6-calculate-delta-h"],
    "chem-molecular-charges": ["s1-count-ve-so3", "s2-fc-structure-a", "s3-fc-structure-b", "s4-so3-conclusion", "s5-no3-count", "s6-no3-resonance-structures", "s7-no3-bond-order"],
    "chem-lewis-dot-structures": ["s1-h2o", "s2-nh3", "s3-hcn", "s4-pcl5", "s5-sf4", "s5-expanded-check", "s6-sulfate", "s7-ammonium", "s7-ion-check"],
    "chem-polar-bonds-molecules": ["s1-co2-geometry", "s2-co2-polarity", "s3-h2o-geometry", "s4-h2o-polarity", "s5-ccl4", "s6-chcl3", "s7-polarity-rule"],
}


def make_bundle(topic_id: str, profile: dict[str, Any]) -> list[dict[str, Any]]:
    bundle = [concept_assessment(topic_id, profile), glossary_assessment(topic_id, profile), worked_assessment(topic_id, profile), recall_assessment(topic_id, profile)]
    for assessment, stable_id in zip(bundle, IDS[topic_id]):
        assessment["id"] = stable_id
    stable_steps = STEP_IDS[topic_id]
    steps = [step for example in bundle[2]["workedExamples"] for step in example["steps"]]
    for step, stable_id in zip(steps, stable_steps):
        step["id"] = stable_id
    if topic_id == "chem-compound-nomenclature":
        # Preserve all sixteen published recall IDs.
        for i, term in enumerate(profile["terms"][12:], 13):
            definition = DEFINITIONS[term]
            bundle[3]["items"].append({"id": f"r{i:03d}", "type": "typed", "prompt": f"State the role of {term} in a naming or formula decision.", "answer": {"expected": definition, "aliases": [term]}, "explanation": f"Solution: {definition} Why it works: The definition identifies the exact decision controlled by the term."})
    return bundle


def repair_supplements() -> None:
    # Preserve the covalent-naming learner IDs while placing the activity with nomenclature.
    path = ASSESSMENTS / "chemistry-covalent-naming-worked-example.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data["topicId"] = "chem-compound-nomenclature"
    data["navigation"]["activityType"] = "guidedWorkedExample"
    for example in data.get("workedExamples", []):
        for step in example.get("steps", []):
            instruction = step.get("instruction") or step.get("prompt") or "Apply the molecular-prefix rule."
            step["explanation"] = f"Solution: {instruction} Why it works: A two-nonmetal formula uses prefixes to preserve the stated atom counts."
    write_yaml(path, data)

    # Keep special names and drawing practice supplemental, but make their feedback compliant.
    for name in ["chemistry-special-names-recall.yaml", "chem-lewis-dot-structures-drawing-practice.yaml"]:
        path = ASSESSMENTS / name
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        for item in data.get("items", []):
            expected = item.get("answer", {}).get("expected", "the stated retained name")
            item["explanation"] = f"Solution: {expected}. Why it works: This retained name is conventional chemistry vocabulary."
        for example in data.get("workedExamples", []):
            for step in example.get("steps", []):
                instruction = step.get("instruction") or "Complete the electron-count and structure check."
                step["explanation"] = f"Solution: {instruction} Why it works: The structure must use the supplied valence electrons and satisfy the stated shell and charge checks."
        write_yaml(path, data)


def write_visuals() -> None:
    specs = {
        "bonding-nomenclature-workflow.svg": ("Nomenclature decision workflow", ["classify particles", "identify charge rule", "apply name or formula rule", "verify atom and charge counts"]),
        "bonding-sigma-pi-map.svg": ("Sigma and pi bond map", ["single: one sigma", "double: sigma plus pi", "triple: sigma plus two pi", "connect order to properties"]),
        "bonding-formal-resonance-map.svg": ("Formal charge and resonance", ["count electrons", "calculate each charge", "compare contributors", "interpret the hybrid"]),
        "bonding-lewis-structure-algorithm.svg": ("Lewis structure algorithm", ["count", "connect", "complete shells", "verify charge"]),
        "bonding-polarity-vectors.svg": ("Bond dipole vector addition", ["assign directions", "use geometry", "add vectors", "state net polarity"]),
    }
    style = '<style>.t{font:700 20px Arial;fill:#172554}.h{font:700 14px Arial;fill:#172554}.b{font:13px Arial;fill:#334155}.c{fill:#f8fafc;stroke:#7c3aed;stroke-width:2}.a{stroke:#0f766e;stroke-width:3;marker-end:url(#m)}</style>'
    media = ROOT / "frontend" / "public" / "media" / "chemistry"
    for filename, (title, labels) in specs.items():
        body = [f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="260" viewBox="0 0 960 260"><title>{title}</title><desc>Four-stage visual reasoning aid for {title.lower()}.</desc>{style}<defs><marker id="m" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#0f766e"/></marker></defs><text x="28" y="34" class="t">{title}</text>']
        for i, label in enumerate(labels):
            x = 25 + 235 * i
            body.append(f'<rect x="{x}" y="76" width="190" height="110" rx="14" class="c"/><text x="{x+18}" y="126" class="h">{i+1}. {label}</text>')
            if i < 3: body.append(f'<line x1="{x+195}" y1="130" x2="{x+225}" y2="130" class="a"/>')
        body.append('<text x="28" y="228" class="b">Verify the representation with an independent electron, charge, geometry, or vector check.</text></svg>')
        (media / filename).write_text("".join(body), encoding="utf-8")


def load_foundations() -> dict[str, list[dict[str, Any]]]:
    result = {}
    for topic_id in FOUNDATIONS:
        result[topic_id] = [yaml.safe_load((ASSESSMENTS / f"{topic_id}-{suffix}.yaml").read_text(encoding="utf-8")) for suffix in ["concept-lesson", "glossary", "worked-examples", "recall-drill"]]
    return result


def main() -> None:
    combined = {**FOUNDATIONS, **REFRESH}
    verify_source(combined)
    generated = load_foundations()
    for topic_id, profile in REFRESH.items():
        bundle = make_bundle(topic_id, profile)
        generated[topic_id] = bundle
        for assessment in bundle:
            write_yaml(ASSESSMENTS / f"{assessment['id']}.yaml", assessment)
    repair_supplements()
    write_contracts(combined, generated)
    write_visuals()
    print("Refreshed five partial learning bundles and supplemental activities.")


if __name__ == "__main__":
    main()
