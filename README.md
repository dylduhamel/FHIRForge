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

✅ **Phase 1.5 Complete** (Web UI)
- Streamlit web interface
- Interactive entity highlighting
- Example clinical note templates
- Tabbed results display
- FHIR bundle download
- Real-time API integration

## Tech Stack

### Core
- **Python 3.11** with Poetry for dependency management
- **FastAPI** - REST API framework
- **Streamlit** - Web UI framework
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
│   ├── fhir/
│   │   └── generator.py     # FHIR resource generation
│   └── ui/
│       └── streamlit_app.py # Streamlit web interface
├── tests/
│   ├── test_api.py
│   └── test_extractor.py
├── Dockerfile.api          # API container image
├── Dockerfile.ui           # UI container image
├── docker-compose.yml      # Multi-service orchestration
└── pyproject.toml          # Poetry dependencies
```

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Git

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/fhirforge.git
cd fhirforge

# Build and start all services
docker-compose up --build

# Access the application:
# - Web UI: http://localhost:8501
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Usage

**Web UI**

1. Navigate to http://localhost:8501
2. Select an example or paste your own clinical note
3. Click "Convert to FHIR"
4. View extracted entities with highlighting
5. Download the FHIR bundle

**API Usage**

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

### Managing Services

```bash
# Start services
docker-compose up

# Start in detached mode (background)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build
```

### Running Tests

```bash
# Run tests in container
docker-compose run --rm api pytest tests/ -v --cov=src
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
