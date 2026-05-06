from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from app.config import settings


class SiphonInput(BaseModel):
    """Input schema for Siphon processing pipeline.
    
    Attributes:
        raw_text: Raw AI chat, notes, or transcript to process
        preferred_platforms: Optional list of preferred platforms for content
        tone: Content tone/voice style
        goal: Campaign goal/objective
    """
    raw_text: str = Field(
        ...,
        min_length=settings.MIN_INPUT_LENGTH,
        max_length=settings.MAX_INPUT_LENGTH,
        description="Raw AI chat, notes, or transcript (20-50000 characters)",
        example="Our AI chat about building distribution strategies..."
    )
    preferred_platforms: Optional[List[str]] = Field(
        default=None,
        description="Preferred platforms for content generation",
        example=["X", "LinkedIn"]
    )
    tone: str = Field(
        default="direct, intelligent, founder-building-in-public",
        description="Content tone and voice style",
        example="direct, intelligent, founder-building-in-public"
    )
    goal: str = Field(
        default="attention, feedback, leads, or sales",
        description="Campaign goal/objective",
        example="attention, feedback, leads, or sales"
    )
    
    @field_validator("preferred_platforms")
    def validate_platforms(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate that all platforms are supported."""
        if v is None:
            return v
        
        invalid_platforms = set(v) - set(settings.VALID_PLATFORMS)
        if invalid_platforms:
            raise ValueError(
                f"Invalid platforms: {invalid_platforms}. "
                f"Valid platforms: {settings.VALID_PLATFORMS}"
            )
        return v
    
    @field_validator("tone")
    def validate_tone(cls, v: str) -> str:
        """Validate tone is in allowed list."""
        if v not in settings.VALID_TONES:
            raise ValueError(
                f"Invalid tone: {v}. Valid tones: {settings.VALID_TONES}"
            )
        return v
    
    @field_validator("goal")
    def validate_goal(cls, v: str) -> str:
        """Validate goal is in allowed list."""
        if v not in settings.VALID_GOALS:
            raise ValueError(
                f"Invalid goal: {v}. Valid goals: {settings.VALID_GOALS}"
            )
        return v


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str
    app: str
    version: str
    debug: bool


class ErrorResponse(BaseModel):
    """Standardized error response schema."""
    error: str
    error_code: str
    status_code: int
    request_id: Optional[str] = None
    context: Optional[dict] = None
