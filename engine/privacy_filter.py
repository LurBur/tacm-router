import re
from typing import List, Dict


class PrivacyFilter:
    EMAIL = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
    API_KEY = re.compile(r"\b(sk-[A-Za-z0-9_-]{16,}|AIza[0-9A-Za-z\-_]{20,}|ghp_[A-Za-z0-9_]{20,})\b")
    PHONE = re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")
    TOKEN = re.compile(r"(token|secret|password|passwd|api_key|apikey|access_key)\s*[:=]\s*['\"]?[^'\"\s]+", re.I)

    RISK_TERMS = [
        "password", "api key", "secret key", "client name", "confidential",
        "private user data", "ssn", "social security", "lawsuit", "court order",
        "bank account", "routing number", "credit card",
    ]

    def scan(self, text: str) -> List[Dict[str, str]]:
        findings = []
        for label, pattern in [
            ("email", self.EMAIL),
            ("api_key", self.API_KEY),
            ("phone", self.PHONE),
            ("credential_or_token", self.TOKEN),
        ]:
            for match in pattern.finditer(text):
                findings.append({
                    "label": label,
                    "excerpt": self._mask(match.group(0)),
                    "recommendation": "Remove or redact before publishing.",
                })

        lower = text.lower()
        for term in self.RISK_TERMS:
            if term in lower:
                findings.append({
                    "label": "risk_term",
                    "excerpt": term,
                    "recommendation": "Review manually before publishing.",
                })
        return findings

    def redact(self, text: str) -> str:
        text = self.EMAIL.sub("[REDACTED_EMAIL]", text)
        text = self.API_KEY.sub("[REDACTED_API_KEY]", text)
        text = self.PHONE.sub("[REDACTED_PHONE]", text)
        text = self.TOKEN.sub("[REDACTED_CREDENTIAL]", text)
        return text

    def _mask(self, value: str) -> str:
        if len(value) <= 8:
            return "[REDACTED]"
        return value[:3] + "..." + value[-3:]
