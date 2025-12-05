import spacy
from typing import List, Tuple
from src.api.models import Entity


class ClinicalEntityExtractor:
    """Extract medical entities from clinical notes"""

    def __init__(self):
        # Basic spaCy for now
        #self.nlp = spacy.load("en_core_web_sm")

        # Simple keyword matching of medical entities
        self.condition_keywords = [
            "pain", "diabetes", "hypertension", "infection", "fever",
            "myocardial infarction", "mi", "copd", "asthma", "pneumonia"
        ]

        self.medication_keywords = [
            "lisinopril", "metformin", "aspirin", "insulin", "atorvastatin",
            "omeprazole", "levothyroxine", "amlodipine"
        ]

        self.procedure_keywords = [
            "surgery", "intervention", "biopsy", "imaging", "x-ray",
            "ct scan", "mri", "ultrasound", "echocardiogram"
        ]

    def extract_entities(self, text: str) -> List[Entity]:
        """
        Extract medical entities from text

        :param text: Clinical note text
        :return: list of extracted entities with positions and confidence
        """

        #doc = self.nlp(text.lower())
        entities = []

        # Extract entities
        entities.extend(self._extract_by_keywords(
            text,
            self.condition_keywords,
            "condition"
        ))

        entities.extend(self._extract_by_keywords(
            text,
            self.medication_keywords,
            "medication"
        ))

        entities.extend(self._extract_by_keywords(
            text,
            self.procedure_keywords,
            "procedure"
        ))

        return entities

    def _extract_by_keywords(
            self,
            text: str,
            keywords: List[str],
            entity_type: str
    ) -> List[Entity]:
        """Extract entities by keyword matching"""
        entities = []
        text_lower = text.lower()

        for keyword in keywords:
            start = 0
            while True:
                start = text_lower.find(keyword, start)
                if start == -1:
                    break

                end = start + len(keyword)

                # Simple confidence based on keyword specificity
                confidence = 0.7 if len(keyword) > 5 else 0.6

                entities.append(Entity(
                    text=text[start:end],
                    entity_type=entity_type,
                    start=start,
                    end=end,
                    confidence=confidence
                ))

                start = end

        return entities

# Singleton instance
_extractor = None

def get_extractor() -> ClinicalEntityExtractor:
    """Get or create extractor instance"""
    global _extractor
    if _extractor is None:
        _extractor = ClinicalEntityExtractor()
    return _extractor