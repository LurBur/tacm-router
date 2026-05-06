"""Tests for FastAPI endpoints and error handling."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns service info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == settings.API_TITLE
        assert data["version"] == settings.API_VERSION
        assert "endpoints" in data
    
    def test_health_endpoint(self, client):
        """Test health endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["app"] == settings.API_TITLE
        assert "version" in data
        assert "debug" in data
    
    def test_health_includes_request_id(self, client):
        """Test that response includes request ID header."""
        response = client.get("/health")
        assert response.status_code == 200
        assert "x-request-id" in response.headers


class TestSignalEndpoint:
    """Test signal extraction endpoint."""
    
    def test_signal_extraction_success(self, client):
        """Test successful signal extraction."""
        payload = {
            "raw_text": (
                "A" * 50 + " This is about Siphon turning conversations into content. "
                "It helps founders who struggle with idea validation."
            ),
            "goal": "attention, feedback, leads, or sales"
        }
        
        response = client.post("/siphon/signal", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        assert "core_insight" in data
        assert "signal_score" in data
        assert "risky_info" in data
    
    def test_signal_with_invalid_goal(self, client):
        """Test signal endpoint with invalid goal."""
        payload = {
            "raw_text": "A" * 50,
            "goal": "invalid goal"
        }
        
        response = client.post("/siphon/signal", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert "error_code" in data
        assert data["error_code"] == "VALIDATION_ERROR"
    
    def test_signal_with_too_short_text(self, client):
        """Test signal endpoint with text too short."""
        payload = {
            "raw_text": "short",
            "goal": "attention, feedback, leads, or sales"
        }
        
        response = client.post("/siphon/signal", json=payload)
        assert response.status_code == 422
    
    def test_signal_missing_required_field(self, client):
        """Test signal endpoint with missing required field."""
        payload = {
            "goal": "attention, feedback, leads, or sales"
        }
        
        response = client.post("/siphon/signal", json=payload)
        assert response.status_code == 422


class TestShapeEndpoint:
    """Test shape generation endpoint."""
    
    def test_shape_generation_success(self, client):
        """Test successful content shape generation."""
        payload = {
            "raw_text": (
                "A" * 50 + " This is about Siphon turning conversations into content. "
                "It helps founders who struggle with idea validation."
            ),
            "tone": "direct, intelligent, founder-building-in-public"
        }
        
        response = client.post("/siphon/shape", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        assert "posts" in data
        assert len(data["posts"]) == 10
        assert "shape_score" in data
    
    def test_shape_with_invalid_tone(self, client):
        """Test shape endpoint with invalid tone."""
        payload = {
            "raw_text": "A" * 50,
            "tone": "invalid tone"
        }
        
        response = client.post("/siphon/shape", json=payload)
        assert response.status_code == 422


class TestStrikeEndpoint:
    """Test strike planning endpoint."""
    
    def test_strike_planning_success(self, client):
        """Test successful strike planning."""
        payload = {
            "raw_text": (
                "A" * 50 + " This is about Siphon turning conversations into content. "
                "It helps founders who struggle with idea validation."
            ),
            "preferred_platforms": ["X", "LinkedIn"]
        }
        
        response = client.post("/siphon/strike", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        assert "best_platform" in data
        assert data["best_platform"] in ["X", "LinkedIn"]
        assert "strike_score" in data
    
    def test_strike_with_invalid_platforms(self, client):
        """Test strike endpoint with invalid platforms."""
        payload = {
            "raw_text": "A" * 50,
            "preferred_platforms": ["InvalidPlatform"]
        }
        
        response = client.post("/siphon/strike", json=payload)
        assert response.status_code == 422


class TestFullPipelineEndpoint:
    """Test full Siphon pipeline endpoint."""
    
    def test_full_pipeline_success(self, client):
        """Test successful full pipeline."""
        payload = {
            "raw_text": (
                "A" * 50 + " This is about Siphon turning conversations into content. "
                "It helps founders who struggle with content validation and distribution."
                "We think the market is ready for this solution."
            ),
            "preferred_platforms": ["X", "LinkedIn"],
            "tone": "direct, intelligent, founder-building-in-public",
            "goal": "attention, feedback, leads, or sales"
        }
        
        response = client.post("/siphon", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        # Verify all pipeline components
        assert "signal" in data
        assert "shape" in data
        assert "strike" in data
        assert "score" in data
        assert "markdown_pack" in data
        assert "actions" in data
        
        # Verify signal
        assert "core_insight" in data["signal"]
        assert data["signal"]["signal_score"] >= 0
        
        # Verify shape
        assert len(data["shape"]["posts"]) == 10
        assert data["shape"]["shape_score"] >= 0
        
        # Verify strike
        assert "best_platform" in data["strike"]
        assert data["strike"]["strike_score"] >= 0
        
        # Verify score
        assert "current_mode" in data["score"]
        assert data["score"]["current_mode"] in ["SIGNAL", "SHAPE", "STRIKE", "READY_TO_POST"]
        # The score object may have 'recommended' or 'recommended_next_mode' field
        assert any(key in data["score"] for key in ["recommended", "recommended_next_mode"])
    
    def test_full_pipeline_with_all_options(self, client):
        """Test full pipeline with all custom options."""
        payload = {
            "raw_text": "A" * 100,
            "preferred_platforms": ["Reddit"],
            "tone": "technical, detailed, instructional",
            "goal": "community, engagement, discussion"
        }
        
        response = client.post("/siphon", json=payload)
        assert response.status_code == 200
    
    def test_full_pipeline_with_invalid_input(self, client):
        """Test full pipeline with invalid input."""
        payload = {
            "raw_text": "short",
            "preferred_platforms": ["InvalidPlatform"]
        }
        
        response = client.post("/siphon", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert "error_code" in data


class TestErrorHandling:
    """Test error handling and responses."""
    
    def test_validation_error_response_format(self, client):
        """Test validation error response format."""
        payload = {"raw_text": "short"}
        
        response = client.post("/siphon/signal", json=payload)
        assert response.status_code == 422
        
        data = response.json()
        assert "error" in data
        assert "error_code" in data
        assert "status_code" in data
        assert "request_id" in data
    
    def test_request_id_in_error_response(self, client):
        """Test request ID is included in error response."""
        payload = {"raw_text": "s"}
        
        response = client.post("/siphon", json=payload)
        assert response.status_code == 422
        
        data = response.json()
        assert "request_id" in data
        assert len(data["request_id"]) > 0
    
    def test_404_not_found(self, client):
        """Test 404 response for non-existent endpoint."""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_request_timing_header(self, client):
        """Test that response includes request timing header."""
        payload = {"raw_text": "A" * 50}
        
        response = client.post("/siphon/signal", json=payload)
        assert response.status_code == 200
        assert "x-process-time" in response.headers
        
        # Verify it's a float
        try:
            float(response.headers["x-process-time"])
        except ValueError:
            pytest.fail("x-process-time header is not a valid float")


class TestEndpointDocumentation:
    """Test endpoint documentation and OpenAPI."""
    
    def test_openapi_schema_available(self, client):
        """Test OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "openapi" in data
        assert "paths" in data
        assert "components" in data
    
    def test_swagger_docs_available(self, client):
        """Test Swagger documentation is available."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
