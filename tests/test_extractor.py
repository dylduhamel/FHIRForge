import pytest
from src.nlp.extractor import ClinicalEntityExtractor


def test_extract_conditions():
    extractor = ClinicalEntityExtractor()
    text = "Patient has diabetes and hypertension"
    entities = extractor.extract_entities(text)

    conditions = [e for e in entities if e.entity_type == "condition"]
    assert len(conditions) == 2
    assert any("diabetes" in e.text for e in conditions)
    assert any("hypertension" in e.text for e in conditions)


def test_extract_medications():
    extractor = ClinicalEntityExtractor()
    text = "Patient is taking metformin and lisinopril"
    entities = extractor.extract_entities(text)

    medications = [e for e in entities if e.entity_type == "medication"]
    assert len(medications) == 2


def test_empty_text():
    extractor = ClinicalEntityExtractor()
    entities = extractor.extract_entities("")
    assert len(entities) == 0


def test_confidence_scores():
    extractor = ClinicalEntityExtractor()
    text = "Patient has diabetes"
    entities = extractor.extract_entities(text)

    for entity in entities:
        assert 0 <= entity.confidence <= 1