from typing import List, Optional
from pydantic import BaseModel, Field


class SiphonInput(BaseModel):
    raw_text: str = Field(..., min_length=20)
    preferred_platforms: Optional[List[str]] = None
    tone: str = "direct, intelligent, founder-building-in-public"
    goal: str = "attention, feedback, leads, or sales"
