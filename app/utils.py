"""Utility functions for Siphon MVP service."""

import json
from typing import Any, Dict, Optional


def safe_json_dumps(obj: Any, indent: int = 2) -> str:
    """Safely convert object to JSON string.
    
    Args:
        obj: Object to serialize
        indent: JSON indentation level
        
    Returns:
        JSON string or error message
    """
    try:
        return json.dumps(obj, indent=indent, default=str)
    except Exception as e:
        return json.dumps({"error": f"Serialization failed: {str(e)}"})


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate string to max length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_metrics(response: Dict[str, Any]) -> Dict[str, Any]:
    """Extract key metrics from pipeline response.
    
    Args:
        response: Full pipeline response
        
    Returns:
        Dictionary with extracted metrics
    """
    metrics = {}
    
    if "score" in response:
        score = response["score"]
        metrics["signal_score"] = score.get("signal_score", 0)
        metrics["shape_score"] = score.get("shape_score", 0)
        metrics["strike_score"] = score.get("strike_score", 0)
        metrics["overall_status"] = score.get("current_mode", "unknown")
    
    if "signal" in response:
        metrics["core_insight"] = truncate_string(
            response["signal"].get("core_insight", "")
        )
    
    if "strike" in response:
        metrics["best_platform"] = response["strike"].get("best_platform", "unknown")
    
    if "shape" in response:
        metrics["posts_generated"] = len(response["shape"].get("posts", []))
    
    return metrics
