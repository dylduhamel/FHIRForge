# FHIRForge - Clinical Notes to FHIR Converter

Convert clinical notes to FHIR resources using NLP and AI.

## Overview

FHIRForge is a developer tool that transforms unstructured clinical notes into structured FHIR R4 resources. Built for healthcare software engineers who need to understand FHIR mappings, generate test data, or prototype interoperability features.

## Product Vision

**Target Users:** Healthcare software engineers and developers

**Core Value Propositions:**
1. Fast, free way to experiment with FHIR
2. Interactive learning tool for FHIR concepts
3. Generate realistic FHIR test data from natural language
4. Validate clinical documentation quality

**What Users Receive:**
- Extracted entities (conditions, medications, procedures) with confidence scores
- Valid FHIR R4 Bundle (JSON/XML)
- FHIR validation reports
- Data quality insights
- Code generation snippets (Python, JavaScript, cURL)

## Current Status

✅ **Phase 1 Complete** (Foundation & MVP)
- FastAPI application with OpenAPI docs
- Basic NLP entity extraction (conditions, medications, procedures)
- FHIR R4 resource generation (Condition, MedicationStatement, Procedure)
- Unit tests with pytest
- Docker containerization
- Poetry dependency management

## Tech Stack

### Core
- **Python 3.11** with Poetry for dependency management
- **FastAPI** - REST API framework
- **Pydantic** - Data validation

### NLP & AI
- **spaCy** - NLP pipeline framework (currently using en_core_web_sm)
- **Transformers** (Hugging Face) - Ready for BioClinicalBERT/Med-NER
- **PyTorch** - ML backend

### FHIR
- **fhir.resources** - Python FHIR R4 models
- HAPI FHIR Server (planned for storage)

### DevOps
- **Docker** & Docker Compose
- **pytest** + pytest-cov for testing
- **black**, **ruff**, **mypy** for code quality

## Project Structure

```
fhirforge/
├── src/
│   ├── api/
│   │   ├── main.py          # FastAPI application
│   │   └── models.py        # Pydantic request/response models
│   ├── nlp/
│   │   └── extractor.py     # Entity extraction logic
│   └── fhir/
│       └── generator.py     # FHIR resource generation
├── tests/
│   ├── test_api.py
│   └── test_extractor.py
├── run.py                   # Application entry point
├── pyproject.toml          # Poetry dependencies
├── Dockerfile
└── docker-compose.yml
```

## Getting Started

### Prerequisites
- Python 3.11+ (managed with pyenv)
- Poetry

### Installation

```bash
# Install dependencies
poetry install

# Download spaCy model
poetry run python -m spacy download en_core_web_sm

# Run the application
poetry run python run.py

# Or with Docker
docker-compose up --build
```

### API Usage

```bash
# Health check
curl http://localhost:8000/health

# Convert clinical note
curl -X POST http://localhost:8000/convert \
  -H "Content-Type: application/json" \
  -d '{
    "clinical_note": "Patient has diabetes and hypertension. Taking metformin and lisinopril."
  }'
```

### Run Tests

```bash
poetry run pytest tests/ -v --cov=src
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /convert` - Convert clinical note to FHIR
  - Input: `ConversionRequest` (clinical_note, optional patient_id)
  - Output: `ConversionResponse` (entities, fhir_bundle, warnings)

## Next Steps

See `ROADMAP.md` for detailed development phases and planned features.

## License

MIT (or your choice)

## Contributing

This is a portfolio/learning project. Feedback and suggestions welcome!
