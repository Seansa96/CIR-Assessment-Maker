# Issue Signals Reference

This document lists all available issue signals supported by the CIR Assessment Maker, grouped by domain.

## Algebra

### `sign-error`
- **Description**: Incorrectly handled positive or negative signs during algebraic or arithmetic manipulation.
- **Also applies to**: arithmetic, precalculus, calculus-1, calculus-2, physics-1

### `fraction-arithmetic-error`
- **Description**: Failed to correctly add, subtract, multiply, or divide fractions (e.g., missing common denominator).
- **Also applies to**: arithmetic, calculus-2

### `order-of-operations-error`
- **Description**: Performed operations in the wrong sequence (e.g., addition before multiplication).
- **Also applies to**: arithmetic, calculus-2

### `exponent-rule-misapplied`
- **Description**: Incorrectly applied the rules of exponents (e.g., adding exponents when bases are multiplied).
- **Also applies to**: precalculus, calculus-1, calculus-2

### `algebraic-simplification-error`
- **Description**: Made an error when distributing terms, factoring polynomials, or simplifying algebraic expressions.
- **Also applies to**: precalculus, calculus-1, calculus-2

### `mathematical-translation-error`
- **Description**: Failed to correctly translate a word problem or physical scenario into a mathematical equation.
- **Also applies to**: precalculus, calculus-1, physics-1, calculus-2

### `incorrect-model-selection`
- **Description**: Chose the wrong type of mathematical function (e.g., linear vs exponential) to model a given scenario.
- **Also applies to**: precalculus, calculus-2

### `domain-range-misidentified`
- **Description**: Incorrectly identified or restricted the domain or range of a function.
- **Also applies to**: precalculus, calculus-1, calculus-2

### `function-composition-error`
- **Description**: Made an error when evaluating or constructing a composite function f(g(x)).
- **Also applies to**: precalculus, calculus-1, calculus-2

### `inverse-function-error`
- **Description**: Failed to correctly find or evaluate the inverse of a function.
- **Also applies to**: precalculus, calculus-2

### `asymptote-identification-failure`
- **Description**: Incorrectly identified vertical, horizontal, or slant asymptotes of a function.
- **Also applies to**: precalculus, calculus-1

### `function-analysis-error`
- **Description**: Failed to correctly analyze the overall behavior, roots, extrema, or end behavior of a function.
- **Also applies to**: precalculus, calculus-1, calculus-2

### `expression-equation-recognition-error`
- **Description**: Misidentified the structural form of an expression or equation, leading to the wrong solution strategy.
- **Also applies to**: precalculus, calculus-1, calculus-2, physics-1

### `proportionality-misidentified`
- **Description**: Failed to correctly identify or set up direct, inverse, or joint proportionality relationships.
- **Also applies to**: precalculus, geometry, physics-1

### `ratio-proportion-setup-error`
- **Description**: Incorrectly set up or cross-multiplied a ratio or proportion equation.
- **Also applies to**: arithmetic, geometry, calculus-2

## Arithmetic

### `sign-error`
- **Description**: Incorrectly handled positive or negative signs during algebraic or arithmetic manipulation.
- **Also applies to**: algebra, precalculus, calculus-1, calculus-2, physics-1

### `fraction-arithmetic-error`
- **Description**: Failed to correctly add, subtract, multiply, or divide fractions (e.g., missing common denominator).
- **Also applies to**: algebra, calculus-2

### `order-of-operations-error`
- **Description**: Performed operations in the wrong sequence (e.g., addition before multiplication).
- **Also applies to**: algebra, calculus-2

### `ratio-proportion-setup-error`
- **Description**: Incorrectly set up or cross-multiplied a ratio or proportion equation.
- **Also applies to**: algebra, geometry, calculus-2

## C++

### `syntax-error`
- **Description**: Made a foundational syntax mistake (e.g., missing semicolon, unmatched brackets) that prevents compilation or execution.
- **Also applies to**: computer-science, scripting, python, csharp, typescript, pwsh

### `lifetime-management-error`
- **Description**: Failed to properly manage the lifetime of an object, leading to premature destruction or dangling references.
- **Also applies to**: computer-science, csharp

### `memory-management-error`
- **Description**: Failed to properly allocate or free memory, leading to leaks or segmentation faults.
- **Also applies to**: computer-science

### `missing-prototype-error`
- **Description**: Failed to provide a forward declaration or prototype for a function before its invocation.
- **Also applies to**: computer-science

### `class-inheritance-error`
- **Description**: Misapplied object-oriented inheritance principles, such as incorrect overriding, shadowing, or interface implementation.
- **Also applies to**: computer-science, csharp, python, typescript

### `type-constraint-violation`
- **Description**: Violated strict typing rules, such as attempting to assign an incompatible type without an explicit cast.
- **Also applies to**: computer-science, csharp, typescript

### `import-dependency-error`
- **Description**: Failed to correctly import a required library, module, or namespace.
- **Also applies to**: computer-science, scripting, python, typescript, csharp

### `pointer-arithmetic-error`
- **Description**: Incorrectly calculated memory addresses using pointer arithmetic.
- **Also applies to**: computer-science

### `concurrency-race-condition-error`
- **Description**: Failed to synchronize shared state across multiple threads, leading to a race condition or deadlock.
- **Also applies to**: computer-science, csharp

## Calculus-1

### `sign-error`
- **Description**: Incorrectly handled positive or negative signs during algebraic or arithmetic manipulation.
- **Also applies to**: arithmetic, algebra, precalculus, calculus-2, physics-1

### `exponent-rule-misapplied`
- **Description**: Incorrectly applied the rules of exponents (e.g., adding exponents when bases are multiplied).
- **Also applies to**: algebra, precalculus, calculus-2

### `logarithm-property-misapplied`
- **Description**: Incorrectly applied the properties of logarithms (e.g., expanding log(a+b) instead of log(ab)).
- **Also applies to**: precalculus, calculus-2

### `algebraic-simplification-error`
- **Description**: Made an error when distributing terms, factoring polynomials, or simplifying algebraic expressions.
- **Also applies to**: algebra, precalculus, calculus-2

### `trigonometric-identity-misapplied`
- **Description**: Incorrectly applied or failed to recognize a necessary trigonometric identity (e.g., double angle, Pythagorean).
- **Also applies to**: trigonometry, precalculus, calculus-2

### `power-rule-error`
- **Description**: Incorrectly applied the power rule for derivatives or integrals.
- **Also applies to**: calculus-2, physics-1

### `chain-rule-missed`
- **Description**: Failed to apply the chain rule when differentiating a composite function, or applied it incorrectly.
- **Also applies to**: calculus-2

### `product-rule-misapplied`
- **Description**: Failed to correctly use the product rule for differentiation.
- **Also applies to**: calculus-2

### `quotient-rule-misapplied`
- **Description**: Failed to correctly use the quotient rule for differentiation, often involving a sign error in the numerator.
- **Also applies to**: calculus-2

### `limit-evaluation-error`
- **Description**: Incorrectly evaluated a limit, such as failing to apply L'Hopital's rule or factoring incorrectly.
- **Also applies to**: calculus-2

### `u-substitution-failure`
- **Description**: Chose an incorrect 'u' or failed to correctly substitute 'du' when evaluating an integral.
- **Also applies to**: calculus-2

### `geometric-area-formula-error`
- **Description**: Used an incorrect formula or made an error calculating the area of a 2D shape.
- **Also applies to**: geometry, precalculus, calculus-2

### `geometric-volume-formula-error`
- **Description**: Used an incorrect formula or made an error calculating the volume of a 3D solid.
- **Also applies to**: geometry, precalculus, calculus-2

### `mathematical-translation-error`
- **Description**: Failed to correctly translate a word problem or physical scenario into a mathematical equation.
- **Also applies to**: algebra, precalculus, physics-1, calculus-2

### `boundary-condition-failure`
- **Description**: Failed to correctly apply initial values or boundary conditions when modeling a system.
- **Also applies to**: calculus-2, physics-1

### `domain-range-misidentified`
- **Description**: Incorrectly identified or restricted the domain or range of a function.
- **Also applies to**: algebra, precalculus, calculus-2

### `function-composition-error`
- **Description**: Made an error when evaluating or constructing a composite function f(g(x)).
- **Also applies to**: algebra, precalculus, calculus-2

### `asymptote-identification-failure`
- **Description**: Incorrectly identified vertical, horizontal, or slant asymptotes of a function.
- **Also applies to**: algebra, precalculus

### `double-angle-identity-misapplied`
- **Description**: Incorrectly applied or failed to recognize a double-angle trigonometric identity.
- **Also applies to**: trigonometry, precalculus, calculus-2

### `half-angle-identity-misapplied`
- **Description**: Incorrectly applied or failed to recognize a half-angle trigonometric identity.
- **Also applies to**: trigonometry, precalculus, calculus-2

### `pythagorean-identity-misapplied`
- **Description**: Incorrectly applied a Pythagorean trigonometric identity (e.g., sin^2 + cos^2 = 1).
- **Also applies to**: trigonometry, precalculus, calculus-2

### `sum-difference-identity-misapplied`
- **Description**: Incorrectly applied the sum or difference identity for sine, cosine, or tangent.
- **Also applies to**: trigonometry, precalculus, calculus-2

### `first-derivative-test-misapplied`
- **Description**: Incorrectly used the first derivative to determine increasing/decreasing intervals or local extrema.

### `second-derivative-test-misapplied`
- **Description**: Incorrectly used the second derivative to determine concavity or points of inflection.

### `critical-point-misidentified`
- **Description**: Failed to correctly locate critical points where the derivative is zero or undefined.

### `function-analysis-error`
- **Description**: Failed to correctly analyze the overall behavior, roots, extrema, or end behavior of a function.
- **Also applies to**: algebra, precalculus, calculus-2

### `expression-equation-recognition-error`
- **Description**: Misidentified the structural form of an expression or equation, leading to the wrong solution strategy.
- **Also applies to**: algebra, precalculus, calculus-2, physics-1

## Calculus-2

### `sign-error`
- **Description**: Incorrectly handled positive or negative signs during algebraic or arithmetic manipulation.
- **Also applies to**: arithmetic, algebra, precalculus, calculus-1, physics-1

### `fraction-arithmetic-error`
- **Description**: Failed to correctly add, subtract, multiply, or divide fractions (e.g., missing common denominator).
- **Also applies to**: arithmetic, algebra

### `order-of-operations-error`
- **Description**: Performed operations in the wrong sequence (e.g., addition before multiplication).
- **Also applies to**: arithmetic, algebra

### `exponent-rule-misapplied`
- **Description**: Incorrectly applied the rules of exponents (e.g., adding exponents when bases are multiplied).
- **Also applies to**: algebra, precalculus, calculus-1

### `logarithm-property-misapplied`
- **Description**: Incorrectly applied the properties of logarithms (e.g., expanding log(a+b) instead of log(ab)).
- **Also applies to**: precalculus, calculus-1

### `algebraic-simplification-error`
- **Description**: Made an error when distributing terms, factoring polynomials, or simplifying algebraic expressions.
- **Also applies to**: algebra, precalculus, calculus-1

### `partial-fraction-decomposition-error`
- **Description**: Failed to correctly set up or solve for coefficients during partial fraction decomposition.
- **Also applies to**: precalculus

### `trigonometric-identity-misapplied`
- **Description**: Incorrectly applied or failed to recognize a necessary trigonometric identity (e.g., double angle, Pythagorean).
- **Also applies to**: trigonometry, precalculus, calculus-1

### `power-rule-error`
- **Description**: Incorrectly applied the power rule for derivatives or integrals.
- **Also applies to**: calculus-1, physics-1

### `chain-rule-missed`
- **Description**: Failed to apply the chain rule when differentiating a composite function, or applied it incorrectly.
- **Also applies to**: calculus-1

### `product-rule-misapplied`
- **Description**: Failed to correctly use the product rule for differentiation.
- **Also applies to**: calculus-1

### `quotient-rule-misapplied`
- **Description**: Failed to correctly use the quotient rule for differentiation, often involving a sign error in the numerator.
- **Also applies to**: calculus-1

### `limit-evaluation-error`
- **Description**: Incorrectly evaluated a limit, such as failing to apply L'Hopital's rule or factoring incorrectly.
- **Also applies to**: calculus-1

### `u-substitution-failure`
- **Description**: Chose an incorrect 'u' or failed to correctly substitute 'du' when evaluating an integral.
- **Also applies to**: calculus-1

### `integration-by-parts-misapplied`
- **Description**: Incorrectly assigned 'u' and 'dv', or made an error in the integration by parts formula: uv - integral(v du).

### `trigonometric-substitution-error`
- **Description**: Failed to set up the correct trigonometric substitution or forgot to convert back to 'x' at the end.

### `improper-integral-bounds-error`
- **Description**: Failed to correctly evaluate an improper integral using limits, or ignored an infinite discontinuity.

### `power-series-expansion-error`
- **Description**: Incorrectly generated a Maclaurin or Taylor series expansion for a function.

### `geometric-area-formula-error`
- **Description**: Used an incorrect formula or made an error calculating the area of a 2D shape.
- **Also applies to**: geometry, precalculus, calculus-1

### `geometric-volume-formula-error`
- **Description**: Used an incorrect formula or made an error calculating the volume of a 3D solid.
- **Also applies to**: geometry, precalculus, calculus-1

### `pythagorean-theorem-misapplied`
- **Description**: Failed to correctly apply the Pythagorean theorem for right triangles.
- **Also applies to**: geometry, trigonometry, physics-1

### `mathematical-translation-error`
- **Description**: Failed to correctly translate a word problem or physical scenario into a mathematical equation.
- **Also applies to**: algebra, precalculus, calculus-1, physics-1

### `incorrect-model-selection`
- **Description**: Chose the wrong type of mathematical function (e.g., linear vs exponential) to model a given scenario.
- **Also applies to**: algebra, precalculus

### `boundary-condition-failure`
- **Description**: Failed to correctly apply initial values or boundary conditions when modeling a system.
- **Also applies to**: calculus-1, physics-1

### `domain-range-misidentified`
- **Description**: Incorrectly identified or restricted the domain or range of a function.
- **Also applies to**: algebra, precalculus, calculus-1

### `function-composition-error`
- **Description**: Made an error when evaluating or constructing a composite function f(g(x)).
- **Also applies to**: algebra, precalculus, calculus-1

### `inverse-function-error`
- **Description**: Failed to correctly find or evaluate the inverse of a function.
- **Also applies to**: algebra, precalculus

### `double-angle-identity-misapplied`
- **Description**: Incorrectly applied or failed to recognize a double-angle trigonometric identity.
- **Also applies to**: trigonometry, precalculus, calculus-1

### `half-angle-identity-misapplied`
- **Description**: Incorrectly applied or failed to recognize a half-angle trigonometric identity.
- **Also applies to**: trigonometry, precalculus, calculus-1

### `pythagorean-identity-misapplied`
- **Description**: Incorrectly applied a Pythagorean trigonometric identity (e.g., sin^2 + cos^2 = 1).
- **Also applies to**: trigonometry, precalculus, calculus-1

### `sum-difference-identity-misapplied`
- **Description**: Incorrectly applied the sum or difference identity for sine, cosine, or tangent.
- **Also applies to**: trigonometry, precalculus, calculus-1

### `series-test-selection-error`
- **Description**: Selected an inappropriate convergence test for a given infinite series.

### `ratio-test-evaluation-error`
- **Description**: Made an error setting up or evaluating the limit for the Ratio Test.

### `root-test-evaluation-error`
- **Description**: Made an error setting up or evaluating the limit for the Root Test.

### `alternating-series-test-error`
- **Description**: Failed to correctly verify the conditions for the Alternating Series Test.

### `integral-test-error`
- **Description**: Failed to verify conditions or incorrectly evaluated the improper integral for the Integral Test.

### `p-series-misidentified`
- **Description**: Misidentified a p-series or incorrectly concluded convergence/divergence based on p.

### `geometric-series-convergence-error`
- **Description**: Incorrectly calculated the sum of a geometric series or misidentified its convergence criteria.

### `parametric-derivative-error`
- **Description**: Failed to correctly calculate dy/dx or d2y/dx2 for a set of parametric equations.

### `parametric-arc-length-error`
- **Description**: Set up or evaluated the arc length integral for parametric equations incorrectly.

### `conic-section-misidentified`
- **Description**: Incorrectly identified a conic section (circle, ellipse, parabola, hyperbola) from its equation.
- **Also applies to**: precalculus

### `polar-rectangular-conversion-error`
- **Description**: Made an error converting between polar (r, theta) and rectangular (x, y) coordinates.
- **Also applies to**: precalculus

### `polar-area-calculation-error`
- **Description**: Set up or evaluated the area integral for a polar curve incorrectly.

### `polar-derivative-error`
- **Description**: Failed to correctly calculate the derivative dy/dx for a polar curve.

### `function-analysis-error`
- **Description**: Failed to correctly analyze the overall behavior, roots, extrema, or end behavior of a function.
- **Also applies to**: algebra, precalculus, calculus-1

### `expression-equation-recognition-error`
- **Description**: Misidentified the structural form of an expression or equation, leading to the wrong solution strategy.
- **Also applies to**: algebra, precalculus, calculus-1, physics-1

### `ratio-proportion-setup-error`
- **Description**: Incorrectly set up or cross-multiplied a ratio or proportion equation.
- **Also applies to**: arithmetic, algebra, geometry

## Chemistry

### `stoichiometry-ratio-error`
- **Description**: Failed to use the correct molar ratio from a balanced chemical equation during stoichiometric calculations.

### `chemical-equation-balancing-error`
- **Description**: Failed to correctly balance a chemical equation before proceeding with calculations.

### `molar-mass-calculation-error`
- **Description**: Made an error calculating the molar mass of a compound from the periodic table.

### `ideal-gas-law-misapplied`
- **Description**: Incorrectly applied the ideal gas law (PV=nRT) or used inconsistent units for the gas constant R.
- **Also applies to**: physics-1

### `limiting-reactant-misidentified`
- **Description**: Failed to identify the correct limiting reactant in a chemical reaction.

### `oxidation-state-assignment-error`
- **Description**: Incorrectly assigned oxidation numbers or states to atoms in a molecule or ion.

### `le-chateliers-principle-misapplied`
- **Description**: Incorrectly predicted the shift in chemical equilibrium when a stress (e.g., pressure, temperature, concentration) is applied.

### `ph-poh-calculation-error`
- **Description**: Failed to correctly calculate pH, pOH, [H+], or [OH-] using logarithmic relationships.

### `conjugate-acid-base-misidentified`
- **Description**: Failed to correctly identify the conjugate acid or base of a given chemical species.

### `strong-weak-acid-base-confusion`
- **Description**: Treated a weak acid or base as strong (or vice versa), typically leading to errors in ICE table setups.

### `reaction-type-misidentified`
- **Description**: Misidentified the general type of chemical reaction (e.g., synthesis, decomposition, single replacement, combustion).

### `precipitate-solubility-error`
- **Description**: Failed to use solubility rules to correctly identify a precipitate in a double replacement or net ionic reaction.

### `electronegativity-trend-error`
- **Description**: Incorrectly predicted or compared the electronegativity or electron affinity of elements based on periodic table trends.

### `atomic-radius-trend-error`
- **Description**: Incorrectly predicted or compared atomic or ionic radii across a period or down a group.

### `ionization-energy-trend-error`
- **Description**: Incorrectly predicted or compared the first or successive ionization energies of elements.

### `isotope-subatomic-particle-error`
- **Description**: Failed to correctly determine the number of protons, neutrons, or electrons in a specific isotope or ion.

### `electron-configuration-error`
- **Description**: Incorrectly wrote the electron configuration or orbital diagram (e.g., violating Aufbau, Pauli, or Hund's rules).
- **Also applies to**: physics-1

### `phase-change-energy-calculation-error`
- **Description**: Failed to correctly calculate the heat required for a phase change, such as ignoring the latent heat of fusion or vaporization.
- **Also applies to**: physics-1

### `intermolecular-force-misidentified`
- **Description**: Misidentified the dominant intermolecular force (e.g., hydrogen bonding, dipole-dipole, or London dispersion) in a substance.

### `ionic-vs-covalent-bonding-confusion`
- **Description**: Incorrectly categorized a compound as ionic or covalent, or misunderstood the concepts of electron transfer versus sharing.

### `lewis-structure-octet-error`
- **Description**: Drew an incorrect Lewis structure by failing to satisfy the octet rule (when required) or miscalculating formal charges.

### `molecular-geometry-vsepr-error`
- **Description**: Incorrectly determined the molecular geometry, electron domain geometry, or bond angles using VSEPR theory.

### `ion-charge-misidentified`
- **Description**: Incorrectly identified the charge of a monatomic or transition metal ion, leading to incorrect chemical formulas.

### `polyatomic-ion-misidentified`
- **Description**: Failed to correctly recall the name, formula, or charge of a polyatomic ion, causing subsequent errors in formulas or balancing.

### `chemical-nomenclature-error`
- **Description**: Incorrectly named a compound or wrote its formula from the name, such as confusing -ite/-ate suffixes or ionic/covalent naming rules.

### `phase-classification-error`
- **Description**: Incorrectly classified a substance's phase of matter or failed to assign the correct state symbols (s, l, g, aq) in a reaction.
- **Also applies to**: physics-1

### `physical-vs-chemical-property-confusion`
- **Description**: Failed to correctly distinguish between a physical property and a chemical property.

### `physical-vs-chemical-change-confusion`
- **Description**: Failed to correctly distinguish between a physical change (e.g., melting) and a chemical change (e.g., combustion).

### `intensive-vs-extensive-property-confusion`
- **Description**: Incorrectly categorized a property as intensive (e.g., density, temperature) or extensive (e.g., mass, volume).
- **Also applies to**: physics-1

### `enthalpy-sign-error`
- **Description**: Confused exothermic (negative delta H) with endothermic (positive delta H) processes.
- **Also applies to**: physics-1

### `hess-law-misapplied`
- **Description**: Failed to correctly reverse or scale reactions and their corresponding enthalpy changes when applying Hess's Law.

### `calorimetry-calculation-error`
- **Description**: Incorrectly applied q = mcΔT, such as using the wrong mass (system vs surroundings) or specific heat capacity.
- **Also applies to**: physics-1

### `entropy-prediction-error`
- **Description**: Incorrectly predicted the sign of the change in entropy (delta S) for a chemical or physical process.

### `gibbs-free-energy-misapplied`
- **Description**: Incorrectly evaluated delta G to determine reaction spontaneity, or made a sign/unit error in delta G = delta H - T*delta S.

### `colligative-property-calculation-error`
- **Description**: Incorrectly calculated freezing point depression, boiling point elevation, vapor pressure lowering, or osmotic pressure.

### `vant-hoff-factor-omitted`
- **Description**: Failed to include or correctly determine the van 't Hoff factor (i) for an electrolyte in solution calculations.

### `molarity-molality-confusion`
- **Description**: Confused molarity (moles/L solution) with molality (moles/kg solvent) in concentration or colligative property calculations.

## Computer-Science

### `syntax-error`
- **Description**: Made a foundational syntax mistake (e.g., missing semicolon, unmatched brackets) that prevents compilation or execution.
- **Also applies to**: scripting, python, csharp, c++, typescript, pwsh

### `variable-declaration-error`
- **Description**: Incorrectly declared or defined a variable, such as omitting a type or using an invalid identifier.
- **Also applies to**: scripting

### `uninitialized-variable-error`
- **Description**: Attempted to use or dereference a variable or object before it was properly initialized or assigned a value (e.g., Null Reference).
- **Also applies to**: scripting

### `scope-resolution-error`
- **Description**: Attempted to access a variable or function outside of its valid lexical or dynamic scope.
- **Also applies to**: scripting

### `instantiation-error`
- **Description**: Failed to correctly instantiate an object from a class or struct.

### `lifetime-management-error`
- **Description**: Failed to properly manage the lifetime of an object, leading to premature destruction or dangling references.
- **Also applies to**: c++, csharp

### `memory-management-error`
- **Description**: Failed to properly allocate or free memory, leading to leaks or segmentation faults.
- **Also applies to**: c++

### `function-declaration-error`
- **Description**: Incorrectly defined a function signature, return type, or parameter list.
- **Also applies to**: scripting

### `missing-prototype-error`
- **Description**: Failed to provide a forward declaration or prototype for a function before its invocation.
- **Also applies to**: c++

### `big-o-complexity-error`
- **Description**: Incorrectly evaluated or implemented the time or space complexity (Big O) of an algorithm.
- **Also applies to**: dsa

### `recursive-logic-misapplied`
- **Description**: Incorrectly implemented a recursive function, such as missing a base case or failing to progress toward it.
- **Also applies to**: dsa

### `class-inheritance-error`
- **Description**: Misapplied object-oriented inheritance principles, such as incorrect overriding, shadowing, or interface implementation.
- **Also applies to**: csharp, c++, python, typescript

### `loop-logic-error`
- **Description**: Implemented faulty loop logic, such as an incorrect condition or increment, causing unexpected iteration behavior.
- **Also applies to**: scripting

### `infinite-loop-error`
- **Description**: Created a loop with a condition that can never evaluate to false, causing execution to hang.
- **Also applies to**: scripting

### `off-by-one-error`
- **Description**: Iterated one time too many or too few, often resulting in an out-of-bounds array access.
- **Also applies to**: scripting

### `stack-overflow-error`
- **Description**: Exceeded the call stack limit, typically due to excessively deep or infinite recursion.
- **Also applies to**: dsa

### `bit-overflow-underflow-error`
- **Description**: Performed an operation that exceeded the maximum or minimum bounds of a numeric data type.

### `type-constraint-violation`
- **Description**: Violated strict typing rules, such as attempting to assign an incompatible type without an explicit cast.
- **Also applies to**: csharp, c++, typescript

### `overcomplication-error`
- **Description**: Implemented a convoluted or excessively complex solution when a much simpler, standard approach exists.
- **Also applies to**: scripting

### `simplification-error`
- **Description**: Oversimplified a problem, ignoring crucial constraints or edge cases required for correctness.
- **Also applies to**: scripting

### `edge-case-handling-failure`
- **Description**: Failed to account for edge cases such as empty collections, negative numbers, or boundary limits.
- **Also applies to**: scripting, dsa

### `import-dependency-error`
- **Description**: Failed to correctly import a required library, module, or namespace.
- **Also applies to**: scripting, python, typescript, csharp, c++

### `algorithm-misapplication-error`
- **Description**: Chose the wrong algorithm for the problem (e.g., using a sorting algorithm where a simple search would suffice).
- **Also applies to**: dsa

### `data-structure-misuse`
- **Description**: Chose an inappropriate data structure for the task, leading to severe inefficiency or logic errors (e.g., Array instead of HashSet for rapid lookups).
- **Also applies to**: dsa

### `pointer-arithmetic-error`
- **Description**: Incorrectly calculated memory addresses using pointer arithmetic.
- **Also applies to**: c++

### `modular-arithmetic-error`
- **Description**: Incorrectly applied the modulo operator or modular arithmetic rules.
- **Also applies to**: math

### `function-modeling-from-scenario-error`
- **Description**: Failed to correctly translate a real-world scenario or specification into a programmatic function or class model.
- **Also applies to**: scripting

### `concurrency-race-condition-error`
- **Description**: Failed to synchronize shared state across multiple threads, leading to a race condition or deadlock.
- **Also applies to**: csharp, c++

## Csharp

### `syntax-error`
- **Description**: Made a foundational syntax mistake (e.g., missing semicolon, unmatched brackets) that prevents compilation or execution.
- **Also applies to**: computer-science, scripting, python, c++, typescript, pwsh

### `lifetime-management-error`
- **Description**: Failed to properly manage the lifetime of an object, leading to premature destruction or dangling references.
- **Also applies to**: computer-science, c++

### `class-inheritance-error`
- **Description**: Misapplied object-oriented inheritance principles, such as incorrect overriding, shadowing, or interface implementation.
- **Also applies to**: computer-science, c++, python, typescript

### `type-constraint-violation`
- **Description**: Violated strict typing rules, such as attempting to assign an incompatible type without an explicit cast.
- **Also applies to**: computer-science, c++, typescript

### `import-dependency-error`
- **Description**: Failed to correctly import a required library, module, or namespace.
- **Also applies to**: computer-science, scripting, python, typescript, c++

### `concurrency-race-condition-error`
- **Description**: Failed to synchronize shared state across multiple threads, leading to a race condition or deadlock.
- **Also applies to**: computer-science, c++

## Dsa

### `big-o-complexity-error`
- **Description**: Incorrectly evaluated or implemented the time or space complexity (Big O) of an algorithm.
- **Also applies to**: computer-science

### `recursive-logic-misapplied`
- **Description**: Incorrectly implemented a recursive function, such as missing a base case or failing to progress toward it.
- **Also applies to**: computer-science

### `stack-overflow-error`
- **Description**: Exceeded the call stack limit, typically due to excessively deep or infinite recursion.
- **Also applies to**: computer-science

### `edge-case-handling-failure`
- **Description**: Failed to account for edge cases such as empty collections, negative numbers, or boundary limits.
- **Also applies to**: computer-science, scripting

### `algorithm-misapplication-error`
- **Description**: Chose the wrong algorithm for the problem (e.g., using a sorting algorithm where a simple search would suffice).
- **Also applies to**: computer-science

### `data-structure-misuse`
- **Description**: Chose an inappropriate data structure for the task, leading to severe inefficiency or logic errors (e.g., Array instead of HashSet for rapid lookups).
- **Also applies to**: computer-science

## Geometry

### `geometric-area-formula-error`
- **Description**: Used an incorrect formula or made an error calculating the area of a 2D shape.
- **Also applies to**: precalculus, calculus-1, calculus-2

### `geometric-volume-formula-error`
- **Description**: Used an incorrect formula or made an error calculating the volume of a 3D solid.
- **Also applies to**: precalculus, calculus-1, calculus-2

### `pythagorean-theorem-misapplied`
- **Description**: Failed to correctly apply the Pythagorean theorem for right triangles.
- **Also applies to**: trigonometry, physics-1, calculus-2

### `angle-relationship-misidentified`
- **Description**: Misidentified supplementary, complementary, or other geometric angle relationships.
- **Also applies to**: trigonometry

### `law-of-sines-misapplied`
- **Description**: Incorrectly applied the Law of Sines, or failed to check for the ambiguous case (SSA).
- **Also applies to**: trigonometry, precalculus

### `law-of-cosines-misapplied`
- **Description**: Incorrectly applied the Law of Cosines when solving an oblique triangle.
- **Also applies to**: trigonometry, precalculus

### `circular-properties-error`
- **Description**: Failed to apply or correctly calculate properties of a circle such as arc length, sector area, or inscribed angles.
- **Also applies to**: trigonometry, precalculus

### `triangle-properties-error`
- **Description**: Failed to apply basic triangle properties such as the sum of interior angles or side length inequalities.
- **Also applies to**: trigonometry

### `transversal-angle-theorem-error`
- **Description**: Failed to correctly identify or relate alternate interior, alternate exterior, or corresponding angles formed by a transversal intersecting parallel lines.
- **Also applies to**: trigonometry

### `exterior-angle-theorem-misapplied`
- **Description**: Failed to correctly apply the exterior angle theorem for triangles (the exterior angle equals the sum of the two opposite interior angles).
- **Also applies to**: trigonometry

### `complementary-supplementary-angle-error`
- **Description**: Failed to recognize or correctly calculate that complementary angles sum to 90 degrees, or supplementary angles sum to 180 degrees.
- **Also applies to**: trigonometry

### `proportionality-misidentified`
- **Description**: Failed to correctly identify or set up direct, inverse, or joint proportionality relationships.
- **Also applies to**: algebra, precalculus, physics-1

### `ratio-proportion-setup-error`
- **Description**: Incorrectly set up or cross-multiplied a ratio or proportion equation.
- **Also applies to**: arithmetic, algebra, calculus-2

## Math

### `modular-arithmetic-error`
- **Description**: Incorrectly applied the modulo operator or modular arithmetic rules.
- **Also applies to**: computer-science

## Physics-1

### `sign-error`
- **Description**: Incorrectly handled positive or negative signs during algebraic or arithmetic manipulation.
- **Also applies to**: arithmetic, algebra, precalculus, calculus-1, calculus-2

### `power-rule-error`
- **Description**: Incorrectly applied the power rule for derivatives or integrals.
- **Also applies to**: calculus-1, calculus-2

### `pythagorean-theorem-misapplied`
- **Description**: Failed to correctly apply the Pythagorean theorem for right triangles.
- **Also applies to**: geometry, trigonometry, calculus-2

### `mathematical-translation-error`
- **Description**: Failed to correctly translate a word problem or physical scenario into a mathematical equation.
- **Also applies to**: algebra, precalculus, calculus-1, calculus-2

### `boundary-condition-failure`
- **Description**: Failed to correctly apply initial values or boundary conditions when modeling a system.
- **Also applies to**: calculus-1, calculus-2

### `vector-component-resolution-error`
- **Description**: Failed to correctly break a vector into x and y components using trigonometry (e.g., swapped sine and cosine).

### `kinematic-equation-misapplied`
- **Description**: Chose the wrong kinematic equation or applied it with incorrect knowns/unknowns for constant acceleration.

### `projectile-motion-independence-error`
- **Description**: Failed to treat horizontal and vertical motion independently in projectile problems.

### `free-body-diagram-missing-force`
- **Description**: Failed to identify and include a relevant force (e.g., friction, normal force, tension) on a free-body diagram.

### `newtons-second-law-sign-error`
- **Description**: Set up the net force equation (F=ma) with incorrect signs relative to the chosen coordinate system.

### `static-vs-kinetic-friction-error`
- **Description**: Used the wrong friction coefficient or modeled static friction as always equal to its maximum value (mu_s * N).

### `normal-force-miscalculated`
- **Description**: Assumed normal force always equals mg, ignoring other vertical forces, inclines, or accelerations.

### `conservation-of-energy-misapplied`
- **Description**: Failed to correctly account for all forms of initial and final mechanical energy, or non-conservative work.

### `conservation-of-momentum-misapplied`
- **Description**: Failed to conserve momentum in a collision or explosion, or treated momentum as a scalar instead of a vector.

### `elastic-vs-inelastic-collision-error`
- **Description**: Assumed kinetic energy is conserved in an inelastic collision, or failed to conserve it in an elastic one.

### `work-energy-theorem-error`
- **Description**: Incorrectly calculated work done by a force (e.g., missing the dot product angle) or failed to relate it to a change in kinetic energy.

### `torque-calculation-error`
- **Description**: Failed to correctly calculate torque, often by omitting the lever arm distance or the sine of the angle.

### `moment-of-inertia-misidentified`
- **Description**: Used the wrong moment of inertia formula for a specific extended rigid body geometry (e.g., solid sphere vs hollow shell).

### `conservation-of-angular-momentum-misapplied`
- **Description**: Failed to conserve angular momentum or calculate it correctly for a point particle vs a rigid body.

### `rolling-without-slipping-condition-missed`
- **Description**: Failed to apply the kinematic constraints for rolling without slipping (v = r*omega or a = r*alpha).

### `buoyant-force-miscalculated`
- **Description**: Failed to correctly apply Archimedes' principle, such as using the object's total volume instead of the displaced fluid volume.

### `bernoullis-equation-misapplied`
- **Description**: Incorrectly set up or solved Bernoulli's equation for fluid flow.

### `hookes-law-sign-error`
- **Description**: Failed to correctly account for the restoring nature (negative sign) of a spring force.

### `shm-period-frequency-confusion`
- **Description**: Confused angular frequency, linear frequency, and period, or used the wrong period formula (e.g., pendulum vs mass-spring).

### `relative-velocity-frame-error`
- **Description**: Failed to correctly add or subtract velocity vectors between different reference frames.

### `wave-speed-frequency-wavelength-error`
- **Description**: Incorrectly applied the relationship between wave speed, frequency, and wavelength (v = f * lambda).

### `standing-wave-harmonic-misidentified`
- **Description**: Misidentified the harmonic number, overtone, or node/antinode count for a standing wave in a pipe or string.

### `doppler-effect-sign-error`
- **Description**: Used the wrong signs for observer or source velocities in the Doppler effect formula.

### `sound-intensity-level-error`
- **Description**: Incorrectly applied the logarithmic decibel formula for sound intensity level.

### `expression-equation-recognition-error`
- **Description**: Misidentified the structural form of an expression or equation, leading to the wrong solution strategy.
- **Also applies to**: algebra, precalculus, calculus-1, calculus-2

### `proportionality-misidentified`
- **Description**: Failed to correctly identify or set up direct, inverse, or joint proportionality relationships.
- **Also applies to**: algebra, precalculus, geometry

### `ideal-gas-law-misapplied`
- **Description**: Incorrectly applied the ideal gas law (PV=nRT) or used inconsistent units for the gas constant R.
- **Also applies to**: chemistry

### `electron-configuration-error`
- **Description**: Incorrectly wrote the electron configuration or orbital diagram (e.g., violating Aufbau, Pauli, or Hund's rules).
- **Also applies to**: chemistry

### `phase-change-energy-calculation-error`
- **Description**: Failed to correctly calculate the heat required for a phase change, such as ignoring the latent heat of fusion or vaporization.
- **Also applies to**: chemistry

### `phase-classification-error`
- **Description**: Incorrectly classified a substance's phase of matter or failed to assign the correct state symbols (s, l, g, aq) in a reaction.
- **Also applies to**: chemistry

### `intensive-vs-extensive-property-confusion`
- **Description**: Incorrectly categorized a property as intensive (e.g., density, temperature) or extensive (e.g., mass, volume).
- **Also applies to**: chemistry

### `enthalpy-sign-error`
- **Description**: Confused exothermic (negative delta H) with endothermic (positive delta H) processes.
- **Also applies to**: chemistry

### `calorimetry-calculation-error`
- **Description**: Incorrectly applied q = mcΔT, such as using the wrong mass (system vs surroundings) or specific heat capacity.
- **Also applies to**: chemistry

### `newtons-third-law-pairing-error`
- **Description**: Paired forces on one object, or forces of different interactions, instead of the equal-and-opposite forces exerted by the two interacting objects.

### `newtons-first-law-inertia-error`
- **Description**: Assumed that motion requires a continuing net force or failed to distinguish constant velocity from acceleration.

### `mass-weight-distinction-error`
- **Description**: Confused invariant mass with weight, which depends on the local gravitational field.

### `tension-system-force-error`
- **Description**: Incorrectly related tension to the external pull or to the weights in an accelerating connected system.

### `inertia-trajectory-error`
- **Description**: Predicted a continuing curved path after a constraining force was removed instead of tangential inertial motion.

### `rotational-energy-conservation-error`
- **Description**: Assumed rotational kinetic energy is conserved when angular momentum is conserved despite a changing moment of inertia.

### `angular-momentum-vector-direction-error`
- **Description**: Used the right-hand rule incorrectly or treated angular momentum as a scalar rather than a vector.

### `rolling-energy-partition-error`
- **Description**: Misallocated energy between translational and rotational motion in a rolling system.

### `rolling-static-friction-role-error`
- **Description**: Misidentified the role of static friction in rolling without slipping, including its torque or work.

### `gyroscopic-precession-concept-error`
- **Description**: Misapplied the torque-angular-momentum relationship governing gyroscopic precession.

### `angular-impulse-concept-error`
- **Description**: Failed to connect net external torque over time with a change in angular momentum.

### `rotational-inelastic-collision-error`
- **Description**: Incorrectly treated a rotational sticking collision as conserving kinetic energy rather than angular momentum.

### `conservative-force-concept-error`
- **Description**: Misidentified a conservative force or its path-independent work and potential-energy relationship.

### `system-boundary-energy-error`
- **Description**: Used an inconsistent system boundary when classifying energy transfer or conservation.

### `power-work-rate-error`
- **Description**: Confused equal work with equal power or failed to account for the time over which work is done.

### `momentum-kinetic-energy-relationship-error`
- **Description**: Incorrectly compared kinetic energies for objects with equal momentum but different masses.

### `impulse-momentum-error`
- **Description**: Misapplied the impulse-momentum theorem or failed to recognize equal-and-opposite collision impulses.

### `center-of-mass-concept-error`
- **Description**: Incorrectly located or predicted the motion of a system's center of mass.

### `potential-energy-force-relationship-error`
- **Description**: Failed to use the negative slope of a potential-energy curve to determine force.

### `spring-energy-proportionality-error`
- **Description**: Used a linear rather than quadratic relationship between spring displacement and elastic potential energy.

### `rotational-concept-misunderstood`
- **Description**: Misunderstood a foundational relationship among angular variables, torque, rotational energy, or rotational motion.

### `trigonometry-error`
- **Description**: Applied a trigonometric relationship or angular dependence incorrectly in a physics calculation or interpretation.

### `torque-force-confusion`
- **Description**: Confused force with torque or omitted the force direction and lever-arm dependence of torque.

### `inertia-mass-confusion`
- **Description**: Confused total mass with moment of inertia or ignored how mass distribution affects rotation.

### `linear-angular-confusion`
- **Description**: Confused analogous linear and angular quantities, units, or kinematic relationships.

### `lever-arm-confusion`
- **Description**: Used the wrong perpendicular distance from the axis when reasoning about torque.

### `unit-conversion-error`
- **Description**: Converted physical units incorrectly or used incompatible units in a calculation.

### `apparent-weight-buoyancy-error`
- **Description**: Legacy assessment issue signal: apparent weight buoyancy error.

### `area-length-stiffness-scaling-error`
- **Description**: Legacy assessment issue signal: area length stiffness scaling error.

### `beam-bending-stress-error`
- **Description**: Legacy assessment issue signal: beam bending stress error.

### `bulk-modulus-compressibility-error`
- **Description**: Legacy assessment issue signal: bulk modulus compressibility error.

### `buoyancy-displacement-error`
- **Description**: Legacy assessment issue signal: buoyancy displacement error.

### `buoyancy-surface-confusion`
- **Description**: Legacy assessment issue signal: buoyancy surface confusion.

### `buoyant-force-weight-confusion`
- **Description**: Legacy assessment issue signal: buoyant force weight confusion.

### `circular-motion-acceleration-error`
- **Description**: Legacy assessment issue signal: circular motion acceleration error.

### `component-omitted`
- **Description**: Legacy assessment issue signal: component omitted.

### `concept-misunderstood`
- **Description**: Legacy assessment issue signal: concept misunderstood.

### `conservative-force-work-error`
- **Description**: Legacy assessment issue signal: conservative force work error.

### `damping-force-concept-error`
- **Description**: Legacy assessment issue signal: damping force concept error.

### `density-buoyancy-inverted`
- **Description**: Legacy assessment issue signal: density buoyancy inverted.

### `depth-pressure-buoyancy-confusion`
- **Description**: Legacy assessment issue signal: depth pressure buoyancy confusion.

### `depth-pressure-confusion`
- **Description**: Legacy assessment issue signal: depth pressure confusion.

### `derivative-constant-error`
- **Description**: Legacy assessment issue signal: derivative constant error.

### `displacement-distance-confusion`
- **Description**: Legacy assessment issue signal: displacement distance confusion.

### `ductile-brittle-behavior-error`
- **Description**: Legacy assessment issue signal: ductile brittle behavior error.

### `elastic-energy-density-error`
- **Description**: Legacy assessment issue signal: elastic energy density error.

### `elastic-modulus-type-error`
- **Description**: Legacy assessment issue signal: elastic modulus type error.

### `elastic-plastic-deformation-error`
- **Description**: Legacy assessment issue signal: elastic plastic deformation error.

### `elastic-region-interpretation-error`
- **Description**: Legacy assessment issue signal: elastic region interpretation error.

### `escape-velocity-concept-error`
- **Description**: Legacy assessment issue signal: escape velocity concept error.

### `fluid-concept-misunderstood`
- **Description**: Legacy assessment issue signal: fluid concept misunderstood.

### `fluid-continuity-error`
- **Description**: Legacy assessment issue signal: fluid continuity error.

### `fluid-density-confusion`
- **Description**: Legacy assessment issue signal: fluid density confusion.

### `fluid-efflux-speed-error`
- **Description**: Legacy assessment issue signal: fluid efflux speed error.

### `force-pressure-confusion`
- **Description**: Legacy assessment issue signal: force pressure confusion.

### `formula-inverted`
- **Description**: Legacy assessment issue signal: formula inverted.

### `formula-misapplied`
- **Description**: Legacy assessment issue signal: formula misapplied.

### `free-fall-mass-dependence-error`
- **Description**: Legacy assessment issue signal: free fall mass dependence error.

### `gauge-pressure-concept-error`
- **Description**: Legacy assessment issue signal: gauge pressure concept error.

### `geostationary-orbit-error`
- **Description**: Legacy assessment issue signal: geostationary orbit error.

### `gravitational-potential-energy-sign-error`
- **Description**: Legacy assessment issue signal: gravitational potential energy sign error.

### `gravity-field-superposition-error`
- **Description**: Legacy assessment issue signal: gravity field superposition error.

### `hydraulic-work-distance-error`
- **Description**: Legacy assessment issue signal: hydraulic work distance error.

### `hydrostatic-pressure-depth-error`
- **Description**: Legacy assessment issue signal: hydrostatic pressure depth error.

### `integration-error`
- **Description**: Legacy assessment issue signal: integration error.

### `integration-instead-of-derivative`
- **Description**: Legacy assessment issue signal: integration instead of derivative.

### `integration-missed`
- **Description**: Legacy assessment issue signal: integration missed.

### `inverse-square-gravity-error`
- **Description**: Legacy assessment issue signal: inverse square gravity error.

### `keplers-laws-error`
- **Description**: Legacy assessment issue signal: keplers laws error.

### `kinematic-equation-mismatch`
- **Description**: Legacy assessment issue signal: kinematic equation mismatch.

### `kinematic-graph-interpretation-error`
- **Description**: Legacy assessment issue signal: kinematic graph interpretation error.

### `laminar-turbulent-flow-error`
- **Description**: Legacy assessment issue signal: laminar turbulent flow error.

### `longitudinal-wave-compression-error`
- **Description**: Legacy assessment issue signal: longitudinal wave compression error.

### `mass-dependence-confusion`
- **Description**: Legacy assessment issue signal: mass dependence confusion.

### `mass-volume-confusion`
- **Description**: Legacy assessment issue signal: mass volume confusion.

### `material-property-confusion`
- **Description**: Legacy assessment issue signal: material property confusion.

### `moment-of-inertia-rolling-comparison-error`
- **Description**: Legacy assessment issue signal: moment of inertia rolling comparison error.

### `necking-engineering-stress-error`
- **Description**: Legacy assessment issue signal: necking engineering stress error.

### `net-force-buoyancy-confusion`
- **Description**: Legacy assessment issue signal: net force buoyancy confusion.

### `neutral-buoyancy-confusion`
- **Description**: Legacy assessment issue signal: neutral buoyancy confusion.

### `object-density-confusion`
- **Description**: Legacy assessment issue signal: object density confusion.

### `orbital-energy-relationship-error`
- **Description**: Legacy assessment issue signal: orbital energy relationship error.

### `orbital-mass-speed-error`
- **Description**: Legacy assessment issue signal: orbital mass speed error.

### `orbital-weightlessness-error`
- **Description**: Legacy assessment issue signal: orbital weightlessness error.

### `pascals-principle-error`
- **Description**: Legacy assessment issue signal: pascals principle error.

### `poiseuille-law-radius-error`
- **Description**: Legacy assessment issue signal: poiseuille law radius error.

### `poissons-ratio-error`
- **Description**: Legacy assessment issue signal: poissons ratio error.

### `pressure-confusion`
- **Description**: Legacy assessment issue signal: pressure confusion.

### `pressure-density-compressibility-error`
- **Description**: Legacy assessment issue signal: pressure density compressibility error.

### `pressure-force-area-relationship-error`
- **Description**: Legacy assessment issue signal: pressure force area relationship error.

### `principle-misapplied`
- **Description**: Legacy assessment issue signal: principle misapplied.

### `resonance-condition-error`
- **Description**: Legacy assessment issue signal: resonance condition error.

### `rigid-body-translation-error`
- **Description**: Legacy assessment issue signal: rigid body translation error.

### `rotational-direction-sign-error`
- **Description**: Legacy assessment issue signal: rotational direction sign error.

### `rotational-dynamics-rate-error`
- **Description**: Legacy assessment issue signal: rotational dynamics rate error.

### `rotational-energy-angular-momentum-error`
- **Description**: Legacy assessment issue signal: rotational energy angular momentum error.

### `rotational-inertia-acceleration-error`
- **Description**: Legacy assessment issue signal: rotational inertia acceleration error.

### `rotational-kinematics-equation-error`
- **Description**: Legacy assessment issue signal: rotational kinematics equation error.

### `rotational-kinetic-energy-error`
- **Description**: Legacy assessment issue signal: rotational kinetic energy error.

### `rotational-linear-variable-relationship-error`
- **Description**: Legacy assessment issue signal: rotational linear variable relationship error.

### `rotational-power-relationship-error`
- **Description**: Legacy assessment issue signal: rotational power relationship error.

### `rotational-work-energy-error`
- **Description**: Legacy assessment issue signal: rotational work energy error.

### `schwarzschild-radius-concept-error`
- **Description**: Legacy assessment issue signal: schwarzschild radius concept error.

### `shear-modulus-fluid-error`
- **Description**: Legacy assessment issue signal: shear modulus fluid error.

### `shear-stress-direction-error`
- **Description**: Legacy assessment issue signal: shear stress direction error.

### `shell-theorem-error`
- **Description**: Legacy assessment issue signal: shell theorem error.

### `shm-energy-position-error`
- **Description**: Legacy assessment issue signal: shm energy position error.

### `shock-wave-condition-error`
- **Description**: Legacy assessment issue signal: shock wave condition error.

### `sound-speed-medium-error`
- **Description**: Legacy assessment issue signal: sound speed medium error.

### `spring-series-combination-error`
- **Description**: Legacy assessment issue signal: spring series combination error.

### `static-equilibrium-tension-error`
- **Description**: Legacy assessment issue signal: static equilibrium tension error.

### `stress-strain-curve-property-error`
- **Description**: Legacy assessment issue signal: stress strain curve property error.

### `stress-strain-definition-error`
- **Description**: Legacy assessment issue signal: stress strain definition error.

### `terminal-velocity-force-balance-error`
- **Description**: Legacy assessment issue signal: terminal velocity force balance error.

### `tidal-force-concept-error`
- **Description**: Legacy assessment issue signal: tidal force concept error.

### `torque-equilibrium-concept-error`
- **Description**: Legacy assessment issue signal: torque equilibrium concept error.

### `torque-vector-direction-error`
- **Description**: Legacy assessment issue signal: torque vector direction error.

### `total-acceleration-confusion`
- **Description**: Legacy assessment issue signal: total acceleration confusion.

### `toughness-concept-error`
- **Description**: Legacy assessment issue signal: toughness concept error.

### `uniform-circular-motion-error`
- **Description**: Legacy assessment issue signal: uniform circular motion error.

### `vector-addition-error`
- **Description**: Legacy assessment issue signal: vector addition error.

### `vector-addition-geometry-error`
- **Description**: Legacy assessment issue signal: vector addition geometry error.

### `velocity-acceleration-direction-error`
- **Description**: Legacy assessment issue signal: velocity acceleration direction error.

### `velocity-flow-confusion`
- **Description**: Legacy assessment issue signal: velocity flow confusion.

### `venturi-effect-error`
- **Description**: Legacy assessment issue signal: venturi effect error.

### `viscosity-concept-error`
- **Description**: Legacy assessment issue signal: viscosity concept error.

### `volume-confusion`
- **Description**: Legacy assessment issue signal: volume confusion.

### `wave-particle-motion-direction-error`
- **Description**: Legacy assessment issue signal: wave particle motion direction error.

### `wave-speed-medium-dependence-error`
- **Description**: Legacy assessment issue signal: wave speed medium dependence error.

### `wave-superposition-error`
- **Description**: Legacy assessment issue signal: wave superposition error.

### `youngs-modulus-deformation-error`
- **Description**: Legacy assessment issue signal: youngs modulus deformation error.

## Precalculus

### `sign-error`
- **Description**: Incorrectly handled positive or negative signs during algebraic or arithmetic manipulation.
- **Also applies to**: arithmetic, algebra, calculus-1, calculus-2, physics-1

### `exponent-rule-misapplied`
- **Description**: Incorrectly applied the rules of exponents (e.g., adding exponents when bases are multiplied).
- **Also applies to**: algebra, calculus-1, calculus-2

### `logarithm-property-misapplied`
- **Description**: Incorrectly applied the properties of logarithms (e.g., expanding log(a+b) instead of log(ab)).
- **Also applies to**: calculus-1, calculus-2

### `algebraic-simplification-error`
- **Description**: Made an error when distributing terms, factoring polynomials, or simplifying algebraic expressions.
- **Also applies to**: algebra, calculus-1, calculus-2

### `partial-fraction-decomposition-error`
- **Description**: Failed to correctly set up or solve for coefficients during partial fraction decomposition.
- **Also applies to**: calculus-2

### `trigonometric-identity-misapplied`
- **Description**: Incorrectly applied or failed to recognize a necessary trigonometric identity (e.g., double angle, Pythagorean).
- **Also applies to**: trigonometry, calculus-1, calculus-2

### `geometric-area-formula-error`
- **Description**: Used an incorrect formula or made an error calculating the area of a 2D shape.
- **Also applies to**: geometry, calculus-1, calculus-2

### `geometric-volume-formula-error`
- **Description**: Used an incorrect formula or made an error calculating the volume of a 3D solid.
- **Also applies to**: geometry, calculus-1, calculus-2

### `mathematical-translation-error`
- **Description**: Failed to correctly translate a word problem or physical scenario into a mathematical equation.
- **Also applies to**: algebra, calculus-1, physics-1, calculus-2

### `incorrect-model-selection`
- **Description**: Chose the wrong type of mathematical function (e.g., linear vs exponential) to model a given scenario.
- **Also applies to**: algebra, calculus-2

### `domain-range-misidentified`
- **Description**: Incorrectly identified or restricted the domain or range of a function.
- **Also applies to**: algebra, calculus-1, calculus-2

### `function-composition-error`
- **Description**: Made an error when evaluating or constructing a composite function f(g(x)).
- **Also applies to**: algebra, calculus-1, calculus-2

### `inverse-function-error`
- **Description**: Failed to correctly find or evaluate the inverse of a function.
- **Also applies to**: algebra, calculus-2

### `asymptote-identification-failure`
- **Description**: Incorrectly identified vertical, horizontal, or slant asymptotes of a function.
- **Also applies to**: algebra, calculus-1

### `double-angle-identity-misapplied`
- **Description**: Incorrectly applied or failed to recognize a double-angle trigonometric identity.
- **Also applies to**: trigonometry, calculus-1, calculus-2

### `half-angle-identity-misapplied`
- **Description**: Incorrectly applied or failed to recognize a half-angle trigonometric identity.
- **Also applies to**: trigonometry, calculus-1, calculus-2

### `pythagorean-identity-misapplied`
- **Description**: Incorrectly applied a Pythagorean trigonometric identity (e.g., sin^2 + cos^2 = 1).
- **Also applies to**: trigonometry, calculus-1, calculus-2

### `sum-difference-identity-misapplied`
- **Description**: Incorrectly applied the sum or difference identity for sine, cosine, or tangent.
- **Also applies to**: trigonometry, calculus-1, calculus-2

### `conic-section-misidentified`
- **Description**: Incorrectly identified a conic section (circle, ellipse, parabola, hyperbola) from its equation.
- **Also applies to**: calculus-2

### `conic-properties-calculation-error`
- **Description**: Failed to correctly calculate the vertex, focus, directrix, or asymptotes of a conic section.

### `polar-rectangular-conversion-error`
- **Description**: Made an error converting between polar (r, theta) and rectangular (x, y) coordinates.
- **Also applies to**: calculus-2

### `function-analysis-error`
- **Description**: Failed to correctly analyze the overall behavior, roots, extrema, or end behavior of a function.
- **Also applies to**: algebra, calculus-1, calculus-2

### `law-of-sines-misapplied`
- **Description**: Incorrectly applied the Law of Sines, or failed to check for the ambiguous case (SSA).
- **Also applies to**: geometry, trigonometry

### `law-of-cosines-misapplied`
- **Description**: Incorrectly applied the Law of Cosines when solving an oblique triangle.
- **Also applies to**: geometry, trigonometry

### `circular-properties-error`
- **Description**: Failed to apply or correctly calculate properties of a circle such as arc length, sector area, or inscribed angles.
- **Also applies to**: geometry, trigonometry

### `expression-equation-recognition-error`
- **Description**: Misidentified the structural form of an expression or equation, leading to the wrong solution strategy.
- **Also applies to**: algebra, calculus-1, calculus-2, physics-1

### `proportionality-misidentified`
- **Description**: Failed to correctly identify or set up direct, inverse, or joint proportionality relationships.
- **Also applies to**: algebra, geometry, physics-1

## Pwsh

### `syntax-error`
- **Description**: Made a foundational syntax mistake (e.g., missing semicolon, unmatched brackets) that prevents compilation or execution.
- **Also applies to**: computer-science, scripting, python, csharp, c++, typescript

## Python

### `syntax-error`
- **Description**: Made a foundational syntax mistake (e.g., missing semicolon, unmatched brackets) that prevents compilation or execution.
- **Also applies to**: computer-science, scripting, csharp, c++, typescript, pwsh

### `class-inheritance-error`
- **Description**: Misapplied object-oriented inheritance principles, such as incorrect overriding, shadowing, or interface implementation.
- **Also applies to**: computer-science, csharp, c++, typescript

### `import-dependency-error`
- **Description**: Failed to correctly import a required library, module, or namespace.
- **Also applies to**: computer-science, scripting, typescript, csharp, c++

## Scripting

### `syntax-error`
- **Description**: Made a foundational syntax mistake (e.g., missing semicolon, unmatched brackets) that prevents compilation or execution.
- **Also applies to**: computer-science, python, csharp, c++, typescript, pwsh

### `variable-declaration-error`
- **Description**: Incorrectly declared or defined a variable, such as omitting a type or using an invalid identifier.
- **Also applies to**: computer-science

### `uninitialized-variable-error`
- **Description**: Attempted to use or dereference a variable or object before it was properly initialized or assigned a value (e.g., Null Reference).
- **Also applies to**: computer-science

### `scope-resolution-error`
- **Description**: Attempted to access a variable or function outside of its valid lexical or dynamic scope.
- **Also applies to**: computer-science

### `function-declaration-error`
- **Description**: Incorrectly defined a function signature, return type, or parameter list.
- **Also applies to**: computer-science

### `loop-logic-error`
- **Description**: Implemented faulty loop logic, such as an incorrect condition or increment, causing unexpected iteration behavior.
- **Also applies to**: computer-science

### `infinite-loop-error`
- **Description**: Created a loop with a condition that can never evaluate to false, causing execution to hang.
- **Also applies to**: computer-science

### `off-by-one-error`
- **Description**: Iterated one time too many or too few, often resulting in an out-of-bounds array access.
- **Also applies to**: computer-science

### `overcomplication-error`
- **Description**: Implemented a convoluted or excessively complex solution when a much simpler, standard approach exists.
- **Also applies to**: computer-science

### `simplification-error`
- **Description**: Oversimplified a problem, ignoring crucial constraints or edge cases required for correctness.
- **Also applies to**: computer-science

### `edge-case-handling-failure`
- **Description**: Failed to account for edge cases such as empty collections, negative numbers, or boundary limits.
- **Also applies to**: computer-science, dsa

### `import-dependency-error`
- **Description**: Failed to correctly import a required library, module, or namespace.
- **Also applies to**: computer-science, python, typescript, csharp, c++

### `function-modeling-from-scenario-error`
- **Description**: Failed to correctly translate a real-world scenario or specification into a programmatic function or class model.
- **Also applies to**: computer-science

## Trigonometry

### `trigonometric-identity-misapplied`
- **Description**: Incorrectly applied or failed to recognize a necessary trigonometric identity (e.g., double angle, Pythagorean).
- **Also applies to**: precalculus, calculus-1, calculus-2

### `unit-circle-evaluation-error`
- **Description**: Evaluated a trigonometric function at a standard angle incorrectly.

### `pythagorean-theorem-misapplied`
- **Description**: Failed to correctly apply the Pythagorean theorem for right triangles.
- **Also applies to**: geometry, physics-1, calculus-2

### `angle-relationship-misidentified`
- **Description**: Misidentified supplementary, complementary, or other geometric angle relationships.
- **Also applies to**: geometry

### `double-angle-identity-misapplied`
- **Description**: Incorrectly applied or failed to recognize a double-angle trigonometric identity.
- **Also applies to**: precalculus, calculus-1, calculus-2

### `half-angle-identity-misapplied`
- **Description**: Incorrectly applied or failed to recognize a half-angle trigonometric identity.
- **Also applies to**: precalculus, calculus-1, calculus-2

### `pythagorean-identity-misapplied`
- **Description**: Incorrectly applied a Pythagorean trigonometric identity (e.g., sin^2 + cos^2 = 1).
- **Also applies to**: precalculus, calculus-1, calculus-2

### `sum-difference-identity-misapplied`
- **Description**: Incorrectly applied the sum or difference identity for sine, cosine, or tangent.
- **Also applies to**: precalculus, calculus-1, calculus-2

### `law-of-sines-misapplied`
- **Description**: Incorrectly applied the Law of Sines, or failed to check for the ambiguous case (SSA).
- **Also applies to**: geometry, precalculus

### `law-of-cosines-misapplied`
- **Description**: Incorrectly applied the Law of Cosines when solving an oblique triangle.
- **Also applies to**: geometry, precalculus

### `circular-properties-error`
- **Description**: Failed to apply or correctly calculate properties of a circle such as arc length, sector area, or inscribed angles.
- **Also applies to**: geometry, precalculus

### `triangle-properties-error`
- **Description**: Failed to apply basic triangle properties such as the sum of interior angles or side length inequalities.
- **Also applies to**: geometry

### `transversal-angle-theorem-error`
- **Description**: Failed to correctly identify or relate alternate interior, alternate exterior, or corresponding angles formed by a transversal intersecting parallel lines.
- **Also applies to**: geometry

### `exterior-angle-theorem-misapplied`
- **Description**: Failed to correctly apply the exterior angle theorem for triangles (the exterior angle equals the sum of the two opposite interior angles).
- **Also applies to**: geometry

### `complementary-supplementary-angle-error`
- **Description**: Failed to recognize or correctly calculate that complementary angles sum to 90 degrees, or supplementary angles sum to 180 degrees.
- **Also applies to**: geometry

## Typescript

### `syntax-error`
- **Description**: Made a foundational syntax mistake (e.g., missing semicolon, unmatched brackets) that prevents compilation or execution.
- **Also applies to**: computer-science, scripting, python, csharp, c++, pwsh

### `class-inheritance-error`
- **Description**: Misapplied object-oriented inheritance principles, such as incorrect overriding, shadowing, or interface implementation.
- **Also applies to**: computer-science, csharp, c++, python

### `type-constraint-violation`
- **Description**: Violated strict typing rules, such as attempting to assign an incompatible type without an explicit cast.
- **Also applies to**: computer-science, csharp, c++

### `import-dependency-error`
- **Description**: Failed to correctly import a required library, module, or namespace.
- **Also applies to**: computer-science, scripting, python, csharp, c++

