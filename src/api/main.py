from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.api.models import ConversionRequest, ConversionResponse, Entity
from src.nlp.extractor import get_extractor
from src.fhir.generator import get_generator
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Clinical Notes to FHIR Converter",
    description="Converts Clinical Notes to FHIR resources using NLP",
    version="0.1.0"
)

class HealthResponse(BaseModel):
    status: str
    version: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return HealthResponse(status="healthy", version="0.1.0")


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "Clinical Notes to FHIR Converter API",
        "docs": "/docs",
        "health": "/health"
    }


@app.post("/convert", response_model=ConversionResponse)
async def convert(request: ConversionRequest):
    """
    Convert a clinical note to FHIR resources

    This endpoint accepts clinical note test and returns
    - Extracted entities (conditions, medications, procedures, etc.)
    - Generated FHIR bundle
    - Validation warnings
    """
    logger.info(f"Conversion request received for patient_id: {request.patient_id}")
    logger.debug(f"Clinical note length: {len(request.clinical_note)} characters")

    try:
        # Extract entities
        logger.info("Extracting entities from clinical note")
        extractor = get_extractor()
        entities = extractor.extract_entities(request.clinical_note)
        logger.info(f"Extracted {len(entities)} entities: {[(e.entity_type, e.text) for e in entities]}")

        # Generate FHIR bundle
        logger.info("Generating FHIR bundle")
        generator = get_generator(patient_id=request.patient_id or "example-patient")
        fhir_bundle = generator.generate_bundle(entities)
        logger.info("FHIR bundle generated successfully")

        warnings = []
        if not entities:
            warnings.append("No medical entities detected in the provided clinical note")

        return ConversionResponse(
            status="success",
            entities=entities,
            fhir_bundle=fhir_bundle,
            warnings=warnings
        )
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))