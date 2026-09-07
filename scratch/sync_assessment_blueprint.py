"""Synchronize approved S2C blueprint records with an explicitly authored assessment bank."""
from __future__ import annotations

import sys
from pathlib import Path
import yaml


def slug(value: str) -> str:
    return ''.join(char.lower() if char.isalnum() else '-' for char in value).strip('-')[:150]


assessment_path = Path(sys.argv[1])
blueprint_path = Path(sys.argv[2])
assessment = yaml.safe_load(assessment_path.read_text(encoding='utf-8'))
blueprint = yaml.safe_load(blueprint_path.read_text(encoding='utf-8'))
source_chunks = blueprint['blueprints'][0]['sourceChunks']
existing = {record['questionId']: record for record in blueprint['blueprints']}
records = []
for question in assessment['questions']:
    record = existing.get(question['id'], {})
    issue = next((signal['id'] for choice in question.get('choices', []) for signal in choice.get('issueSignals', [])), 'interpretation-error')
    record.update({
        'id': f"{assessment['id']}-{question['id']}-blueprint",
        'assessmentId': assessment['id'],
        'questionId': question['id'],
        'objectiveId': record.get('objectiveId', blueprint['blueprints'][0]['objectiveId']),
        'sourceChunks': source_chunks,
        'reviewState': 'approved',
        'questionType': question['type'],
        'givens': question['prompt'],
        'unknown': 'The exact response requested by the question.',
        'representationRequirement': 'Interpret the specified notation and preserve every stated domain, grouping, and relation.',
        'governingPrinciple': 'Apply the packet-supported definition or logical structure named in the prompt.',
        'methodSteps': ['Identify the declared object and its conditions.', 'Apply the governing definition or relation.', 'Check the keyed result against every condition.'],
        'likelyMisconception': f"The prompt-specific misconception captured by issue signal '{issue}'.",
        'difficultyEvidence': question['difficultyEvidence'],
        'answerVerificationMethod': 'Check the keyed response directly against the stated definition, domain, and relation.',
        'variationAxes': ['representation', 'condition or domain', 'misconception branch'],
        'reasoningSignature': f"{assessment['id']}::{question['id']}::{slug(question['prompt'])}",
        'difficultyDimensions': question['difficultyDimensions'],
        'subjectDifficultyTags': ['mathematical-literacy', assessment['topicId']],
        'prerequisiteObjectiveIds': question.get('prerequisiteObjectiveIds', []),
        'extensionObjectiveIds': question.get('extensionObjectiveIds', []),
    })
    records.append(record)
blueprint['blueprints'] = records
blueprint_path.write_text(yaml.safe_dump(blueprint, sort_keys=False, allow_unicode=True, width=110), encoding='utf-8')
