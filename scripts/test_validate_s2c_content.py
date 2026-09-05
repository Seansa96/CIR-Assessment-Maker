"""Focused regression tests for Mathematical Literacy S2C content gates."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).with_name('validate_s2c_content.py')
SPEC = importlib.util.spec_from_file_location('validate_s2c_content', MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)


class MathematicalLiteracyS2CGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.original_source_directory = validator.SOURCE_DIRECTORY
        self.original_blueprint_directory = validator.BLUEPRINT_DIRECTORY
        self.original_status_path = validator.MIGRATION_STATUS_PATH
        validator.SOURCE_DIRECTORY = str(self.root / 'sources')
        validator.BLUEPRINT_DIRECTORY = str(self.root / 'blueprints')
        validator.MIGRATION_STATUS_PATH = str(self.root / 'status.yaml')

    def tearDown(self):
        validator.SOURCE_DIRECTORY = self.original_source_directory
        validator.BLUEPRINT_DIRECTORY = self.original_blueprint_directory
        validator.MIGRATION_STATUS_PATH = self.original_status_path
        self.temp.cleanup()

    def write_source(self, state='approved', text='Reviewed transcription', image_path='page-images/page-0001.png'):
        source = Path(validator.SOURCE_DIRECTORY) / 'src-test'
        (source / 'page-images').mkdir(parents=True, exist_ok=True)
        (source / 'manifest.json').write_text(json.dumps({'id': 'src-test', 'chunkCount': 1}), encoding='utf-8')
        (source / 'page-images' / 'page-0001.png').write_bytes(b'PNG')
        (source / 'chunks.json').write_text(json.dumps([{
            'id': 'src-test:page-0001', 'kind': 'page-image', 'text': text,
            'transcriptionReviewState': state, 'imagePath': image_path,
        }]), encoding='utf-8')
        return {'id': 'packet-test', 'sources': [{'sourceId': 'src-test', 'chunkIds': ['src-test:page-0001']}]}

    def test_approved_page_image_chunk_is_eligible(self):
        errors = []
        allowed = validator.source_chunks_for_packet(self.write_source(), errors)
        self.assertEqual([], errors)
        self.assertEqual({'src-test:page-0001'}, allowed)

    def test_nonempty_legacy_text_chunk_remains_eligible(self):
        source = Path(validator.SOURCE_DIRECTORY) / 'src-text'
        source.mkdir(parents=True)
        (source / 'manifest.json').write_text(json.dumps({'id': 'src-text', 'chunkCount': 1}), encoding='utf-8')
        (source / 'chunks.json').write_text(json.dumps([{
            'id': 'src-text:chunk-0001', 'kind': 'text', 'text': 'Faithful imported source text.',
        }]), encoding='utf-8')
        errors = []
        allowed = validator.source_chunks_for_packet({
            'id': 'packet-text', 'sources': [{'sourceId': 'src-text', 'chunkIds': ['src-text:chunk-0001']}],
        }, errors)
        self.assertEqual([], errors)
        self.assertEqual({'src-text:chunk-0001'}, allowed)

    def test_draft_blank_and_traversal_page_images_are_rejected(self):
        for state, text, image_path in (
            ('draft', 'Reviewed transcription', 'page-images/page-0001.png'),
            ('approved', '', 'page-images/page-0001.png'),
            ('approved', 'Reviewed transcription', '../outside.png'),
        ):
            with self.subTest(state=state, text=text, image_path=image_path):
                errors = []
                allowed = validator.source_chunks_for_packet(self.write_source(state, text, image_path), errors)
                self.assertEqual(set(), allowed)
                self.assertTrue(errors)

    def test_blueprint_requires_item_coverage_and_unique_signature(self):
        packet = self.write_source()
        blueprints = Path(validator.BLUEPRINT_DIRECTORY)
        blueprints.mkdir(parents=True)
        record = {
            'id': 'bp-1', 'assessmentId': 'assessment-1', 'questionId': 'q001',
            'objectiveId': 'ml-test', 'sourceChunks': ['src-test:page-0001'], 'reviewState': 'approved',
            'questionType': 'multipleChoice', 'givens': 'A claim', 'unknown': 'classification',
            'representationRequirement': 'statement', 'governingPrinciple': 'A statement has a definite truth value.',
            'methodSteps': ['read the claim', 'check its truth condition'], 'likelyMisconception': 'Treating a question as a statement.',
            'difficultyEvidence': 'Requires classifying the sentence form.', 'answerVerificationMethod': 'Check the definition.',
            'variationAxes': ['sentence form', 'truth condition'], 'reasoningSignature': 'statement-classification',
        }
        (blueprints / 'bp.yaml').write_text(__import__('yaml').safe_dump({
            'categoryId': 'mathematical-literacy', 'topicId': 'mathematical-statements-and-logic',
            'packetId': 'packet-test', 'blueprints': [record, {**record, 'id': 'bp-2'}],
        }), encoding='utf-8')
        data = {
            'id': 'assessment-1', 'topicId': 'mathematical-statements-and-logic',
            'questions': [{'id': 'q001'}, {'id': 'q002'}],
        }
        errors = []
        validator.validate_blueprint('bp', data, packet, {'src-test:page-0001'}, errors)
        self.assertTrue(any('missing item coverage' in error for error in errors))
        self.assertTrue(any('repeats reasoning signatures' in error for error in errors))


if __name__ == '__main__':
    unittest.main()
