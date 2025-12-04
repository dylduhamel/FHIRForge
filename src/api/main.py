from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.api.models import ConversionRequest, ConversionResponse, Entity

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
    try:
        entities = [
            Entity(
                text="chest pain",
                entity_type="condition",
                start=20,
                end=30,
                confidence=0.95
            )
        ]

        return ConversionResponse(
            status="success",
            entities=entities,
            warnings=["NLP pipeline not yet implemented"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))