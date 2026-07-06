# Linear Algebra Curriculum Reference

This document outlines the assessment structure, topics, and question archetypes for the Linear Algebra curriculum.

## Curriculum Order

1. **Vectors and Matrix Basics**: vectors, linear combinations, matrix operations, matrix-vector products
2. **Systems and RREF**: augmented matrices, row operations, pivots, free variables, solution sets
3. **Span, Independence, Basis, Dimension**: span, linear dependence, bases, coordinates, rank-nullity foundations
4. **Linear Transformations**: transformations, standard matrices, kernel, image, one-to-one, onto
5. **Determinants**: determinant meaning, computation, invertibility, area/volume scaling
6. **Vector Spaces and Subspaces**: abstract vector spaces, subspace tests, column/null spaces
7. **Orthogonality and Projections**: dot product, orthogonal complements, projections, Gram-Schmidt
8. **Least Squares**: normal equations, projection interpretation, fitting
9. **Eigenvalues and Eigenvectors**: characteristic equation, eigenspaces, diagonalization readiness
10. **Diagonalization and Applications**: diagonalization, powers of matrices, dynamical systems
11. **Inner Product Spaces**: generalized inner products, norms, orthogonality
12. **Comprehensive Review**: mixed tests that force choosing the correct tool

---

## Topic 1: Vectors and Matrix Basics

**Subtopic**: `linear-algebra-vectors`
**Skill Tags**: `vector-addition`, `scalar-multiplication`, `linear-combinations`, `matrix-addition`, `matrix-multiplication`, `matrix-vector-product`, `matrix-transpose`

### Definitions & Notation
- **Vector ($\mathbb{R}^n$)**: An ordered list of $n$ numbers, represented as a column matrix.
- **Linear Combination**: $c_1\vec{v}_1 + c_2\vec{v}_2 + \dots + c_k\vec{v}_k$
- **Matrix-Vector Product ($A\vec{x}$)**: Represents a linear combination of the columns of $A$ using weights from $\vec{x}$.
- **Matrix Multiplication ($AB$)**: $C_{ij} = (\text{row } i \text{ of } A) \cdot (\text{column } j \text{ of } B)$. Dimensions must match: $(m \times n) \times (n \times p) \to m \times p$.

### Common Traps / Mistakes
- **Dimension Mismatches**: Attempting to add matrices of different dimensions or multiply matrices where inner dimensions don't match.
- **Commutativity**: Assuming $AB = BA$. Matrix multiplication is generally non-commutative.
- **Matrix-Vector Product Orientation**: Trying to compute $A\vec{x}$ as row combinations rather than column combinations (or transposing incorrectly).

### Easy Problem Archetypes (Easy Quizzes)
- **Vector arithmetic**: Given two vectors $\vec{u}$ and $\vec{v}$, compute $2\vec{u} - 3\vec{v}$.
- **Matrix multiplication check**: Can you multiply a $3 \times 4$ and a $4 \times 5$ matrix? What is the resulting dimension?
- **Basic matrix arithmetic**: Compute $A + 2B$.
- **Direct matrix-vector product**: Compute $A\vec{x}$ for a small $2 \times 2$ or $3 \times 3$ matrix.

### Hard Problem Archetypes (Hard Quizzes)
- **Unknown entries**: Find $x, y$ such that $A + B = C$ or $AB = C$ where some entries are variables.
- **Properties of matrix algebra**: Simplify $(A+B)^2$ noting that it is $A^2 + AB + BA + B^2$ and not $A^2 + 2AB + B^2$.
- **Conceptual logic**: If $A\vec{x} = \vec{0}$ for some non-zero $\vec{x}$, what does that say about the columns of $A$? (Introduction to linear dependence conceptually).
- **Transpose properties**: Simplify $(AB)^T$ to $B^TA^T$ and evaluate for specific matrices.

### Worked-Example Patterns
- **Matrix-Vector Product as Linear Combinations**: Show the direct dot-product method vs. the linear-combination-of-columns method to enforce the conceptual understanding of $A\vec{x}$.
- **Matrix Multiplication Step-by-Step**: Trace the row-by-column dot products carefully. Explain why the dimensions align.

### Recall Targets (Recall Drills)
- Dimensions of matrix multiplication result.
- Formula for the transpose of a product: $(AB)^T = B^TA^T$.
- Definition of a linear combination.
- The equivalent form of $A\vec{x}$ as $x_1\vec{a}_1 + \dots + x_n\vec{a}_n$.
