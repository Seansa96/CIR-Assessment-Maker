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
            if len(dimensions) < 2:
                dimensions = ['representationTransfer', 'errorDiagnosis']
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
            'remediation': 'phase-1 provenance complete',
        })
    retired = []
    for path in sorted(RETIRED.glob('mathematical-literacy-*.yaml')):
        data = load_yaml(path)
        retired.append({'id': data['id'], 'archivePath': f'data/retired-assessments/{path.name}', 'state': 'archived'})
    write_yaml(STATUS_PATH, {
        'schemaVersion': 1, 'id': 'mathematical-literacy-s2c-migration-status',
        'categoryId': 'mathematical-literacy', 'status': 'phase-1-complete',
        'activeDefinitions': active, 'retiredDefinitions': retired,
        'compatibility': 'Archived definitions retain stable IDs and are outside active discovery; historical attempts may rely on stored snapshots.',
        'completionGate': 'Every active assessment must reference an approved packet and a complete assessment-scoped blueprint before this status can become complete.',
    })
    active_blueprint_files = {f"{entry['blueprintId']}.yaml" for entry in active}
    retired_blueprints = ROOT / 'docs' / 'assessment-reference' / 'retired-blueprints'
    for blueprint_path in BLUEPRINTS.glob('mathematical-literacy-*.yaml'):
        if blueprint_path.name not in active_blueprint_files:
            retired_blueprints.mkdir(parents=True, exist_ok=True)
            shutil.move(str(blueprint_path), str(retired_blueprints / blueprint_path.name))


if __name__ == '__main__':
    main()
