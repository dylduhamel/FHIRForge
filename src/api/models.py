from pydantic import BaseModel, Field
from typing import List, Optional


class ConversionRequest(BaseModel):
    """Request model for clinical note conversion"""
    clinical_note: str = Field(
        ...,
        description="The clinical note to convert to FHIR",
        min_length=10,
        examples=["Patient presented with chest pain and shortness of breath."]
    )
    patient_id: Optional[str] = Field(
        None,
        description="Optional patient identifier",
        examples=["P1234"]
    )


class Entity(BaseModel):
    """Extracted entity from clinical note"""
    text: str = Field(..., description="Extracted text")
    entity_type: str = Field(..., description="Type of entity (condition, medication, etc.)")
    start: int = Field(..., description="Start position in text")
    end: int = Field(..., description="End position in text")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class ConversionResponse(BaseModel):
    """Response model for clinical note conversion"""
    status: str
    entities: List[Entity]
    fhir_bundle: Optional[dict] = None
    warnings: List[str] = Field(default_factory=list)