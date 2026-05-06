# Developer Quick Reference

## Architecture Overview

```
REQUEST → Middleware (RequestId, Timing) → Route Handler → Engine → Response
                                                  ↓
                                          Error Handler
                                                  ↓
                                          Standardized Error Response
```

## Adding a New API Endpoint

### Step 1: Define Input Schema
```python
# app/schemas.py
class MyInput(BaseModel):
    """My input schema."""
    text: str = Field(..., min_length=20)
    option: str = "default"
    
    @field_validator("option")
    def validate_option(cls, v: str) -> str:
        if v not in ["option1", "option2"]:
            raise ValueError(f"Invalid option: {v}")
        return v
```

### Step 2: Add Route Handler
```python
# app/main.py
@app.post("/my-endpoint", summary="Brief description", tags=["Category"])
def my_endpoint(request: Request, payload: MyInput):
    """Full description."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(f"Starting operation", extra={"request_id": request_id})
    
    try:
        result = engine.do_something(payload.text, payload.option)
        logger.info("Operation completed", extra={"request_id": request_id})
        return result
    except Exception as e:
        logger.error(f"Operation failed: {str(e)}", extra={"request_id": request_id}, exc_info=True)
        raise ProcessingException(detail=f"Failed: {str(e)}", stage="my_stage")
```

### Step 3: Add Tests
```python
# tests/test_api_endpoints.py
class TestMyEndpoint:
    def test_success(self, client):
        payload = {"text": "A" * 50, "option": "option1"}
        response = client.post("/my-endpoint", json=payload)
        assert response.status_code == 200
    
    def test_invalid_option(self, client):
        payload = {"text": "A" * 50, "option": "invalid"}
        response = client.post("/my-endpoint", json=payload)
        assert response.status_code == 422
```

---

## Logging Best Practices

### Standard Info Log
```python
logger.info(
    f"Processing started for {operation}",
    extra={"request_id": request_id}
)
```

### Error Log with Context
```python
logger.error(
    f"Failed to process: {str(e)}",
    extra={"request_id": request_id},
    exc_info=True  # Include full traceback
)
```

### Debug Log
```python
logger.debug(
    f"Internal state: {state}",
    extra={"request_id": request_id}
)
```

**Always include `request_id` in `extra` dict for tracing!**

---

## Exception Handling Patterns

### Validation Error (422)
```python
from app.exceptions import InvalidInputException

if not validate(data):
    raise InvalidInputException(
        detail="Validation failed",
        context={"field": "invalid_value"}
    )
```

### Processing Error (500)
```python
from app.exceptions import ProcessingException

try:
    result = engine.process(data)
except Exception as e:
    raise ProcessingException(
        detail=f"Engine failed: {str(e)}",
        stage="processing"
    )
```

### Rate Limit (429)
```python
from app.exceptions import RateLimitException

if requests_exceed_limit():
    raise RateLimitException(retry_after_seconds=60)
```

---

## Configuration Pattern

### In settings
```python
# app/config.py
class Settings(BaseSettings):
    MY_NEW_SETTING: str = os.getenv("MY_NEW_SETTING", "default")
    MY_THRESHOLD: int = 70
```

### In code
```python
from app.config import settings

if score < settings.MY_THRESHOLD:
    # Do something
```

### In .env
```env
MY_NEW_SETTING=custom_value
```

---

## Testing Patterns

### Basic Endpoint Test
```python
def test_endpoint_success(self, client):
    response = client.post("/endpoint", json={"field": "value"})
    assert response.status_code == 200
    data = response.json()
    assert "key" in data
```

### Error Case Test
```python
def test_endpoint_validation_error(self, client):
    response = client.post("/endpoint", json={"field": "invalid"})
    assert response.status_code == 422
    data = response.json()
    assert data["error_code"] == "VALIDATION_ERROR"
    assert "request_id" in data
```

### Using Fixtures
```python
def test_with_fixture(self, client, sample_content):
    payload = {"text": sample_content["medium"]}
    response = client.post("/endpoint", json=payload)
    assert response.status_code == 200
```

---

## Common Tasks

### Get Request ID
```python
request_id = getattr(request.state, "request_id", "unknown")
```

### Parse JSON Safely
```python
from app.utils import safe_json_dumps

try:
    json_str = safe_json_dumps(obj)
except:
    json_str = "{}"
```

### Truncate Long Strings
```python
from app.utils import truncate_string

short = truncate_string(long_text, max_length=100)
```

### Extract Metrics

```python
from app.utils import extract_metrics

metrics = extract_metrics(response)
# Returns: {
#   "signal_score": 82,
#   "shape_score": 78,
#   "strike_score": 85,
#   "overall_status": "READY_TO_POST",
#   "core_insight": "Core idea...",
#   "best_platform": "X",
#   "posts_generated": 10
# }
```

---

## Middleware Pattern

```python
from starlette.middleware.base import BaseHTTPMiddleware

class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Before request
        logger.info("Before request")
        
        response = await call_next(request)
        
        # After request
        logger.info(f"After request: {response.status_code}")
        return response

# Register in main.py
app.add_middleware(MyMiddleware)
```

---

## Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_api_endpoints.py

# Specific class
pytest tests/test_api_endpoints.py::TestHealthEndpoints

# Specific test
pytest tests/test_api_endpoints.py::TestHealthEndpoints::test_health_endpoint

# Verbose output
pytest -vv

# With coverage
pytest --cov=app --cov=engine

# Stop on first failure
pytest -x

# Show print statements
pytest -s
```

---

## Debugging Tips

### Enable Debug Logging
```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Print Request/Response
```python
logger.debug(f"Request payload: {json.dumps(payload, indent=2)}", extra={"request_id": request_id})
logger.debug(f"Response: {json.dumps(result, indent=2)}", extra={"request_id": request_id})
```

### Use Request ID
```
# Find all logs for specific request:
grep "req-abc123" *.log
```

### Run Single Test with Output
```bash
pytest tests/test_api_endpoints.py::TestHealthEndpoints::test_health_endpoint -vv -s
```

---

## Code Style Guide

### Logging Emojis (Optional but Recommended)
- 📬 Incoming request
- ✅ Success
- ❌ Error
- ⏱️ Timing
- 📊 Metrics
- 🚀 Startup
- 🛑 Shutdown
- 📍 Process stage
- 💡 Highlight

### Type Hints
```python
def my_function(text: str, count: int) -> Dict[str, Any]:
    """Description."""
    return {}
```

### Docstrings
```python
def my_function(param: str) -> str:
    """Brief description.
    
    Longer description if needed.
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
    """
    pass
```

---

## Deployment Checklist

- [ ] All tests passing (`pytest`)
- [ ] No security issues in dependencies (`pip audit`)
- [ ] Configuration documented in `.env.example`
- [ ] Logging is appropriate (not too verbose in PRODUCTION)
- [ ] Error messages don't expose sensitive data
- [ ] Rate limiting enabled in production
- [ ] Monitoring/alerting set up
- [ ] Documentation updated
- [ ] CHANGELOG.md entry added
- [ ] API_GUIDE.md examples tested

---

## Performance Tips

1. **Log Level in Production**: Use INFO or WARNING, not DEBUG
2. **Caching**: Consider caching repeated requests
3. **Async**: Use async/await for I/O operations
4. **Batch**: Support batch operations for bulk processing
5. **Timeouts**: Set reasonable timeouts on external calls

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Logging](https://docs.python.org/3/library/logging.html)

---

**Last Updated:** May 6, 2026  
**Version:** 0.2.0
