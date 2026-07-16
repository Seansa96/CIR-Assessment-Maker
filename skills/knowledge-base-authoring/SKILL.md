---
name: Knowledge Base Authoring
description: Guidelines and requirements for generating comprehensive knowledge base reference files and massive question banks for assessment generation.
---

# Knowledge Base Authoring Guidelines

When tasked with generating a knowledge base or reference material for a new area or topic, you are acting as an author of a comprehensive "local textbook." These reference materials serve as the foundational source of truth for dynamically drafting learning assessments, quizzes, and tests.

## 1. Directory Structure

All knowledge base materials must be organized under `docs/assessment-reference/<knowledge-base-name>/`.
For example, a Calculus 2 knowledge base should live in `docs/assessment-reference/calc-2-knowledge-base/`.

## 2. Reference Files (The "Local Textbook")

Each chapter or core area must have a dedicated markdown reference file (e.g., `calc2-ch9-differential-equations.md`). These files must:

*   **Be Comprehensive**: They are not mere summaries. They must provide deep conceptual explanations, formal definitions, proofs of key formulas (e.g., geometric formulas for volume), and geometric/analytical exploration.
*   **Identify Media Needs**: If a concept requires visual aids (such as a slope field or geometric visualization), include a clear placeholder indicating that media generation is required (e.g., `"Placeholder: This explanation requires generation of media showing..."`).
*   **Cover Advanced Material**: Incorporate both foundational concepts (e.g., Stewart's Calculus) and highly advanced analysis (e.g., Advanced Calculus 100+1 problems).

## 3. Question Bank Files

For each reference chapter, you must also generate a massive question bank in YAML format (e.g., `calc2-ch9-differential-equations-question-bank.yaml`).

*   **Volume Requirement**: Each chapter's question bank must contain **at least 150 questions**.
*   **Difficulty Distribution**:
    *   **100 Questions**: Foundational and intermediate level, inspired by standard textbooks (e.g., Stewart).
    *   **50 Questions**: Advanced, "Olympiad" level, inspired by advanced texts (e.g., Advanced Calculus 100+1 problems).
*   **Structure**: The question bank YAML should contain an `items` array where each item provides an `id`, `concept`, `difficulty`, `source`, `prompt`, `answer`, and `solutionOutline`.

## 4. Assessment Generation from Question Banks

Once the question bank is populated, do not hand-write 90+ individual assessment YAMLs. Instead:
1. Write a Python script to parse the massive question bank.
2. Dynamically sample the questions (e.g., 15 for a quiz).
3. Generate the standard assessment YAML files (Easy, Hard, Olympiad for Quizzes and Tests) using the script. 
4. **Important**: Always use strict YAML block scalars (`|`) or single quotes when outputting LaTeX strings to avoid YAML syntax/escape character errors in the generated files.
