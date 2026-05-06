"""FastAPI application with error handling, logging, and request tracking."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import settings
from app.schemas import SiphonInput, HealthResponse, ErrorResponse
from app.middleware import RequestIdMiddleware, TimingMiddleware
from app.exceptions import SiphonException, ProcessingException
from app.logger import get_logger, configure_logging
from engine.siphon_engine import SiphonEngine

# Configure logging
configure_logging()
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# Add middleware
app.add_middleware(TimingMiddleware)
app.add_middleware(RequestIdMiddleware)

# Initialize engine
engine = SiphonEngine()


# Exception handlers
@app.exception_handler(SiphonException)
async def siphon_exception_handler(request: Request, exc: SiphonException):
    """Handle Siphon custom exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        f"Siphon error: {exc.detail} (code: {exc.error_code})",
        extra={"request_id": request_id}
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "error_code": exc.error_code,
            "status_code": exc.status_code,
            "request_id": request_id,
            "context": exc.context,
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(
        f"Validation error: {str(exc)}",
        extra={"request_id": request_id}
    )
    # Convert errors to serializable format
    error_details = []
    for error in exc.errors():
        error_details.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Input validation failed",
            "error_code": "VALIDATION_ERROR",
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "request_id": request_id,
            "details": error_details,
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        f"Unexpected error: {str(exc)}",
        extra={"request_id": request_id},
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error. Please try again later.",
            "error_code": "INTERNAL_ERROR",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "request_id": request_id,
        }
    )


# Routes
@app.get(
    "/",
    summary="Service Information",
    tags=["Info"]
)
def root():
    """Get service information and available endpoints."""
    logger.debug("Root endpoint accessed")
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "flow": "Signal → Shape → Strike",
        "beta_price": "$19",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "full_pipeline": "/siphon",
            "signal_only": "/siphon/signal",
            "shape_only": "/siphon/shape",
            "strike_only": "/siphon/strike",
        }
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    tags=["Health"]
)
def health() -> HealthResponse:
    """Check if service is healthy and ready to process requests."""
    logger.debug("Health check")
    return HealthResponse(
        status="ok",
        app=settings.API_TITLE,
        version=settings.API_VERSION,
        debug=settings.DEBUG,
    )


@app.post(
    "/siphon",
    summary="Full Pipeline: Signal → Shape → Strike",
    tags=["Pipeline"]
)
def siphon(request: Request, payload: SiphonInput):
    """Process raw text through full Siphon pipeline.
    
    1. **Signal**: Extract core message and insights
    2. **Shape**: Generate platform-ready content (10 variations)
    3. **Strike**: Select optimal platform and CTA
    
    Returns complete content pack with scoring and recommendations.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(
        f"Starting full siphon pipeline ({len(payload.raw_text)} chars)",
        extra={"request_id": request_id}
    )
    
    try:
        result = engine.run(
            raw_text=payload.raw_text,
            preferred_platforms=payload.preferred_platforms,
            tone=payload.tone,
            goal=payload.goal,
        )
        logger.info(
            "Full pipeline completed successfully",
            extra={"request_id": request_id}
        )
        return result
    except Exception as e:
        logger.error(
            f"Pipeline failed at full run: {str(e)}",
            extra={"request_id": request_id},
            exc_info=True
        )
        raise ProcessingException(
            detail=f"Pipeline processing failed: {str(e)}",
            stage="full_run"
        )


@app.post(
    "/siphon/signal",
    summary="Signal Extraction Only",
    tags=["Pipeline"]
)
def signal(request: Request, payload: SiphonInput):
    """Extract signal (core insight) from raw text.
    
    Returns core message, themes, audience, pain point, and monetizable angle.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(
        f"Starting signal extraction ({len(payload.raw_text)} chars)",
        extra={"request_id": request_id}
    )
    
    try:
        result = engine.signal_only(payload.raw_text, goal=payload.goal)
        logger.info(
            "Signal extraction completed",
            extra={"request_id": request_id}
        )
        return result
    except Exception as e:
        logger.error(
            f"Signal extraction failed: {str(e)}",
            extra={"request_id": request_id},
            exc_info=True
        )
        raise ProcessingException(
            detail=f"Signal extraction failed: {str(e)}",
            stage="signal"
        )


@app.post(
    "/siphon/shape",
    summary="Content Shaping Only",
    tags=["Pipeline"]
)
def shape(request: Request, payload: SiphonInput):
    """Generate platform-ready content variations from signal.
    
    Requires raw text to extract signal first, then shapes into 10 posts.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(
        f"Starting content shaping ({len(payload.raw_text)} chars)",
        extra={"request_id": request_id}
    )
    
    try:
        signal_output = engine.signal_only(payload.raw_text, goal=payload.goal)
        result = engine.shape_only(signal_output, tone=payload.tone)
        logger.info(
            f"Content shaping completed (generated {len(result.get('posts', []))} posts)",
            extra={"request_id": request_id}
        )
        return result
    except Exception as e:
        logger.error(
            f"Content shaping failed: {str(e)}",
            extra={"request_id": request_id},
            exc_info=True
        )
        raise ProcessingException(
            detail=f"Content shaping failed: {str(e)}",
            stage="shape"
        )


@app.post(
    "/siphon/strike",
    summary="Platform Selection & CTA Planning Only",
    tags=["Pipeline"]
)
def strike(request: Request, payload: SiphonInput):
    """Select optimal platform and plan validation strategy.
    
    Requires raw text to extract signal and shape first, then plans strike.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(
        f"Starting strike planning ({len(payload.raw_text)} chars)",
        extra={"request_id": request_id}
    )
    
    try:
        signal_output = engine.signal_only(payload.raw_text, goal=payload.goal)
        shape_output = engine.shape_only(signal_output, tone=payload.tone)
        result = engine.strike_only(
            signal_output,
            shape_output,
            preferred_platforms=payload.preferred_platforms,
            goal=payload.goal,
        )
        logger.info(
            f"Strike planning completed (selected platform: {result.get('best_platform')})",
            extra={"request_id": request_id}
        )
        return result
    except Exception as e:
        logger.error(
            f"Strike planning failed: {str(e)}",
            extra={"request_id": request_id},
            exc_info=True
        )
        raise ProcessingException(
            detail=f"Strike planning failed: {str(e)}",
            stage="strike"
        )


# Startup/shutdown events
@app.on_event("startup")
async def startup_event():
    """Log application startup."""
    logger.info(
        f"🚀 Siphon MVP v{settings.API_VERSION} starting (Debug: {settings.DEBUG})"
    )


@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown."""
    logger.info("🛑 Siphon MVP shutting down")
