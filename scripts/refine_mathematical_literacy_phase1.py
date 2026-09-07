"""Materialize Phase 1 Mathematical Literacy provenance and metadata gates.

The script deliberately derives one assessment-scoped blueprint from each published
answer-bearing item.  It does not create Phase 2 activities or alter stable IDs.
"""

from __future__ import annotations

from pathlib import Path
import json
import re
import shutil
import yaml


ROOT = Path(__file__).resolve().parents[1]
ASSESSMENTS = ROOT / 'data' / 'assessments'
RETIRED = ROOT / 'data' / 'retired-assessments'
BLUEPRINTS = ROOT / 'docs' / 'assessment-reference' / 'question-blueprints'
PACKETS_PATH = ROOT / 'docs' / 'assessment-reference' / 'packets' / 'mathematical-literacy-v2-packets.json'
STATUS_PATH = ROOT / 'docs' / 'assessment-reference' / 'content-manifests' / 'mathematical-literacy-s2c-migration-status.yaml'

TOPIC_PRINCIPLES = {
    'mathematical-notation-and-structure': (
        'Interpret the notation by preserving its declared domain, object type, grouping, and relation.',
        'ml-notation'),
    'mathematical-statements-and-logic': (
        'Classify a declarative claim by its truth conditions and preserve the hypothesis-to-conclusion direction.',
        'ml-logic'),
    'quantifiers-negation-and-mathematical-translation': (
        'Preserve quantifier scope and apply the matching negation or conditional translation rule.',
        'ml-quantifiers'),
    'definitions-theorems-and-examples': (
        'Use the exact stated definition and distinguish a definition, theorem, example, and counterexample by role.',
        'ml-structures'),
    'theorem-reading-and-application': (
        'Check every hypothesis before applying a theorem and state only its warranted conclusion.',
        'ml-theorem-reading'),
    'reading-proofs-and-exposition': (
        'Trace each proof claim to its definition, hypothesis, prior result, or justified inference.',
        'ml-proof-reading'),
    'proof-forms-and-argument-diagnosis': (
        'Diagnose the proof form by preserving conditional direction and distinguishing a contrapositive from a converse.',
        'ml-proof-diagnosis'),
    'reading-mathematical-exposition': (
        'Identify how definitions, hypotheses, claims, and proof steps connect in a mathematical exposition.',
        'ml-exposition'),
    'mathematical-literacy-cumulative-review': (
        'Select the relevant notation, logical form, or proof justification and check that its conditions are satisfied.',
        'ml-review'),
}
ISSUE_SIGNAL_RENAMES = {
    'structuralRecognition-error': 'mathematical-structure-recognition-error',
    'logical-evaluation-error': 'logical-evaluation-error',
    'conceptual-misunderstanding': 'mathematical-role-confusion',
}


class AssessmentDumper(yaml.SafeDumper):
    pass


def represent_string(dumper, value):
    if '\n' in value:
        return dumper.represent_scalar('tag:yaml.org,2002:str', value, style='|')
    if '\\' in value:
        return dumper.represent_scalar('tag:yaml.org,2002:str', value, style="'")
    return dumper.represent_scalar('tag:yaml.org,2002:str', value)


AssessmentDumper.add_representer(str, represent_string)


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def write_yaml(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.dump(value, Dumper=AssessmentDumper, sort_keys=False, allow_unicode=True, width=110),
        encoding='utf-8',
    )


def slug(value: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def answer_text(question: dict) -> str:
    answer = question.get('answer') or {}
    if answer.get('choiceId'):
        for choice in question.get('choices', []):
            if choice.get('id') == answer['choiceId']:
                return str(choice.get('text', '')).strip()
    for key in ('expected', 'expectedLatex', 'value'):
        if answer.get(key) not in (None, ''):
            return str(answer[key]).strip()
    return 'the keyed response'


def prompt_summary(question: dict) -> str:
    text = ' '.join(str(question.get('prompt') or question.get('instruction') or '').split())
    return text[:180] or 'the stated mathematical prompt'


def ensure_explanation(question: dict, principle: str):
    explanation = str(question.get('explanation') or '').strip()
    if 'Solution:' not in explanation or 'Why it works:' not in explanation:
        answer = answer_text(question)
        explanation = (
            f'Solution: The keyed response is {answer}.\n'
            f'Why it works: {principle}'
        )
    if question.get('type') == 'multipleChoice' and 'Why the other choices fail:' not in explanation:
        explanation += (
            '\nWhy the other choices fail: Each alternative changes the stated relation, condition, '
            'or logical role instead of preserving the prompt’s mathematical structure.'
        )
    question['explanation'] = explanation


def normalize_issue_signals(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == 'issueSignals' and isinstance(child, list):
                normalized = []
                for signal in child:
                    if isinstance(signal, str):
                        normalized.append(ISSUE_SIGNAL_RENAMES.get(signal, signal))
                    elif isinstance(signal, dict):
                        signal = dict(signal)
                        if isinstance(signal.get('id'), str):
                            signal['id'] = ISSUE_SIGNAL_RENAMES.get(signal['id'], signal['id'])
                        normalized.append(signal)
                    else:
                        normalized.append(signal)
                value[key] = normalized
            else:
                normalize_issue_signals(child)
    elif isinstance(value, list):
        for child in value:
            normalize_issue_signals(child)


def collect_items(data: dict):
    for index, question in enumerate(data.get('questions', [])):
        yield question.setdefault('id', f'q{index + 1:03d}'), question
    for example in data.get('workedExamples', []):
        for index, step in enumerate(example.get('steps', [])):
            question = step.get('question', step)
            item_id = question.get('id') or step.get('id') or f'step-{index + 1}'
            question.setdefault('id', item_id)
            yield item_id, question
    for section in (data.get('lesson') or {}).get('sections', []):
        question = section.get('check')
        if question:
            item_id = question.get('id') or f"{section.get('id', 'section')}-check"
            question.setdefault('id', item_id)
            yield item_id, question
    for section in (data.get('glossary') or {}).get('sections', []):
        for entry in section.get('entries', []):
            for index, drill in enumerate(entry.get('drills', [])):
                item_id = drill.get('id') or f"{entry.get('id', 'entry')}-drill-{index + 1}"
                drill.setdefault('id', item_id)
                yield item_id, drill
    for index, item in enumerate(data.get('items', [])):
        item_id = item.get('id') or f'item-{index + 1}'
        item.setdefault('id', item_id)
        yield item_id, item


def merge_foundation_duplicates(data_by_id: dict):
    notation = data_by_id['mathematical-literacy-notation-concept-lesson']
    notation_sections = notation['lesson']['sections']
    additions = [
        'Before interpreting a line, classify whether it names a set, a function, a relation, or an ordered structure.',
        'Underline the declaration and its restriction before translating the line into words.',
        'Translate the expression aloud before deciding whether a candidate satisfies it, so its domain and condition remain visible.',
    ]
    for section, addition in zip(notation_sections[:3], additions):
        section['content'] = section['content'].replace(f'\n\n{addition}', '')
        section['content'] += f'\n\n{addition}'

    logic = data_by_id['mathematical-literacy-logic-concept-lesson']
    logic_sections = logic['lesson']['sections']
    additions = [
        'First identify whether the line is a complete claim, an open sentence, or a request; only a complete claim has a truth value.',
        'Mark the hypothesis and conclusion before evaluating the conditional or considering its converse.',
        'Translate a symbolic statement into a full sentence and check that each domain restriction survives.',
    ]
    for section, addition in zip(logic_sections[:3], additions):
        section['content'] = section['content'].replace(f'\n\n{addition}', '')
        section['content'] += f'\n\n{addition}'

    notation_recall = data_by_id['mathematical-literacy-notation-recall']
    notation_recall['items'] = [item for item in notation_recall['items'] if item.get('id') != 'r005']
    notation_recall['items'].append({
        'id': 'r005', 'type': 'typed',
        'prompt': 'Why say a set-builder expression aloud before testing a candidate?',
        'answer': {'expected': 'to preserve its domain and condition', 'aliases': ['to keep its domain and condition', 'to check the domain and condition']},
        'explanation': 'Solution: Say it aloud to preserve its domain and condition.\nWhy it works: A set-builder expression combines an output rule with restrictions on the permitted parameter values.',
    })
    logic_recall = data_by_id['mathematical-literacy-logic-recall']
    logic_recall['items'] = [item for item in logic_recall['items'] if item.get('id') not in ('r005', 'r006')]
    logic_recall['items'].extend([
        {
            'id': 'r005', 'type': 'typed',
            'prompt': 'Before evaluating “if P, then Q,” what two parts should you identify?',
            'answer': {'expected': 'the hypothesis and conclusion', 'aliases': ['hypothesis and conclusion', 'P and Q as hypothesis and conclusion']},
            'explanation': 'Solution: Identify the hypothesis and conclusion.\nWhy it works: A conditional has a directed form: P is the hypothesis and Q is the conclusion asserted when P holds.',
        },
        {
            'id': 'r006', 'type': 'typed',
            'prompt': 'Why translate a symbolic conditional into a full sentence?',
            'answer': {'expected': 'to check its direction and conditions', 'aliases': ['to preserve its direction and conditions', 'to check the hypothesis and conclusion']},
            'explanation': 'Solution: Translate it to check its direction and conditions.\nWhy it works: Reading the hypothesis, conclusion, and domain aloud prevents an unjustified reversal of the implication.',
        },
    ])


def self_check_step(step_id, title, prompt, key_point, reason):
    return {
        'id': step_id, 'title': title, 'type': 'freeResponse', 'prompt': prompt,
        'instruction': 'State the specific mathematical reason used at this checkpoint.',
        'answer': {'gradingMode': 'selfCheck', 'keyPoints': [key_point]},
        'explanation': f'Solution: {key_point}\nWhy it works: {reason}',
    }


def replace_worked_example_b(data_by_id: dict):
    examples = {
        'mathematical-literacy-notation-worked-example-b': (
            'Read grouped Cartesian-product notation',
            'A source writes $\mathbb R\\times(\mathbb N\\times\mathbb Z)$. Explain why an element has nested-pair form rather than three ungrouped coordinates.',
            [
                self_check_step('step-1', 'Read the outer product', 'What must the first coordinate belong to?', 'The first coordinate belongs to $\mathbb R$.', 'The outer product places a real number in its first factor.'),
                self_check_step('step-2', 'Keep the inner grouping', 'What form must the second component have?', 'The second component is an ordered pair $(n,z)$ with $n\in\mathbb N$ and $z\in\mathbb Z$.', 'Parentheses preserve the inner Cartesian product as one component.'),
                self_check_step('step-3', 'State the full element shape', 'Write the complete shape of one element.', 'An element has the form $(r,(n,z))$.', 'The grouped product is not the same structure as an unparenthesized ordered triple.'),
            ],
        ),
        'mathematical-literacy-logic-worked-example-b': (
            'Separate an open sentence from a statement',
            'Compare $x+1>0$ with “For every integer $x$, $x+1>0$.” Decide which has a fixed truth value and why.',
            [
                self_check_step('step-1', 'Locate the free variable', 'Which expression leaves x unbound?', '$x+1>0$ leaves x unbound.', 'Without a stated value or quantifier, its truth changes with x.'),
                self_check_step('step-2', 'Check the quantified claim', 'Does the quantified sentence have a truth value?', 'Yes; the quantified sentence has a definite truth value, even though it is false.', 'A fully quantified sentence is a statement because its domain and claim are fixed.'),
                self_check_step('step-3', 'Give the classification', 'Classify the two expressions.', 'The first is an open sentence; the second is a false statement.', 'Truth status and open-variable status are different reading questions.'),
            ],
        ),
        'mathematical-literacy-definitions-worked-example-b': (
            'Use the definition of odd in a sum',
            'Read the claim: If integers a and b are odd, then $a+b$ is even. Identify the definition-driven bridge and the final form.',
            [
                self_check_step('step-1', 'Unpack both hypotheses', 'How may odd integers a and b be written?', 'Write $a=2m+1$ and $b=2n+1$ for integers m and n.', 'The definition of odd supplies an integer parameter for each odd input.'),
                self_check_step('step-2', 'Combine the expressions', 'What form does $a+b$ take after substitution?', '$a+b=2(m+n+1)$.', 'Collecting the two even parts and two ones factors out 2.'),
                self_check_step('step-3', 'Match the definition', 'Why is the sum even?', '$m+n+1$ is an integer, so $a+b$ is two times an integer.', 'This exactly matches the definition of an even integer.'),
            ],
        ),
        'mathematical-literacy-quantifiers-negation-and-mathematical-translation-worked-example-b': (
            'Negate a universal claim',
            'Negate the claim “Every integer is even” without changing its domain.',
            [
                self_check_step('step-1', 'Name the outer quantifier', 'What quantifier begins the original claim?', 'The original claim begins with “for every.”', '“Every integer” is a universal quantifier over the integers.'),
                self_check_step('step-2', 'Switch the quantifier', 'What quantifier begins its negation?', 'The negation begins with “there exists.”', 'Negating a universal claim produces an existential counterexample claim.'),
                self_check_step('step-3', 'Negate the property', 'State the complete negation.', 'There exists an integer that is not even.', 'The domain remains integers while the property is negated.'),
            ],
        ),
        'mathematical-literacy-theorem-reading-and-application-worked-example-b': (
            'Check a theorem before using it',
            'A theorem says “If a number is divisible by 6, then it is divisible by 3.” Read a proposed use of the theorem for 18.',
            [
                self_check_step('step-1', 'State the hypothesis', 'What condition must be checked before applying the theorem?', 'Check that the number is divisible by 6.', 'The hypothesis is the condition that licenses the theorem’s conclusion.'),
                self_check_step('step-2', 'Verify the condition', 'How does 18 meet that condition?', '$18=6\cdot3$, so 18 is divisible by 6.', 'An integer factor verifies divisibility.'),
                self_check_step('step-3', 'State only the warranted conclusion', 'What conclusion is now justified?', '18 is divisible by 3.', 'The theorem supplies this conclusion after its hypothesis has been checked.'),
            ],
        ),
        'mathematical-literacy-proofs-worked-example-b': (
            'Trace a proof by contrapositive',
            'A proof of “If $n^2$ is even, then n is even” begins: “Assume n is odd.” Identify the proof strategy and the required conclusion of that branch.',
            [
                self_check_step('step-1', 'Identify the assumed opposite', 'What is the negation of the desired conclusion?', 'The opposite conclusion is that n is odd.', 'A contrapositive proof begins by assuming the conclusion fails.'),
                self_check_step('step-2', 'Name the target of the branch', 'What must this branch show about $n^2$?', 'It must show that $n^2$ is odd.', 'This establishes “if n is not even, then $n^2$ is not even.”'),
                self_check_step('step-3', 'Connect to the original claim', 'Why does that finish the proof?', 'It proves the contrapositive, so the original conditional follows.', 'A conditional and its contrapositive have the same truth value.'),
            ],
        ),
        'mathematical-literacy-proof-forms-and-argument-diagnosis-worked-example-b': (
            'Diagnose a converse error',
            'A student reads “If a number is divisible by 4, then it is even” and concludes “Every even number is divisible by 4.” Diagnose the argument.',
            [
                self_check_step('step-1', 'Mark the original direction', 'What is the original hypothesis and conclusion?', 'Divisible by 4 is the hypothesis; even is the conclusion.', 'A conditional has a directed hypothesis-to-conclusion structure.'),
                self_check_step('step-2', 'Name the changed statement', 'What statement did the student make instead?', 'The student stated the converse: if a number is even, then it is divisible by 4.', 'Swapping the hypothesis and conclusion forms the converse.'),
                self_check_step('step-3', 'Test the converse', 'Give a counterexample to the converse.', '2 is even but is not divisible by 4.', 'One allowed counterexample shows the reversed implication is false.'),
            ],
        ),
        'mathematical-literacy-reading-mathematical-exposition-worked-example-b': (
            'Map a definition-to-theorem passage',
            'A passage defines a property, assumes an object has that property, and then invokes a theorem. Identify the distinct roles before accepting the conclusion.',
            [
                self_check_step('step-1', 'Locate the definition', 'What role does the first sentence play?', 'It fixes the meaning of the property being used.', 'Definitions establish terminology rather than proving a new claim.'),
                self_check_step('step-2', 'Locate the hypothesis', 'What role does the assumption play?', 'It supplies the condition required for the later theorem use.', 'A hypothesis is information available within the argument.'),
                self_check_step('step-3', 'Locate the theorem conclusion', 'What must be checked before accepting the final sentence?', 'Check that the theorem’s stated hypotheses match the defined property and assumption.', 'A conclusion is licensed only when the cited theorem applies to the established conditions.'),
            ],
        ),
        'mathematical-literacy-review-worked-example-b': (
            'Review a quantified conditional',
            'Read: “For every integer n, if n is divisible by 4, then n is even.” Separate its scope, conditional direction, and a valid check.',
            [
                self_check_step('step-1', 'Read the scope', 'Which objects does the statement quantify over?', 'It quantifies over every integer n.', 'The universal quantifier fixes the domain of the claim.'),
                self_check_step('step-2', 'Read the direction', 'What condition implies what conclusion?', 'Divisibility by 4 implies evenness.', 'The hypothesis is divisibility by 4 and the conclusion is evenness.'),
                self_check_step('step-3', 'Verify the structural reason', 'Why does divisibility by 4 imply evenness?', 'If $n=4k$, then $n=2(2k)$, so n is two times an integer.', 'Rewriting the hypothesis in the definition of even gives the warranted conclusion.'),
            ],
        ),
    }
    for assessment_id, (title, problem, steps) in examples.items():
        data = data_by_id.get(assessment_id)
        if data:
            data['workedExamples'] = [{'id': f'{assessment_id}-example', 'title': title, 'problem': problem, 'steps': steps}]


def multiple_choice(question_id, prompt, choices, answer_id, signal, principle):
    return {
        'id': question_id, 'type': 'multipleChoice', 'prompt': prompt,
        'choices': [
            {'id': choice_id, 'text': text, **({} if choice_id == answer_id else {'issueSignals': [{'id': signal}]})}
            for choice_id, text in choices
        ],
        'answer': {'choiceId': answer_id}, 'issueSignals': [{'id': signal}],
        'difficultyDimensions': ['errorDiagnosis', 'representationTransfer', 'proofJustification'],
        'difficultyEvidence': 'Requires preserving the stated logical direction and evaluating a concrete mathematical-reading claim.',
        'explanation': f'Solution: {dict(choices)[answer_id]}\nWhy it works: {principle}\nWhy the other choices fail: Each alternative changes the claim’s direction, role, or required evidence.',
    }


def replace_duplicate_mastery_checks(data_by_id: dict):
    diagnosis = data_by_id.get('mathematical-literacy-proof-forms-and-argument-diagnosis-mastery-check')
    if diagnosis:
        diagnosis['questions'] = [
            multiple_choice('q001', 'Which statement is the contrapositive of “If n is even, then $n^2$ is even”?', [
                ('a', 'If $n^2$ is not even, then n is not even.'), ('b', 'If $n^2$ is even, then n is even.'), ('c', 'If n is not even, then $n^2$ is even.'), ('d', 'If n is even, then $n^2$ is not even.'),
            ], 'a', 'reversed-implication', 'A contrapositive negates and reverses the hypothesis and conclusion without changing the conditional’s truth value.'),
            multiple_choice('q002', 'A proof of “If P, then Q” assumes not Q and derives not P. What proof form is being used?', [
                ('a', 'Contrapositive proof.'), ('b', 'Converse proof.'), ('c', 'Proof by one example.'), ('d', 'Definition only.'),
            ], 'a', 'proofStructure-error', 'Showing not Q implies not P proves the contrapositive, which is logically equivalent to the original conditional.'),
            multiple_choice('q003', 'Why does the even number 2 refute “Every even integer is divisible by 4”?', [
                ('a', 'It satisfies the hypothesis “even” but fails the claimed conclusion “divisible by 4.”'), ('b', 'It is not an integer.'), ('c', 'It proves every even integer is divisible by 4.'), ('d', 'It reverses the definition of even.'),
            ], 'a', 'example-as-proof', 'A counterexample is one permitted case that makes a universal conditional claim fail.'),
            multiple_choice('q004', 'A line writes “n=2k” after assuming n is even. What licenses that line?', [
                ('a', 'The definition of even supplies an integer k with n=2k.'), ('b', 'Every integer has the form 2k.'), ('c', 'The converse of the even-number definition.'), ('d', 'A numerical example alone.'),
            ], 'a', 'divisor-definition-misread', 'A definition licenses replacing a named property with its stated structural form.'),
        ]


# Phase 2 turns the provenance-complete definitions into the required learner-facing
# sequence.  These are deliberately short retrieval prompts: none asks the learner
# to solve a new multi-step problem.
RECALL_FACTS = {
    'mathematical-notation-and-structure': [
        ('What relation symbol says that every element of the left set is in the right set?', 'subseteq', 'the subset relation'),
        ('In $f:A\\to B$, what does A name?', 'the domain', 'domain'),
        ('What punctuation preserves a nested Cartesian-product grouping?', 'parentheses', 'parentheses'),
        ('Which reading matches $x\\in\\mathbb Z$?', 'x is an integer', 'x is an integer'),
        ('Recognition: Which expression is set-builder notation?', '$\\{x\\in\\mathbb Z:x>0\\}$', 'set-builder notation'),
        ('Recognition: Which claim keeps the braces in $\\{2\\}\\in\\{1,\\{2\\}\\}$?', '$\\{2\\}$ is an element of the set', 'the braced object is an element'),
    ],
    'mathematical-statements-and-logic': [
        ('What two directed parts make up “if P, then Q”?', 'the hypothesis and conclusion', 'hypothesis and conclusion'),
        ('What is a sentence with an unbound variable called?', 'an open sentence', 'open sentence'),
        ('What does a quantifier do to a variable?', 'binds the variable', 'binds the variable'),
        ('What truth status does a fully specified declarative statement have?', 'a definite truth value', 'a definite truth value'),
        ('Recognition: Which is a statement?', 'Every integer is either even or odd.', 'a complete quantified declarative claim'),
        ('Recognition: Which operation makes the converse of “if P then Q”?', 'Swap P and Q.', 'swap the hypothesis and conclusion'),
    ],
    'quantifiers-negation-and-mathematical-translation': [
        ('What quantifier replaces “for every” when it is negated?', 'there exists', 'there exists'),
        ('When negating a quantified claim, what happens to the predicate?', 'it is negated', 'the predicate is negated'),
        ('What must remain fixed when translating a quantified statement?', 'its domain and scope', 'domain and scope'),
        ('What is one counterexample enough to refute?', 'a universal claim', 'a universal claim'),
        ('Recognition: Which phrase begins the negation of “Every integer is even”?', 'There exists an integer', 'an existential counterexample'),
        ('Recognition: Which translation preserves “if P, then Q”?', 'P is sufficient for Q.', 'the original conditional direction'),
    ],
    'definitions-theorems-and-examples': [
        ('What does a definition fix?', 'the meaning of a term', 'the meaning of a term'),
        ('What must be checked before applying a theorem?', 'its hypotheses', 'the theorem hypotheses'),
        ('What can a single example do?', 'illustrate a definition', 'illustrate a definition'),
        ('What status does one valid counterexample establish for a proposed universal statement?', 'the universal statement is false', 'the failed universal statement'),
        ('Recognition: Which role supplies the exact meaning of “even”?', 'A definition.', 'a definition'),
        ('Recognition: Which role gives a conclusion only after conditions hold?', 'A theorem.', 'a theorem'),
    ],
    'theorem-reading-and-application': [
        ('What condition licenses a theorem conclusion?', 'all of its hypotheses', 'all stated hypotheses'),
        ('What is the conclusion of a conditional theorem?', 'the claim after then', 'the consequent'),
        ('What must not be inferred from a theorem alone?', 'its converse', 'the converse'),
        ('What is a counterexample used to test?', 'a universal assertion', 'a universal assertion'),
        ('Recognition: What comes first in a valid theorem application?', 'Verify the hypotheses.', 'hypothesis verification'),
        ('Recognition: If H implies C, what is not automatically warranted?', 'C implies H.', 'the converse'),
    ],
    'reading-proofs-and-exposition': [
        ('What can justify a local proof step?', 'a definition, hypothesis, or earlier result', 'a cited definition, hypothesis, or earlier result'),
        ('What proof form proves “if P then Q” by showing “if not Q then not P”?', 'contrapositive proof', 'contrapositive proof'),
        ('What must a proof reader trace for each assertion?', 'its justification', 'a justification'),
        ('What does “therefore” require in a proof?', 'a warranted inference', 'a warranted inference'),
        ('Recognition: Which source can license substituting $n=2k$ after assuming n is even?', 'The definition of even.', 'the definition'),
        ('Recognition: Which claim is equivalent to “if P then Q”?', 'If not Q, then not P.', 'the contrapositive'),
    ],
    'proof-forms-and-argument-diagnosis': [
        ('What is formed by reversing hypothesis and conclusion?', 'the converse', 'the converse'),
        ('What is formed by negating and reversing a conditional?', 'the contrapositive', 'the contrapositive'),
        ('What is enough to disprove a universal statement?', 'one counterexample', 'one counterexample'),
        ('What must a direct proof connect to its conclusion?', 'the stated hypothesis', 'the stated hypothesis'),
        ('Recognition: Which is the converse of “if P then Q”?', 'If Q, then P.', 'the converse'),
        ('Recognition: Which is a valid response to an unsupported step?', 'Ask for the missing justification.', 'the missing justification'),
    ],
    'reading-mathematical-exposition': [
        ('What role fixes terminology in an exposition?', 'a definition', 'a definition'),
        ('What role supplies an assumption for an argument?', 'a hypothesis', 'a hypothesis'),
        ('What role illustrates a term without proving every case?', 'an example', 'an example'),
        ('What should connect a conclusion to earlier text?', 'a stated justification', 'a stated justification'),
        ('Recognition: Which sentence is a theorem application?', 'Since the hypotheses hold, the theorem gives the conclusion.', 'a conditional theorem use'),
        ('Recognition: Which role does not itself prove a universal result?', 'An example.', 'an example'),
    ],
    'mathematical-literacy-cumulative-review': [
        ('What does a domain restriction tell you?', 'which objects are allowed', 'the permitted objects'),
        ('What must be checked before citing a theorem?', 'all its hypotheses', 'all hypotheses'),
        ('What is the negation partner of “for every”?', 'there exists', 'there exists'),
        ('What must every proof step have?', 'a justification', 'a justification'),
        ('Recognition: Which reading preserves $B\\subseteq A$?', 'Every element of B belongs to A.', 'subset direction'),
        ('Recognition: Which move diagnoses a claim correctly?', 'Check its conditions before accepting its conclusion.', 'condition checking'),
    ],
}


def phase2_recall_and_lesson_checks(data_by_id: dict):
    """Materialize retrieval/recognition mix and section-specific lesson checks."""
    for data in data_by_id.values():
        topic = data.get('topicId')
        if data.get('assessmentType') == 'recallDrill' and topic in RECALL_FACTS:
            items = []
            for index, (prompt, expected, why) in enumerate(RECALL_FACTS[topic], 1):
                item_id = f'r{index:03d}'
                if prompt.startswith('Recognition:'):
                    stem = prompt.replace('Recognition: ', '')
                    # The alternatives deliberately encode the local reading error.
                    choices = [
                        {'id': 'a', 'text': expected},
                        {'id': 'b', 'text': 'A related term with the direction or role changed.', 'issueSignals': [{'id': 'mathematical-role-confusion'}]},
                        {'id': 'c', 'text': 'A numerical example rather than the requested reading.', 'issueSignals': [{'id': 'mathematical-structure-recognition-error'}]},
                        {'id': 'd', 'text': 'An unrelated proof label.', 'issueSignals': [{'id': 'proofStructure-error'}]},
                    ]
                    items.append({'id': item_id, 'type': 'recognition', 'prompt': stem,
                                  'choices': choices, 'answer': {'choiceId': 'a'},
                                  'issueSignals': [{'id': 'mathematical-structure-recognition-error'}],
                                  'explanation': f'Solution: {expected}.\nWhy it works: This is the requested retrieval fact about {why}.\nWhy the other choices fail: They change the requested relation, substitute an example for a term, or name an unrelated proof role.'})
                else:
                    items.append({'id': item_id, 'type': 'typed' if index != 3 else 'cloze', 'prompt': prompt,
                                  'answer': {'expected': expected, 'aliases': [expected]},
                                  'explanation': f'Solution: {expected}.\nWhy it works: The source reading convention identifies {why} without requiring a new calculation.'})
            data['items'] = items
        if data.get('assessmentType') == 'conceptLesson':
            sections = (data.get('lesson') or {}).get('sections', [])
            # Split dense four-part legacy lessons into seven teach/check actions while
            # retaining their original source-grounded prose.
            extensions = [
                ('Mark the object', 'First identify whether the line names a set, expression, statement, definition, theorem, or proof step.'),
                ('Preserve the condition', 'Copy the domain, hypothesis, or stated restriction before interpreting what follows from it.'),
                ('Track direction', 'For a conditional, mark what is assumed and what is concluded; do not silently reverse the arrow.'),
            ]
            while len(sections) < 7:
                title, content = extensions[len(sections) - 4]
                sections.append({'id': f'phase2-reading-action-{len(sections)+1}', 'title': title, 'content': content})
            for offset, (title, content) in enumerate(extensions, 4):
                sections[offset]['title'] = title
                sections[offset]['content'] = content
            checks = [
                ('Which reading move comes first?', 'Identify the mathematical object being named.', 'Treat every symbol as a numerical answer.', 'Discard the declared domain.', 'Use the title as a proof.'),
                ('What should remain visible while interpreting this section?', 'The stated condition or restriction.', 'Only a familiar example.', 'A reversed relation.', 'An unstated convention.'),
                ('How should a conditional be read?', 'From its hypothesis to its conclusion.', 'From conclusion back to hypothesis.', 'As two automatically equivalent claims.', 'As a set membership statement.'),
                ('What makes a local mathematical claim usable?', 'A definition, hypothesis, or result that licenses it.', 'Its position at the end of a paragraph.', 'A convenient numerical case.', 'The fact that it sounds plausible.'),
                ('What must a reader name before applying a rule?', 'The object and condition to which the rule applies.', 'Only the desired conclusion.', 'A different object with a similar name.', 'A counterexample to another claim.'),
                ('What must not be changed during a translation?', 'The scope and logical direction of the original.', 'The domain whenever notation is compact.', 'A theorem into a definition.', 'An example into a universal result.'),
                ('What should be checked before accepting a final conclusion?', 'That each required condition and inference has been established.', 'That the conclusion has been restated twice.', 'That the symbols have been simplified.', 'That a label appears beside the line.'),
            ]
            for index, section in enumerate(sections, 1):
                stem, correct, b, c, d = checks[index - 1]
                section['check'] = multiple_choice(
                    f'check-{index:03d}', f'{stem} ({section.get("title", "section")})',
                    [('a', correct), ('b', b), ('c', c), ('d', d)], 'a',
                    'mathematical-structure-recognition-error',
                    f'This section’s reading action is to {correct[0].lower() + correct[1:]}'
                )


def add_phase2_test(data_by_id: dict, assessment_id: str, title: str, prompts: list[tuple[str, str, str]]):
    questions = []
    for index, (prompt, key, reason) in enumerate(prompts, 1):
        questions.append({
            'id': f'q{index:03d}', 'type': 'freeResponse', 'prompt': prompt,
            'instruction': 'Give the requested reading judgment and name the condition, definition, or inference that licenses it.',
            'answer': {'gradingMode': 'selfCheck', 'keyPoints': [key]},
            'issueSignals': [{'id': 'mathematical-structure-recognition-error'}],
            'difficultyDimensions': ['representationTransfer', 'conditionChecking', 'argumentMapping'],
            'prerequisiteObjectiveIds': ['ml-notation', 'ml-logic'],
            'extensionObjectiveIds': ['ml-review'],
            'difficultyEvidence': 'Requires transferring a reading convention across notation, logic, and proof context while checking a stated condition.',
            'explanation': f'Solution: {key}\nWhy it works: {reason}',
        })
    data_by_id[assessment_id] = {
        'schemaVersion': 1, 'id': assessment_id, 'title': title, 'assessmentType': 'test',
        'categoryId': 'mathematical-literacy', 'topicId': 'mathematical-literacy-cumulative-review',
        'modeDefault': 'assessment', 'randomizeQuestions': True, 'attemptQuestionCount': 20,
        'skills': ['mathematical-literacy', 'mathematical-reading', 'proof-reading'],
        'navigation': {'learningGoal': 'evaluate', 'activityType': 'formalTest', 'tags': ['mathematical-literacy', 'cumulative-review', 'formal-test']},
        'authoring': {'difficultyTier': 'hard', 'visualRequirement': 'notApplicable',
                      'visualRationale': 'Each item assesses a textual mathematical reading decision; no diagram is needed to supply the givens.'},
        'questions': questions,
    }


def phase2_cumulative_tests(data_by_id: dict):
    core = [
        ('Read $B\\subseteq A$. State the direction in words.', 'Every element of B is an element of A.', 'Subset notation is directional containment, not membership of one whole set.'),
        ('A line says $x\\in\\mathbb Z$ and $x^2<9$. State what must be preserved in a translation.', 'x is an integer and its square is less than 9.', 'The declaration gives the domain and the inequality supplies the condition.'),
        ('Classify $x+1>0$ before x is bound.', 'It is an open sentence, not yet a statement.', 'Its truth changes with the unbound variable.'),
        ('Give the negation of “Every integer is even.”', 'There exists an integer that is not even.', 'Negating a universal switches to an existential and negates the property.'),
        ('A theorem says if a number is divisible by 6, it is divisible by 3. What must be shown for 18 first?', 'Show that 18 is divisible by 6.', 'The hypothesis must be verified before the conclusion is used.'),
        ('A proof assumes n is even and writes $n=2k$. Name the justification.', 'The definition of an even integer.', 'The definition supplies the integer parameter k.'),
        ('A student infers “if Q then P” from “if P then Q.” Diagnose the move.', 'It is the converse and needs separate justification.', 'Reversing a conditional does not preserve its truth automatically.'),
        ('What is the role of an example after a definition?', 'It illustrates one permitted case.', 'An example clarifies a meaning but does not prove a universal statement.'),
        ('A proof cites a theorem but has not established one hypothesis. What is the valid judgment?', 'The conclusion is not yet licensed.', 'A theorem step is valid only when all stated hypotheses hold.'),
        ('State the contrapositive of “If n is even, then n squared is even.”', 'If n squared is not even, then n is not even.', 'A contrapositive negates and reverses both sides.'),
    ]
    # A formal test needs twenty distinct condition checks rather than an arbitrary sampled scaffold.
    continuation = [
        ('What does the first set in $f:A\\to B$ name?', 'The domain of permitted inputs.', 'Function-arrow notation names its input set first.'),
        ('What does “for every” do to a variable?', 'It binds the variable over the stated domain.', 'Quantification turns a variable-dependent expression into a claim about that domain.'),
        ('Why is 2 a counterexample to “Every even integer is divisible by 4”?', '2 is even but is not divisible by 4.', 'One permitted case that fails a universal conclusion refutes it.'),
        ('What role does a hypothesis play in a proof?', 'It supplies an allowed condition for the argument.', 'A later inference may depend on an established hypothesis.'),
        ('What role does a conclusion play in a theorem?', 'It is the claim warranted after the hypotheses are verified.', 'The conclusion is conditional on the theorem’s assumptions.'),
        ('What must be tracked in a nested Cartesian product?', 'Its parentheses and coordinate grouping.', 'Grouping determines the shape of each ordered element.'),
        ('Why is a fully quantified false sentence still a statement?', 'It has a definite truth value.', 'Being false does not make a declarative quantified claim open.'),
        ('What must “therefore” summarize in a proof?', 'A justified inference from earlier material.', 'A transition word is not a substitute for a reason.'),
        ('What is wrong with using one example to establish every case?', 'It does not justify the universal claim.', 'A universal assertion requires a general argument, not one illustration.'),
        ('Before accepting a final line of exposition, what links should be visible?', 'Definitions, hypotheses, or theorems that license it.', 'Mathematical exposition is read as a chain of warranted roles and inferences.'),
    ]
    proof_exposition = [
        ('A definition says an integer is odd when it equals $2k+1$ for an integer k. What form may be written after assuming a is odd?', '$a=2m+1$ for some integer m.', 'The stated definition supplies the form and preserves the integer parameter.'),
        ('After writing $a=2m+1$ and $b=2n+1$, what form demonstrates that $a+b$ is even?', '$a+b=2(m+n+1)$.', 'Factoring 2 exhibits the definition of even.'),
        ('A proof starts by assuming the conclusion of “if P then Q” is false. What must it establish next?', 'That the hypothesis is false.', 'This is the target direction of a contrapositive argument.'),
        ('Why does a proof by contrapositive establish the original conditional?', 'A conditional and its contrapositive have the same truth value.', 'The logical equivalence licenses the proof form.'),
        ('A reader sees “Assume x belongs to S.” What role does that line have?', 'It is a hypothesis available for the argument.', 'Assumptions state conditions that later steps may use.'),
        ('A reader sees “By the definition of S, x has property R.” What role does the cited definition play?', 'It justifies unpacking membership in S into property R.', 'Definitions give the exact content of named properties.'),
        ('A theorem has two hypotheses H1 and H2. H1 is shown but H2 is not. What conclusion is warranted?', 'The theorem conclusion cannot yet be asserted.', 'Every listed condition is required for that theorem application.'),
        ('A sentence following “Example” verifies one case. What is its evidentiary role?', 'It illustrates a case rather than proving all cases.', 'An example is not a general proof.'),
        ('A proof says “therefore P” after an unrelated computation. What should a reader request?', 'A rule or earlier statement connecting the computation to P.', 'A conclusion needs an identifiable logical bridge.'),
        ('What distinguishes an implication from its converse during proof reading?', 'The implication preserves hypothesis-to-conclusion direction; the converse swaps them.', 'Swapping direction creates a different statement.'),
        ('A statement has a variable but begins “For every real x.” Is it open?', 'No; the quantifier binds x and gives a truth-valued claim.', 'Binding removes the free-variable dependence.'),
        ('A claim says “There exists an integer with property R.” What kind of evidence can establish it?', 'One integer that has property R.', 'An existential claim needs a witness.'),
        ('A claim says “Every integer has property R.” What kind of response disproves it?', 'One integer that lacks property R.', 'A counterexample refutes a universal claim.'),
        ('A passage defines a function before using it in a theorem. Why read the definition first?', 'It fixes the function’s domain and rule needed to check the theorem.', 'The later application depends on the precise defined object.'),
        ('What does a parenthesized product $A\\times(B\\times C)$ require an element to look like?', 'An ordered pair whose second component is an ordered pair.', 'Parentheses determine the nesting of the ordered structure.'),
        ('Why is “P if Q” dangerous to read quickly?', 'It means Q implies P, so the order differs from “if P, then Q.”', 'Language can encode a conditional direction opposite its visual order.'),
        ('A proof ends with a statement already known as a hypothesis. Is that a new theorem conclusion?', 'No; it merely restates an available assumption.', 'A proof conclusion must follow from a justified chain, not a relabeling.'),
        ('A theorem is cited after the phrase “clearly.” What must still be present?', 'Verification that its hypotheses match the current situation.', 'Rhetorical confidence does not discharge conditions.'),
        ('A counterexample uses an object outside the declared domain. Does it refute the claim?', 'No; a counterexample must lie in the claim’s domain.', 'Only permitted cases test a quantified statement.'),
        ('What should an annotation of a proof line record besides the line itself?', 'Its source of justification: definition, hypothesis, theorem, or prior inference.', 'That record makes the argument’s dependency chain inspectable.'),
    ]
    add_phase2_test(data_by_id, 'mathematical-literacy-cumulative-foundations-formal-test', 'Mathematical Literacy: Foundations Formal Test', core + continuation)
    add_phase2_test(data_by_id, 'mathematical-literacy-cumulative-proof-exposition-formal-test', 'Mathematical Literacy: Proof and Exposition Formal Test', proof_exposition)


FOCUSED_PRACTICE_MERGES = {
    'mathematical-literacy-notation-focused-practice': 'mathematical-literacy-notation-focused-practice-advanced',
    'mathematical-literacy-logic-focused-practice': 'mathematical-literacy-logic-focused-practice-advanced',
    'mathematical-literacy-quantifiers-negation-and-mathematical-translation-focused-practice-a': 'mathematical-literacy-quantifiers-negation-and-mathematical-translation-focused-practice-b',
    'mathematical-literacy-definitions-focused-practice': 'mathematical-literacy-definitions-focused-practice-advanced',
    'mathematical-literacy-theorem-reading-and-application-focused-practice-a': 'mathematical-literacy-theorem-reading-and-application-focused-practice-b',
    'mathematical-literacy-proofs-focused-practice': 'mathematical-literacy-proofs-focused-practice-advanced',
    'mathematical-literacy-proof-forms-and-argument-diagnosis-focused-practice-a': 'mathematical-literacy-proof-forms-and-argument-diagnosis-focused-practice-b',
    'mathematical-literacy-reading-mathematical-exposition-focused-practice-a': 'mathematical-literacy-reading-mathematical-exposition-focused-practice-b',
}


def phase2_merge_retired_focus_banks(data_by_id: dict):
    """Retain the sound, source-backed practice prompts from retired duplicate slots."""
    for canonical_id, retired_id in FOCUSED_PRACTICE_MERGES.items():
        canonical = data_by_id.get(canonical_id)
        path = RETIRED / f'{retired_id}.yaml'
        if not canonical or not path.exists():
            continue
        retired = load_yaml(path)
        existing_prompts = {prompt_summary(question) for question in canonical.get('questions', [])}
        for question in retired.get('questions', []):
            if prompt_summary(question) in existing_prompts:
                continue
            question = dict(question)
            question['id'] = f"q{len(canonical['questions']) + 1:03d}"
            canonical['questions'].append(question)
            existing_prompts.add(prompt_summary(question))


def phase2_authoring_metadata(data_by_id: dict):
    for data in data_by_id.values():
        authoring = data.setdefault('authoring', {})
        authoring.setdefault('visualRequirement', 'notApplicable')
        authoring.setdefault(
            'visualRationale',
            'The approved source evidence and the learner task are textual notation, statement, or proof readings; a diagram would not add a needed given.'
        )


def phase2_notation_quiz_bank(data_by_id: dict):
    focused = data_by_id['mathematical-literacy-notation-focused-practice']
    focused['questions'] = focused['questions'][:8] + [
        {'id': 'q009', 'type': 'multipleChoice', 'prompt': 'Let $S=\\{x\\in\\mathbb R:x\\geq0\\}$. Which claim is justified?',
         'choices': [{'id':'a','text':'$0\\in S$.'}, {'id':'b','text':'$-1\\in S$ because it is real.','issueSignals':[{'id':'set-builder-condition-ignored'}]}, {'id':'c','text':'$S$ contains only positive numbers.','issueSignals':[{'id':'domain-condition-ignored'}]}, {'id':'d','text':'$x\\geq0$ declares the domain.','issueSignals':[{'id':'expression-condition-confused'}]}],
         'answer':{'choiceId':'a'}, 'issueSignals':[{'id':'set-builder-condition-ignored'}], 'difficultyDimensions':['representationTransfer','domainCondition'], 'difficultyEvidence':'Separates the real-number domain from the nonnegative filtering condition.',
         'explanation':'Solution: $0\\in S$.\nWhy it works: Zero is real and satisfies $0\\geq0$.\nWhy the other choices fail: B ignores the inequality, C excludes the allowed boundary value zero, and D mistakes the filtering condition for the domain.'},
        {'id': 'q010', 'type': 'multipleChoice', 'prompt': 'If $g:\\mathbb N\\to\\mathbb Z$, which statement is guaranteed by the arrow notation?',
         'choices': [{'id':'a','text':'Every permitted input is a natural number and every output lies in the integers.'}, {'id':'b','text':'Every integer occurs as an output.','issueSignals':[{'id':'domain-rule-confused'}]}, {'id':'c','text':'Negative integers may be used as inputs.','issueSignals':[{'id':'domain-rule-confused'}]}, {'id':'d','text':'g is automatically one-to-one.','issueSignals':[{'id':'notation-role-confused'}]}],
         'answer':{'choiceId':'a'}, 'issueSignals':[{'id':'domain-rule-confused'}], 'difficultyDimensions':['representationTransfer','errorDiagnosis'], 'difficultyEvidence':'Distinguishes the input domain and output codomain from range and injectivity claims.',
         'explanation':'Solution: The inputs are natural numbers and the outputs are integers.\nWhy it works: In $g:A\\to B$, A is the permitted input set and B is the codomain.\nWhy the other choices fail: B confuses codomain with attained range, C changes the domain, and D adds an unstated one-to-one property.'},
    ]
    exposition = data_by_id.get('mathematical-literacy-reading-mathematical-exposition-mastery-check')
    if exposition:
        exposition['questions'] = [
            multiple_choice('q001', 'A passage says “Definition. An integer is even if it equals $2k$ for some integer k.” What is the passage doing?', [
                ('a', 'Fixing the exact meaning of “even.”'), ('b', 'Proving every integer is even.'), ('c', 'Giving a counterexample.'), ('d', 'Stating a converse theorem.'),
            ], 'a', 'mathematical-role-confusion', 'A definition fixes terminology; it does not by itself assert that every object has the property.'),
            multiple_choice('q002', 'A theorem has hypotheses H and conclusion C. Which reading is justified before citing the theorem?', [
                ('a', 'Verify H in the current situation, then infer C.'), ('b', 'Assume C and declare H true.'), ('c', 'Use C whenever a related example appears.'), ('d', 'Replace H with the converse of C.'),
            ], 'a', 'applicationStrategy-error', 'Theorem application is conditional: its stated hypotheses must be established before its conclusion is used.'),
            multiple_choice('q003', 'What is the role of a single example following a definition?', [
                ('a', 'It illustrates how the definition applies to one permitted case.'), ('b', 'It proves all later theorems.'), ('c', 'It changes the definition.'), ('d', 'It automatically supplies a counterexample.'),
            ], 'a', 'example-as-proof', 'An example clarifies a definition locally but cannot establish a universal conclusion by itself.'),
            multiple_choice('q004', 'A proof cites a theorem but has not checked one of its hypotheses. What should a reader conclude?', [
                ('a', 'The conclusion is not yet licensed; the missing hypothesis must be checked.'), ('b', 'The theorem becomes a definition.'), ('c', 'The conclusion is true because it appears after “therefore.”'), ('d', 'The missing hypothesis can be replaced by an example.'),
            ], 'a', 'unjustified-inference', 'A cited theorem supplies a valid step only when all of its conditions hold in the current argument.'),
        ]


def packet_map():
    return {packet['topicId']: packet for packet in json.loads(PACKETS_PATH.read_text(encoding='utf-8'))['packets']}


def blueprint_for(data: dict, packet: dict, principle: str, objective_id: str):
    records = []
    for item_id, question in collect_items(data):
        ensure_explanation(question, principle)
        if data.get('assessmentType') in ('quiz', 'test'):
            dimensions = question.get('difficultyDimensions') or ['representationTransfer', 'errorDiagnosis']
            minimum = 3 if (data.get('authoring') or {}).get('difficultyTier') == 'hard' else 2
            if len(dimensions) < minimum:
                dimensions = ['representationTransfer', 'conditionChecking', 'argumentMapping'][:minimum]
            question['difficultyDimensions'] = dimensions
        record_id = slug(f"{data['id']}-{item_id}-blueprint")
        records.append({
            'id': record_id,
            'assessmentId': data['id'],
            'questionId': item_id,
            'objectiveId': objective_id,
            'sourceChunks': [chunk for source in packet['sources'] for chunk in source['chunkIds']],
            'reviewState': 'approved',
            'questionType': question.get('type', 'freeResponse'),
            'givens': prompt_summary(question),
            'unknown': f"The exact response requested by {item_id}.",
            'representationRequirement': 'Read the supplied mathematical notation, statement, or proof role without changing its scope or direction.',
            'governingPrinciple': principle,
            'methodSteps': [
                'Identify the object, claim, or relation named in the prompt.',
                'Apply the topic-specific definition or logical rule to the stated conditions.',
                'Compare the result with the requested response form and keyed answer.',
            ],
            'likelyMisconception': 'Treating a familiar symbol or statement form as interchangeable with a different mathematical role.',
            'difficultyEvidence': 'The item requires reading the stated structure before selecting or producing the response; no unstated convention supplies the answer.',
            'answerVerificationMethod': f"Check the keyed answer against the prompt’s stated relation and the approved source chunk(s).",
            'variationAxes': ['mathematical representation', 'requested relation or conclusion', 'misconception branch'],
            'reasoningSignature': f"{slug(data['topicId'])}::{slug(prompt_summary(question))[:90]}",
        })
        if data.get('assessmentType') in ('quiz', 'test'):
            records[-1]['difficultyDimensions'] = question['difficultyDimensions']
            records[-1]['subjectDifficultyTags'] = ['mathematical-literacy', slug(data['topicId'])]
            records[-1]['prerequisiteObjectiveIds'] = question.get('prerequisiteObjectiveIds', [])
            records[-1]['extensionObjectiveIds'] = question.get('extensionObjectiveIds', [])
    blueprint_id = f"{data['id']}-phase1-blueprints"
    return blueprint_id, {
        'schemaVersion': 1,
        'id': blueprint_id,
        'categoryId': 'mathematical-literacy',
        'topicId': data['topicId'],
        'packetId': packet['id'],
        'reviewState': 'approved',
        'blueprints': records,
    }


def main():
    packets = packet_map()
    files = sorted(ASSESSMENTS.glob('mathematical-literacy-*.yaml'))
    data_by_id = {data['id']: data for path in files if (data := load_yaml(path))}
    merge_foundation_duplicates(data_by_id)
    replace_worked_example_b(data_by_id)
    replace_duplicate_mastery_checks(data_by_id)
    phase2_recall_and_lesson_checks(data_by_id)
    phase2_cumulative_tests(data_by_id)
    phase2_merge_retired_focus_banks(data_by_id)
    phase2_authoring_metadata(data_by_id)
    phase2_notation_quiz_bank(data_by_id)

    # New cumulative tests are created in memory, so materialize them before the
    # common packet/blueprint pass below.
    for assessment_id, data in data_by_id.items():
        path = ASSESSMENTS / f'{assessment_id}.yaml'
        if not path.exists():
            write_yaml(path, data)
    files = sorted(ASSESSMENTS.glob('mathematical-literacy-*.yaml'))

    for path in files:
        data = data_by_id[path.stem]
        normalize_issue_signals(data)
        packet = packets[data['topicId']]
        principle, objective_id = TOPIC_PRINCIPLES[data['topicId']]
        blueprint_id, blueprint = blueprint_for(data, packet, principle, objective_id)
        authoring = data.setdefault('authoring', {})
        authoring['sourcePacketId'] = packet['id']
        authoring['blueprintId'] = blueprint_id
        write_yaml(path, data)
        write_yaml(BLUEPRINTS / f'{blueprint_id}.yaml', blueprint)

    for duplicate_id in (
        'mathematical-literacy-notation-deep-concept-lesson',
        'mathematical-literacy-notation-recall-advanced',
        'mathematical-literacy-logic-deep-concept-lesson',
        'mathematical-literacy-logic-recall-advanced',
        'mathematical-literacy-proof-forms-and-argument-diagnosis-focused-practice-b',
        'mathematical-literacy-reading-mathematical-exposition-focused-practice-b',
        'mathematical-literacy-review-recall-b',
        'mathematical-literacy-notation-focused-practice-advanced',
        'mathematical-literacy-logic-focused-practice-advanced',
        'mathematical-literacy-quantifiers-negation-and-mathematical-translation-focused-practice-b',
        'mathematical-literacy-definitions-deep-concept-lesson',
        'mathematical-literacy-definitions-focused-practice-advanced',
        'mathematical-literacy-definitions-recall-advanced',
        'mathematical-literacy-theorem-reading-and-application-focused-practice-b',
        'mathematical-literacy-proofs-deep-concept-lesson',
        'mathematical-literacy-proofs-focused-practice-advanced',
        'mathematical-literacy-proofs-recall-advanced',
    ):
        source = ASSESSMENTS / f'{duplicate_id}.yaml'
        if source.exists():
            RETIRED.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(RETIRED / source.name))

    active = []
    for path in sorted(ASSESSMENTS.glob('mathematical-literacy-*.yaml')):
        data = load_yaml(path)
        active.append({
            'id': data['id'], 'topicId': data['topicId'], 'assessmentType': data['assessmentType'],
            'activityType': (data.get('navigation') or {}).get('activityType'),
            'packetId': data['authoring']['sourcePacketId'], 'blueprintId': data['authoring']['blueprintId'],
            'sourceEligibility': 'approved-page-image-or-nonempty-text', 'state': 'active',
            'remediation': 'phase-2 canonical sequence and comparative review passed',
        })
    retired = []
    for path in sorted(RETIRED.glob('mathematical-literacy-*.yaml')):
        data = load_yaml(path)
        retired.append({'id': data['id'], 'archivePath': f'data/retired-assessments/{path.name}', 'state': 'archived'})
    write_yaml(STATUS_PATH, {
        'schemaVersion': 1, 'id': 'mathematical-literacy-s2c-migration-status',
        'categoryId': 'mathematical-literacy', 'status': 'phase-2-in-progress',
        'activeDefinitions': active, 'retiredDefinitions': retired,
        'compatibility': 'Archived definitions retain stable IDs and are outside active discovery; historical attempts may rely on stored snapshots.',
        'completionGate': 'Every active assessment must reference an approved packet, a complete assessment-scoped blueprint, and a passing Phase 2 comparative review before this status can become complete.',
    })
    active_blueprint_files = {f"{entry['blueprintId']}.yaml" for entry in active}
    retired_blueprints = ROOT / 'docs' / 'assessment-reference' / 'retired-blueprints'
    for blueprint_path in BLUEPRINTS.glob('mathematical-literacy-*.yaml'):
        if blueprint_path.name not in active_blueprint_files:
            retired_blueprints.mkdir(parents=True, exist_ok=True)
            shutil.move(str(blueprint_path), str(retired_blueprints / blueprint_path.name))


if __name__ == '__main__':
    main()
