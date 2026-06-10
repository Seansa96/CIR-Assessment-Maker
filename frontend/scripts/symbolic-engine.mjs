import { ComputeEngine } from "@cortex-js/compute-engine";

const input = await readStdin();

try {
  const request = JSON.parse(input);
  const submittedLatex = field(request, "submittedLatex", "SubmittedLatex");
  const expectedLatex = field(request, "expectedLatex", "ExpectedLatex");
  const mode = field(request, "equivalenceMode", "EquivalenceMode") || "expression";
  const variables = field(request, "variables", "Variables") || [];
  const tolerance = Number(field(request, "tolerance", "Tolerance") ?? 0);

  const result = compare(submittedLatex, expectedLatex, mode, variables, tolerance);
  process.stdout.write(JSON.stringify(result));
} catch (error) {
  process.stdout.write(JSON.stringify({
    isEquivalent: false,
    parseSucceeded: false,
    normalizedSubmitted: null,
    normalizedExpected: null,
    reason: "Symbolic comparison failed."
  }));
}

function compare(submittedLatex, expectedLatex, mode, variables, tolerance) {
  const ce = new ComputeEngine();
  const submitted = ce.parse(submittedLatex);
  const expected = ce.parse(expectedLatex);

  if (containsError(submitted.json)) {
    return failed(submitted, expected, mode, "Submitted answer could not be parsed.");
  }

  if (containsError(expected.json)) {
    return failed(submitted, expected, mode, "Expected answer could not be parsed.");
  }

  const compared = mode.toLowerCase() === "derivative"
    ? derivativeDifference(ce, submitted, expected, variables[0])
    : submitted.sub(expected);
  const simplified = compared.simplify();

  if (!containsError(simplified.json) && isZero(simplified)) {
    return passed(submitted, expected, mode, "Expressions simplified to the same value.");
  }

  if (variables.length > 0 && numericSamplesPass(submittedLatex, expectedLatex, mode, variables, tolerance)) {
    return passed(submitted, expected, mode, "Expressions matched across numeric samples.");
  }

  return {
    isEquivalent: false,
    parseSucceeded: true,
    normalizedSubmitted: submitted.latex,
    normalizedExpected: expected.latex,
    reason: "Submitted expression is not equivalent to the expected answer."
  };
}

function derivativeDifference(ce, submitted, expected, variable) {
  if (!variable) {
    return ce.box(["Error", "'missing-variable'"]);
  }

  const submittedDerivative = ce.box(["D", submitted.json, variable]).evaluate().simplify();
  const expectedDerivative = ce.box(["D", expected.json, variable]).evaluate().simplify();
  return submittedDerivative.sub(expectedDerivative);
}

function numericSamplesPass(submittedLatex, expectedLatex, mode, variables, tolerance) {
  const samples = [-2, -1, 0.5, 1, 2, 3];

  for (const sample of samples) {
    const ce = new ComputeEngine();
    const submitted = ce.parse(submittedLatex);
    const expected = ce.parse(expectedLatex);
    for (const variable of variables) {
      ce.assign(variable, sample);
    }

    const difference = mode.toLowerCase() === "derivative"
      ? derivativeDifference(ce, submitted, expected, variables[0])
      : submitted.sub(expected);
    const value = difference.N().numericValue;

    if (typeof value !== "number" || !Number.isFinite(value) || Math.abs(value) > tolerance) {
      return false;
    }
  }

  return true;
}

function isZero(expression) {
  if (expression.numericValue === 0) {
    return true;
  }

  return expression.latex === "0" || JSON.stringify(expression.json) === "0";
}

function containsError(value) {
  if (Array.isArray(value)) {
    return value.some(containsError);
  }

  return value === "Error";
}

function passed(submitted, expected, mode, reason) {
  return {
    isEquivalent: true,
    parseSucceeded: true,
    normalizedSubmitted: submitted.latex,
    normalizedExpected: expected.latex,
    equivalenceMode: mode,
    reason
  };
}

function failed(submitted, expected, mode, reason) {
  return {
    isEquivalent: false,
    parseSucceeded: false,
    normalizedSubmitted: submitted?.latex ?? null,
    normalizedExpected: expected?.latex ?? null,
    equivalenceMode: mode,
    reason
  };
}

function field(value, camelName, pascalName) {
  return value[camelName] ?? value[pascalName];
}

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", chunk => {
      data += chunk;
    });
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });
}
