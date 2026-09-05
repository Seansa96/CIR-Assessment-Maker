import os
import sys
import yaml
import glob
import json
import re
from collections import Counter
from functools import lru_cache

REPEATED_CONCLUSION = 'Therefore the answer is '
GENERIC_TEMPLATE_DISTRACTORS = {
    'use a relation from a different representation.',
    'reverse a sign, direction, or role without justification.',
    'ignore the stated geometric constraints.',
}
GENERIC_DISTRACTOR_FEEDBACK = 'why the other choices fail: each changes a sign, swaps a role, or applies a different relationship.'
RETIRED_EDITORIAL_CHOICE_PATTERN = "(answers '"
GENERIC_WHY_IT_WORKS = 'why it works: this uses the defining relationship for the topic.'
DOUBLE_QUOTED_LATEX = re.compile(r'"[^"\n]*\\[^"\n]*"')

PACKET_PATH = os.path.join('docs', 'assessment-reference', 'packets', 'mathematical-literacy-v2-packets.json')
BLUEPRINT_DIRECTORY = os.path.join('docs', 'assessment-reference', 'question-blueprints')
SOURCE_DIRECTORY = os.path.join('data', 'source-library', 'sources')
MIGRATION_STATUS_PATH = os.path.join('docs', 'assessment-reference', 'content-manifests', 'mathematical-literacy-s2c-migration-status.yaml')
BLUEPRINT_REQUIRED_FIELDS = {
    'id', 'assessmentId', 'questionId', 'objectiveId', 'sourceChunks', 'reviewState',
    'questionType', 'givens', 'unknown', 'representationRequirement',
    'governingPrinciple', 'methodSteps', 'likelyMisconception',
    'difficultyEvidence', 'answerVerificationMethod', 'variationAxes',
    'reasoningSignature',
}
GENERIC_GOVERNING_PRINCIPLES = {
    'preserve scope, direction, and justification',
    'integrate scope, direction, and justification',
    'apply the governing relationship',
    'use the defining relationship for the topic',
}

def mathematical_literacy_packets():
    try:
        with open(PACKET_PATH, 'r', encoding='utf-8') as f:
            return {packet['id']: packet for packet in json.load(f).get('packets', [])}
    except (OSError, ValueError, KeyError):
        return {}

def load_blueprint(blueprint_id):
    path = os.path.join(BLUEPRINT_DIRECTORY, f'{blueprint_id}.yaml')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}, path
    except (OSError, yaml.YAMLError):
        return None, path

@lru_cache(maxsize=1)
def active_reasoning_signature_counts():
    """Return signatures only from blueprints referenced by the active ML inventory."""
    try:
        with open(MIGRATION_STATUS_PATH, 'r', encoding='utf-8') as f:
            status = yaml.safe_load(f) or {}
        blueprint_ids = {
            entry.get('blueprintId') for entry in status.get('activeDefinitions', [])
            if entry.get('blueprintId')
        }
    except (OSError, yaml.YAMLError):
        return Counter()
    signatures = []
    for blueprint_id in blueprint_ids:
        blueprint, _ = load_blueprint(blueprint_id)
        if blueprint:
            signatures.extend(
                record.get('reasoningSignature') for record in blueprint.get('blueprints', [])
                if record.get('reasoningSignature')
            )
    return Counter(signatures)

def source_chunks_for_packet(packet, errors):
    allowed = set()
    for source in packet.get('sources', []):
        source_id = source.get('sourceId')
        if not source_id:
            errors.append(f"Packet '{packet.get('id', '<unknown>')}' has a source without sourceId.")
            continue
        manifest_path = os.path.join(SOURCE_DIRECTORY, source_id, 'manifest.json')
        chunks_path = os.path.join(SOURCE_DIRECTORY, source_id, 'chunks.json')
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            with open(chunks_path, 'r', encoding='utf-8') as f:
                chunks = {chunk.get('id'): chunk for chunk in json.load(f)}
        except (OSError, ValueError, TypeError):
            errors.append(f"Packet '{packet.get('id', '<unknown>')}' cannot resolve source '{source_id}' manifest/chunks.")
            continue
        if not manifest.get('id') or manifest.get('chunkCount', 0) <= 0:
            errors.append(f"Packet '{packet.get('id', '<unknown>')}' references an empty source manifest '{source_id}'.")
            continue
        for chunk_id in source.get('chunkIds', []):
            chunk = chunks.get(chunk_id)
            if not chunk:
                errors.append(f"Packet '{packet.get('id', '<unknown>')}' references missing chunk '{chunk_id}'.")
                continue
            if not str(chunk.get('text') or '').strip():
                errors.append(f"Packet '{packet.get('id', '<unknown>')}' references empty chunk '{chunk_id}'.")
                continue
            if chunk.get('kind') == 'page-image':
                image_path = str(chunk.get('imagePath') or '')
                expected_root = os.path.abspath(os.path.join(SOURCE_DIRECTORY, source_id))
                resolved_image = os.path.abspath(os.path.join(expected_root, image_path))
                if (chunk.get('transcriptionReviewState') != 'approved'
                        or not image_path
                        or not resolved_image.startswith(expected_root + os.sep)
                        or not os.path.isfile(resolved_image)):
                    errors.append(f"Packet '{packet.get('id', '<unknown>')}' references ineligible page-image chunk '{chunk_id}' (approved transcription and safe image are required).")
                    continue
            allowed.add(chunk_id)
    return allowed

def collect_answer_bearing_items(data):
    items = []
    for index, question in enumerate(data.get('questions', [])):
        items.append((question.get('id', f'q-{index + 1}'), question))
    for example in data.get('workedExamples', []):
        for index, step in enumerate(example.get('steps', [])):
            question = step.get('question', step)
            items.append((question.get('id') or step.get('id', f'step-{index + 1}'), question))
    for section in (data.get('lesson') or {}).get('sections', []):
        if section.get('check'):
            question = section['check']
            items.append((question.get('id', f"{section.get('id', 'section')}-check"), question))
    for section in (data.get('glossary') or {}).get('sections', []):
        for entry in section.get('entries', []):
            for index, drill in enumerate(entry.get('drills', [])):
                items.append((drill.get('id', f"{entry.get('id', 'entry')}-drill-{index + 1}"), drill))
    for index, item in enumerate(data.get('items', [])):
        items.append((item.get('id', f'item-{index + 1}'), item))
    return items

def validate_blueprint(blueprint_id, data, packet, allowed_chunks, errors):
    blueprint, path = load_blueprint(blueprint_id)
    if blueprint is None:
        errors.append(f"Mathematical Literacy assessment references missing blueprint '{blueprint_id}'.")
        return
    if blueprint.get('categoryId') != 'mathematical-literacy':
        errors.append(f"Blueprint '{blueprint_id}' has an invalid categoryId.")
    if blueprint.get('topicId') != data.get('topicId'):
        errors.append(f"Blueprint '{blueprint_id}' topicId does not match the assessment.")
    if blueprint.get('packetId') != packet.get('id'):
        errors.append(f"Blueprint '{blueprint_id}' packetId does not match authoring.sourcePacketId.")
    records = blueprint.get('blueprints')
    if not isinstance(records, list):
        errors.append(f"Blueprint '{blueprint_id}' must contain a blueprints list.")
        return
    expected_ids = {item_id for item_id, _ in collect_answer_bearing_items(data)}
    record_ids = set()
    signatures = []
    for index, record in enumerate(records):
        missing = sorted(field for field in BLUEPRINT_REQUIRED_FIELDS if not record.get(field))
        if missing:
            errors.append(f"Blueprint '{blueprint_id}' record {index + 1} is missing: {', '.join(missing)}.")
            continue
        if record.get('assessmentId') != data.get('id'):
            errors.append(f"Blueprint '{blueprint_id}' record '{record.get('id')}' has the wrong assessmentId.")
        record_ids.add(record.get('questionId'))
        if record.get('reviewState') != 'approved':
            errors.append(f"Blueprint '{blueprint_id}' record '{record.get('id')}' is not approved.")
        if not isinstance(record.get('methodSteps'), list) or len(record['methodSteps']) < 2:
            errors.append(f"Blueprint '{blueprint_id}' record '{record.get('id')}' needs at least two methodSteps.")
        if not isinstance(record.get('variationAxes'), list) or len(record['variationAxes']) < 2:
            errors.append(f"Blueprint '{blueprint_id}' record '{record.get('id')}' needs at least two variationAxes.")
        if not isinstance(record.get('sourceChunks'), list) or not set(record['sourceChunks']).issubset(allowed_chunks):
            errors.append(f"Blueprint '{blueprint_id}' record '{record.get('id')}' cites chunks outside its eligible packet.")
        if normalized_choice_text(record.get('governingPrinciple')) in GENERIC_GOVERNING_PRINCIPLES:
            errors.append(f"Blueprint '{blueprint_id}' record '{record.get('id')}' uses generic governing-principle boilerplate.")
        signatures.append(record.get('reasoningSignature'))
    missing_records = expected_ids - record_ids
    extra_records = record_ids - expected_ids
    if missing_records:
        errors.append(f"Blueprint '{blueprint_id}' is missing item coverage for: {', '.join(sorted(missing_records))}.")
    if extra_records:
        errors.append(f"Blueprint '{blueprint_id}' has records for unknown items: {', '.join(sorted(extra_records))}.")
    duplicates = [signature for signature, count in Counter(signatures).items() if signature and count > 1]
    if duplicates:
        errors.append(f"Blueprint '{blueprint_id}' repeats reasoning signatures: {', '.join(sorted(duplicates))}.")
    active_duplicates = {
        signature for signature, count in active_reasoning_signature_counts().items()
        if count > 1 and signature in signatures
    }
    if active_duplicates:
        errors.append(f"Blueprint '{blueprint_id}' has globally repeated reasoning signatures: {', '.join(sorted(active_duplicates))}.")

def normalized_choice_text(text):
    return ' '.join(str(text or '').lower().split())

def repeated_conclusion(explanation):
    conclusions = [part.strip() for part in explanation.split(REPEATED_CONCLUSION)[1:]]
    return len(conclusions) > 1 and any(conclusions[0] == conclusion for conclusion in conclusions[1:])

def validate_question_item(q, q_id, assessment_type, errors):
    if not q:
        return
        
    q_type = q.get('type', '')
    
    # Explanations
    explanation = q.get('explanation', '')
    if not explanation:
        errors.append(f"{q_id}: Missing explanation.")
    else:
        if 'Solution:' not in explanation:
            errors.append(f"{q_id}: Explanation missing 'Solution:'.")
        if 'Why it works:' not in explanation:
            errors.append(f"{q_id}: Explanation missing 'Why it works:'.")
        if q_type == 'multipleChoice' and 'Why the other choices fail:' not in explanation:
            errors.append(f"{q_id}: multipleChoice explanation missing 'Why the other choices fail:'.")
        if q_type == 'multipleChoice' and GENERIC_DISTRACTOR_FEEDBACK in normalized_choice_text(explanation):
            errors.append(f"{q_id}: Generic distractor feedback. Explain why each competing choice fails for this prompt.")
        if GENERIC_WHY_IT_WORKS in normalized_choice_text(explanation):
            errors.append(f"{q_id}: Generic 'Why it works' explanation. Name the governing relationship for this prompt.")
        if repeated_conclusion(explanation):
            errors.append(f"{q_id}: Explanation repeats its 'Therefore the answer is' conclusion.")
    
    # Difficulty Dimensions (Quizzes and Tests)
    if assessment_type in ['quiz', 'test']:
        if 'difficultyDimensions' not in q:
            errors.append(f"{q_id}: Scored STEM quiz/test item missing 'difficultyDimensions'.")
        elif not isinstance(q['difficultyDimensions'], list):
            errors.append(f"{q_id}: 'difficultyDimensions' must be a list of enums, not a scalar value.")
        elif len(q['difficultyDimensions']) < 2:
            errors.append(f"{q_id}: Scored STEM quiz/test item must have at least 2 distinct difficulty dimensions.")
    
    # Free Response
    if q_type == 'freeResponse':
        answer = q.get('answer', {})
        if 'expected' in answer:
            errors.append(f"{q_id}: freeResponse uses 'expected'. Rely on 'gradingMode: selfCheck' instead.")

def validate_file(filepath):
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw = f.read()
            if DOUBLE_QUOTED_LATEX.search(raw):
                errors.append('Double-quoted YAML scalar contains a LaTeX backslash. Use a block scalar or a single-quoted scalar.')
            f.seek(0)
            data = yaml.safe_load(f)
            if not data:
                return errors
                
            assessment_type = data.get('assessmentType', '')
            if data.get('categoryId') == 'mathematical-literacy':
                packets = mathematical_literacy_packets()
                authoring = data.get('authoring') or {}
                packet_id = authoring.get('sourcePacketId')
                blueprint_id = authoring.get('blueprintId')
                if not packet_id:
                    errors.append('Mathematical Literacy assessment is missing authoring.sourcePacketId.')
                elif packet_id not in packets:
                    errors.append(f"Mathematical Literacy assessment references unknown packet '{packet_id}'.")
                elif packets[packet_id].get('topicId') != data.get('topicId'):
                    errors.append(f"Mathematical Literacy assessment packet '{packet_id}' does not match topicId '{data.get('topicId')}'.")
                if not blueprint_id:
                    errors.append('Mathematical Literacy assessment is missing authoring.blueprintId.')
                elif packet_id in packets:
                    allowed_chunks = source_chunks_for_packet(packets[packet_id], errors)
                    validate_blueprint(blueprint_id, data, packets[packet_id], allowed_chunks, errors)
            
            multiple_choice_questions = []

            def collect_question(q, q_id):
                validate_question_item(q, q_id, assessment_type, errors)
                if q and q.get('type') == 'multipleChoice':
                    multiple_choice_questions.append((q_id, q))

            # Check all questions (Quiz/Test)
            questions = data.get('questions', [])
            for i, q in enumerate(questions):
                q_id = q.get('id', f'index-{i}')
                collect_question(q, q_id)

            # Check worked example steps
            worked_examples = data.get('workedExamples', [])
            for we in worked_examples:
                steps = we.get('steps', [])
                for i, step in enumerate(steps):
                    step_id = step.get('id', f'step-{i}')
                    question = step.get('question', step)
                    collect_question(question, step_id)
            
            # Check concept lesson checks
            lesson = data.get('lesson', {})
            if lesson:
                sections = lesson.get('sections', [])
                if assessment_type == 'conceptLesson':
                    def repeated(values):
                        seen = set()
                        for value in values:
                            value = normalized_choice_text(value)
                            if value and value in seen:
                                return True
                            seen.add(value)
                        return False
                    if repeated(section.get('content', '') for section in sections):
                        errors.append('Concept lesson repeats section prose. Each section must teach a distinct step.')
                    checks = [section.get('check') for section in sections if section.get('check')]
                    if repeated(check.get('prompt', '') for check in checks):
                        errors.append('Concept lesson repeats learning-check prompts. Use section-specific questions.')
                    if repeated(check.get('explanation', '') for check in checks):
                        errors.append('Concept lesson repeats learning-check explanations. Tie each explanation to its prompt.')
                    choice_uses = {}
                    for check in checks:
                        for choice in check.get('choices', []):
                            text = normalized_choice_text(choice.get('text'))
                            if text:
                                choice_uses.setdefault(text, set()).add(check.get('id', 'check'))
                    for text, check_ids in choice_uses.items():
                        if len(check_ids) > 1:
                            errors.append(f"Repeated concept-lesson answer choice '{text}' appears in {len(check_ids)} checks. Use section-specific choices.")
                for sec in sections:
                    check = sec.get('check')
                    if check:
                        check_id = check.get('id', f"{sec.get('id', 'section')}-check")
                        collect_question(check, check_id)

            # Check glossary drills
            glossary = data.get('glossary', {})
            if glossary:
                sections = glossary.get('sections', [])
                for sec in sections:
                    entries = sec.get('entries', [])
                    for entry in entries:
                        drills = entry.get('drills', [])
                        for i, drill in enumerate(drills):
                            drill_id = drill.get('id', f"{entry.get('id', 'entry')}-drill-{i}")
                            validate_question_item(drill, drill_id, assessment_type, errors)

            # Check recall drills. Recall items are answer-bearing even though they are not
            # quiz questions, so they must carry the same instructional explanation contract.
            for i, item in enumerate(data.get('items', [])):
                validate_question_item(item, item.get('id', f'item-{i}'), assessment_type, errors)

            if assessment_type == 'workedExample' and data.get('categoryId') == 'physics-2':
                enforce = data.get('topicId') == 'physics2-electric-charges-fields'
                examples = data.get('workedExamples', [])
                steps = [step.get('question', step) for example in examples for step in example.get('steps', [])]
                auto = {'multipleChoice', 'selectAll', 'numericResponse', 'symbolicResponse'}
                if any(len(example.get('steps', [])) < 3 or len(example.get('steps', [])) > 6 for example in examples): errors.append('Physics 2 worked-example problems require three to six checkpoints.')
                if not steps or sum(step.get('type') in auto for step in steps) / len(steps) < .75: errors.append('Physics 2 worked examples require at least 75% auto-checkable checkpoints.')
                if enforce and any(step.get('type') == 'freeResponse' for step in steps): errors.append('Electric Charges and Fields worked examples may not use self-check free response.')
                if any('Explain how this step advances' in step.get('prompt', '') for step in steps): errors.append('Worked-example prompts must be concrete, not generic scaffolding.')

            distractor_uses = {}
            for q_id, question in multiple_choice_questions:
                correct_id = question.get('answer', {}).get('choiceId')
                for choice in question.get('choices', []):
                    if choice.get('id') == correct_id:
                        continue
                    text = normalized_choice_text(choice.get('text'))
                    if text in GENERIC_TEMPLATE_DISTRACTORS:
                        errors.append(f"{q_id}: Generic template distractor '{choice.get('text')}'. Use a prompt-specific misconception or competing result.")
                    if RETIRED_EDITORIAL_CHOICE_PATTERN in str(choice.get('text', '')):
                        errors.append(f"{q_id}: Learner-visible editorial answer annotation is retired. Use a concise distractor only.")
                    if text:
                        distractor_uses.setdefault(text, set()).add(q_id)
            for text, question_ids in distractor_uses.items():
                if len(question_ids) > 1:
                    errors.append(f"Repeated multiple-choice distractor '{text}' appears in {len(question_ids)} questions. Use prompt-specific distractors.")
                            
    except Exception as e:
        errors.append(f"Failed to parse or read file: {e}")
        
    return errors

def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        # Default to checking all assessments if none specified
        files = glob.glob('data/assessments/*.yaml')
        
    total_errors = 0
    for f in files:
        if not os.path.exists(f):
            print(f"File not found: {f}")
            continue
            
        errors = validate_file(f)
        if errors:
            print(f"\n[FAIL] {f}")
            for err in errors:
                print(f"  - {err}")
            total_errors += len(errors)
        else:
            print(f"[PASS] {f}")
            
    if total_errors > 0:
        print(f"\nFound {total_errors} S2C constraint violations.")
        sys.exit(1)
    else:
        print("\nAll files passed S2C constraints!")
        sys.exit(0)

if __name__ == "__main__":
    main()
