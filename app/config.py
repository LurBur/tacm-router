"""Configuration management for Siphon MVP service."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Service configuration loaded from environment variables."""
    
    # API Configuration
    API_TITLE: str = "Siphon MVP"
    API_VERSION: str = "0.2.0"
    API_DESCRIPTION: str = "Triadic content engine: Signal -> Shape -> Strike"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Request Limits
    MAX_INPUT_LENGTH: int = 50000  # 50K characters max
    MIN_INPUT_LENGTH: int = 20
    REQUEST_TIMEOUT_SECONDS: int = 60
    
    # Scoring Thresholds
    SIGNAL_SCORE_THRESHOLD: int = 70
    SHAPE_SCORE_THRESHOLD: int = 75
    STRIKE_SCORE_THRESHOLD: int = 75
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 30
    
    # Validation Rules
    VALID_PLATFORMS: list = [
        "X",
        "LinkedIn",
        "Reddit",
        "TikTok",
        "Newsletter",
        "Threads",
        "Instagram",
        "YouTube",
    ]
    VALID_TONES: list = [
        "direct, intelligent, founder-building-in-public",
        "casual, witty, storytelling",
        "technical, detailed, instructional",
        "inspirational, motivational, vision-focused",
    ]
    VALID_GOALS: list = [
        "attention, feedback, leads, or sales",
        "community, engagement, discussion",
        "authority, expertise, thought leadership",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
