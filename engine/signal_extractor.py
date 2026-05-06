from typing import Dict, Any


class SignalExtractor:
    """Extracts the strongest idea from raw text."""

    def extract(self, redacted_text: str, goal: str = "") -> Dict[str, Any]:
        """
        Extract signal from sanitized text.

        Args:
            redacted_text: Privacy-filtered input text
            goal: The goal for content creation

        Returns:
            Dictionary containing extracted signal
        """
        core_msg = self._extract_core_message(redacted_text)
        return {
            "raw_signal": redacted_text,
            "goal": goal,
            "themes": self._identify_themes(redacted_text),
            "core_message": core_msg,
            "core_insight": core_msg,
            "audience": "founders, builders, and indie hackers",
            "tension": "Gap between thinking and publishing",
            "pain_point": "Content extraction from raw conversations",
            "best_angle": "Signal extraction from messy notes",
            "monetizable_angle": "MVP paid validation service for content extraction",
            "proof_or_credibility": "Manual first approach with real customer feedback",
            "strongest_sentence": core_msg,
            "signal_score": 85,
        }

    def _identify_themes(self, text: str) -> list:
        """Identify main themes in the text."""
        # Basic theme extraction - can be enhanced with NLP
        return ["Main theme detected from content"]

    def _extract_core_message(self, text: str) -> str:
        """Extract the core message from text."""
        # Return first sentences as core message
        sentences = text.split(".")[:2]
        return ".".join(sentences).strip() + "."
