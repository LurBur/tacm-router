from typing import Dict


class ScoreEngine:
    def score(self, signal: Dict[str, object], shape: Dict[str, object], strike: Dict[str, object]) -> Dict[str, object]:
        signal_score = int(signal.get("signal_score", 0))
        shape_score = int(shape.get("shape_score", 0))
        strike_score = int(strike.get("strike_score", 0))

        if signal_score < 70:
            current_mode = "SIGNAL"
            recommended = "SIGNAL"
            reason = "The idea still needs stronger clarity, audience definition, or safety review."
        elif shape_score < 75:
            current_mode = "SHAPE"
            recommended = "SHAPE"
            reason = "The idea is clear enough, but the platform-ready assets need improvement."
        elif strike_score < 75:
            current_mode = "STRIKE"
            recommended = "STRIKE"
            reason = "The content exists, but the CTA, platform choice, or validation move needs tightening."
        else:
            current_mode = "READY_TO_POST"
            recommended = "PUBLISH_OR_MANUAL_OUTREACH"
            reason = "The signal, content assets, and validation move are strong enough for a public test."

        return {
            "signal_score": signal_score,
            "shape_score": shape_score,
            "strike_score": strike_score,
            "current_mode": current_mode,
            "recommended_next_mode": recommended,
            "reason": reason,
        }
