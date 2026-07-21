import yaml
from pathlib import Path

ROOT = Path("C:/Users/SeanS/Downloads/cir_app")
MANIFESTS = ROOT / "docs" / "assessment-reference" / "content-manifests"
BLUEPRINTS = ROOT / "docs" / "assessment-reference" / "question-blueprints"
ASSESSMENTS = ROOT / "data" / "assessments"

MANIFESTS.mkdir(parents=True, exist_ok=True)
BLUEPRINTS.mkdir(parents=True, exist_ok=True)

def dump(path, data):
    path.write_text(yaml.safe_dump(data, sort_keys=False, indent=2), encoding="utf-8")

# 1. Content Manifests
power_series_manifest = {
    "schemaVersion": 1,
    "id": "calc2-power-series-manifest",
    "categoryId": "calculus-2",
    "topicId": "power-series",
    "objectiveId": "calc2-obj-power-series",
    "sourceId": "src-20260719182540-a40fdcd443",
    "reviewState": "approved",
    "artifacts": [
        {
            "assessmentId": "calc2-power-series-worked-example",
            "objectiveIds": ["calc2-obj-power-series"],
            "sourceChunkIds": ["src-20260719182540-a40fdcd443:chunk-2095", "src-20260719182540-a40fdcd443:chunk-2104"],
            "requiresVisual": False
        }
    ]
}
dump(MANIFESTS / "calc2-power-series.yaml", power_series_manifest)

taylor_maclaurin_manifest = {
    "schemaVersion": 1,
    "id": "calc2-taylor-maclaurin-manifest",
    "categoryId": "calculus-2",
    "topicId": "taylor-maclaurin",
    "objectiveId": "calc2-obj-taylor-maclaurin",
    "sourceId": "src-20260719182540-a40fdcd443",
    "reviewState": "approved",
    "artifacts": [
        {
            "assessmentId": "calc2-taylor-maclaurin-worked-example",
            "objectiveIds": ["calc2-obj-taylor-maclaurin"],
            "sourceChunkIds": ["src-20260719182540-a40fdcd443:chunk-2112", "src-20260719182540-a40fdcd443:chunk-2165"],
            "requiresVisual": False
        }
    ]
}
dump(MANIFESTS / "calc2-taylor-maclaurin.yaml", taylor_maclaurin_manifest)

# 2. Question Blueprints
blueprints = [
    {
        "id": "calc2-power-series-radius-interval",
        "objectiveId": "calc2-obj-power-series",
        "archetype": "power-series-convergence",
        "questionType": "numericResponse",
        "givens": ["Power series expression"],
        "unknown": "Radius of convergence",
        "requiresDiagram": False,
        "governingPrinciple": "The Ratio Test determines the radius of convergence for a power series.",
        "methodSteps": [
            "Apply the Ratio Test to find the limit L.",
            "Set L < 1 to find the radius of convergence R."
        ],
        "likelyMisconception": "Forgetting to evaluate the absolute value or misinterpreting L.",
        "difficultyEvidence": "Requires limit evaluation and algebraic simplification of factorials/exponents.",
        "answerVerificationMethod": "independent-derivation",
        "variationAxes": ["series algebraic form", "target unknown (radius vs interval)"],
        "reasoningSignature": "Radius of convergence comes from the limit ratio of consecutive terms."
    },
    {
        "id": "calc2-power-series-endpoints",
        "objectiveId": "calc2-obj-power-series",
        "archetype": "power-series-endpoints",
        "questionType": "multipleChoice",
        "givens": ["Power series expression"],
        "unknown": "Convergence behavior at interval endpoints",
        "requiresDiagram": False,
        "governingPrinciple": "The Ratio Test is inconclusive at endpoints; specific series tests must be applied.",
        "methodSteps": [
            "Identify the radius R and the center a.",
            "Substitute x = a + R and x = a - R into the series.",
            "Apply Alternating Series Test, p-series, or other convergence tests."
        ],
        "likelyMisconception": "Assuming convergence is symmetrical at both endpoints.",
        "difficultyEvidence": "Requires synthesis of multiple convergence tests.",
        "answerVerificationMethod": "independent-derivation",
        "variationAxes": ["endpoint to test", "underlying convergence test type"],
        "reasoningSignature": "Endpoints must be checked individually using classical series tests."
    },
    {
        "id": "calc2-taylor-maclaurin-expansion",
        "objectiveId": "calc2-obj-taylor-maclaurin",
        "archetype": "taylor-maclaurin-expansion",
        "questionType": "symbolicResponse",
        "givens": ["Function f(x)", "Center point a", "Degree n"],
        "unknown": "Taylor polynomial T_n(x)",
        "requiresDiagram": False,
        "governingPrinciple": "The coefficients of a Taylor series are c_n = f^(n)(a) / n!.",
        "methodSteps": [
            "Compute derivatives up to degree n.",
            "Evaluate derivatives at x=a.",
            "Construct polynomial using Taylor formula."
        ],
        "likelyMisconception": "Forgetting the factorial in the denominator.",
        "difficultyEvidence": "Successive derivatives and correct assembly of the polynomial.",
        "answerVerificationMethod": "independent-derivation",
        "variationAxes": ["function form (exp, trig, rational)", "center a", "degree n"],
        "reasoningSignature": "Taylor polynomials approximate a function using its local derivatives."
    },
    {
        "id": "calc2-taylor-maclaurin-evaluation",
        "objectiveId": "calc2-obj-taylor-maclaurin",
        "archetype": "taylor-maclaurin-evaluation",
        "questionType": "numericResponse",
        "givens": ["Known Maclaurin series", "Value to approximate"],
        "unknown": "Approximate value or exact sum",
        "requiresDiagram": False,
        "governingPrinciple": "Standard series (e^x, sin x, cos x, 1/(1-x)) can be evaluated at specific x.",
        "methodSteps": [
            "Identify the standard Maclaurin series.",
            "Substitute the specific value for x.",
            "Compute the infinite sum."
        ],
        "likelyMisconception": "Failing to recognize the standard series form.",
        "difficultyEvidence": "Pattern recognition of standard Maclaurin series.",
        "answerVerificationMethod": "independent-derivation",
        "variationAxes": ["standard series type", "substitution value"],
        "reasoningSignature": "Infinite sums can be exactly evaluated by recognizing standard Maclaurin series evaluated at a point."
    }
]
dump(BLUEPRINTS / "calc2-infinite-series-blueprints.yaml", blueprints)

print("Manifests and Blueprints created.")
