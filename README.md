# Siphon MVP

Siphon is a triadic content engine that turns raw AI conversations, founder notes, transcripts, and idea dumps into platform-ready content.

It runs through three modes:

1. **Signal**: extract the strongest idea.
2. **Shape**: turn the idea into posts, scripts, and threads.
3. **Strike**: choose the best platform, CTA, and validation move.

## One-sentence positioning

Siphon extracts signal from your AI conversations, shapes it into platform-ready content, and helps you strike where it can create traction.

## MVP offer

Send one sanitized AI chat. Siphon turns it into 10 ready-to-post assets plus a first-post recommendation.

Beta price: **$19**.

---

## What's New in v0.2.0

✨ **Production-Ready Improvements**

- 🛡️ **Comprehensive Error Handling** - All endpoints have try-catch with clear error messages
- 📝 **Structured Logging** - Track requests, processing stages, and errors with request IDs
- 🔍 **Request Tracking** - Each request gets a unique ID for debugging and monitoring
- ⏱️ **Performance Monitoring** - Automatic response time tracking
- ✅ **Enhanced Validation** - Input validation with better error messages
- 📊 **Expanded Test Coverage** - 30+ tests for endpoints, validation, and edge cases
- ⚙️ **Configuration Management** - Environment-based settings (`.env` support)
- 📡 **Response Format** - Standardized error responses with context
- 🚀 **Improved Demo** - Better demo output with metrics and recommendations

---

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip or conda

### Quick Start (Local)

```bash
# Clone or navigate to repository
cd tacm-router

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Create .env file for configuration
cp .env.example .env

# Run demo
python demo.py

# Run tests
pytest -v

# Run API server
uvicorn app.main:app --reload
```

Then open: `http://127.0.0.1:8000/docs`

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python demo.py
uvicorn app.main:app --reload
```

---

## API Documentation

### Base URL

```
http://localhost:8000
```

### Health Checks

#### GET `/health`
Check if service is ready.

**Response (200):**
```json
{
  "status": "ok",
  "app": "Siphon MVP",
  "version": "0.2.0",
  "debug": false
}
```

---

### Endpoints

#### POST `/siphon`
**Full pipeline: Signal → Shape → Strike**

Process text through complete Siphon pipeline (1-2 seconds).

**Request:**
```json
{
  "raw_text": "Your AI chat, notes, or transcript (20-50000 chars)...",
  "preferred_platforms": ["X", "LinkedIn"],
  "tone": "direct, intelligent, founder-building-in-public",
  "goal": "attention, feedback, leads, or sales"
}
```

**Response (200):**
```json
{
  "signal": {
    "core_insight": "...",
    "themes": ["..."],
    "audience": "...",
    "signal_score": 82
  },
  "shape": {
    "posts": [
      {"platform": "X", "content": "..."},
      ...
    ],
    "shape_score": 78
  },
  "strike": {
    "best_platform": "X",
    "cta": "...",
    "strike_score": 85
  },
  "score": {
    "current_mode": "READY_TO_POST",
    "recommended": "PUBLISH_OR_MANUAL_OUTREACH",
    "reason": "All scores above threshold"
  },
  "markdown_pack": "...",
  "actions": {...}
}
```

#### POST `/siphon/signal`
**Signal extraction only**

Extract core message and insights.

**Request:**
```json
{
  "raw_text": "Your text...",
  "goal": "attention, feedback, leads, or sales"
}
```

#### POST `/siphon/shape`
**Content shaping only**

Generate 10 platform-ready posts from raw text.

**Request:**
```json
{
  "raw_text": "Your text...",
  "tone": "direct, intelligent, founder-building-in-public"
}
```

#### POST `/siphon/strike`
**Platform selection only**

Plan validation strategy and select best platform.

**Request:**
```json
{
  "raw_text": "Your text...",
  "preferred_platforms": ["X", "LinkedIn"]
}
```

---

### Error Responses

All errors follow a standard format with request ID for tracking:

**422 Validation Error:**
```json
{
  "error": "Input validation failed",
  "error_code": "VALIDATION_ERROR",
  "status_code": 422,
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "details": [...]
}
```

**500 Processing Error:**
```json
{
  "error": "Pipeline processing failed",
  "error_code": "PROCESSING_ERROR",
  "status_code": 500,
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "context": {"stage": "signal"}
}
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
# API Configuration
DEBUG=False
LOG_LEVEL=INFO

# Request Limits
MAX_INPUT_LENGTH=50000
MIN_INPUT_LENGTH=20
REQUEST_TIMEOUT_SECONDS=60

# Scoring Thresholds
SIGNAL_SCORE_THRESHOLD=70
SHAPE_SCORE_THRESHOLD=75
STRIKE_SCORE_THRESHOLD=75

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS_PER_MINUTE=30
```

### Settings

All settings are defined in `app/config.py` and can be customized via environment variables.

---

## Logging

The service includes structured logging with request tracking:

```
2026-05-06 10:30:45 - app.main - INFO - [req-123e4567] - 📬 Incoming POST /siphon
2026-05-06 10:30:47 - app.main - INFO - [req-123e4567] - ✓ Signal extraction completed
2026-05-06 10:30:48 - app.main - INFO - [req-123e4567] - ✅ Response 200 for POST /siphon
```

Each request gets a unique ID for debugging and monitoring.

---

## Testing

Run the full test suite:

```bash
# All tests
pytest -v

# Specific test file
pytest tests/test_api_endpoints.py -v

# Specific test class
pytest tests/test_api_endpoints.py::TestHealthEndpoints -v

# Specific test
pytest tests/test_api_endpoints.py::TestHealthEndpoints::test_health_endpoint -v

# With coverage
pytest --cov=app --cov=engine -v
```

### Test Coverage

- ✅ 30+ tests for endpoints
- ✅ Input validation tests
- ✅ Error handling tests
- ✅ Edge case tests
- ✅ Full pipeline integration tests

---

## Project Structure

```
tacm-router/
├── app/                    # FastAPI application
│   ├── __init__.py
│   ├── main.py            # Route definitions & error handling
│   ├── schemas.py         # Pydantic models with validation
│   ├── config.py          # Settings & configuration
│   ├── exceptions.py      # Custom exceptions
│   ├── logger.py          # Logging setup
│   ├── middleware.py      # Request tracking middleware
│   └── utils.py           # Utility functions
├── engine/                # Core Siphon engine
│   ├── siphon_engine.py   # Main pipeline orchestrator
│   ├── privacy_filter.py  # Sensitive data redaction
│   ├── signal_extractor.py # Insight extraction
│   ├── shape_generator.py # Content generation
│   ├── strike_planner.py  # Platform selection
│   ├── score_engine.py    # Quality scoring
│   └── exporter.py        # Markdown rendering
├── tests/                 # Test suite
│   ├── conftest.py        # Shared fixtures
│   ├── test_siphon_engine.py      # Engine tests
│   └── test_api_endpoints.py      # API tests
├── demo.py               # Demo script
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
├── pytest.ini           # Pytest configuration
└── README.md            # This file
```

---

## Next Steps / Roadmap

- [ ] Rate limiting middleware
- [ ] Caching layer for repeated requests
- [ ] Async/await support for I/O operations
- [ ] Request batching for bulk processing
- [ ] Comprehensive API monitoring & metrics
- [ ] Docker support
- [ ] CI/CD pipeline
- [ ] Database integration for request history
- [ ] Authentication & API keys

---

## Troubleshooting

### Import errors when running demo
```bash
# Make sure you're in the project directory
cd tacm-router

# Make sure virtual environment is activated
source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Port 8000 already in use
```bash
# Use a different port
uvicorn app.main:app --reload --port 8001
```

### Tests failing
```bash
# Run with verbose output
pytest -vv --tb=long

# Check Python version (need 3.8+)
python --version
```

---

## License

Beta MVP - $19 per sanitized AI chat.

## Endpoints

- `GET /health`
- `POST /siphon`
- `POST /siphon/signal`
- `POST /siphon/shape`
- `POST /siphon/strike`

## Validation target

Get 3 beta users in 72 hours.

If no one pays, fix the offer before building more software. Very tragic, also correct.
