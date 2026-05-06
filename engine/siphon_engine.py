from typing import Optional, List, Dict

from engine.privacy_filter import PrivacyFilter
from engine.signal_extractor import SignalExtractor
from engine.shape_generator import ShapeGenerator
from engine.strike_planner import StrikePlanner
from engine.score_engine import ScoreEngine
from engine.exporter import ContentPackExporter


class SiphonEngine:
    def __init__(self):
        self.privacy_filter = PrivacyFilter()
        self.signal_extractor = SignalExtractor()
        self.shape_generator = ShapeGenerator()
        self.strike_planner = StrikePlanner()
        self.score_engine = ScoreEngine()
        self.exporter = ContentPackExporter()

    def run(
        self,
        raw_text: str,
        preferred_platforms: Optional[List[str]] = None,
        tone: str = "direct, intelligent, founder-building-in-public",
        goal: str = "attention, feedback, leads, or sales",
    ) -> Dict[str, object]:
        redacted_text = self.privacy_filter.redact(raw_text)
        risky_info = self.privacy_filter.scan(raw_text)

        signal = self.signal_extractor.extract(redacted_text, goal=goal)
        signal["risky_info"] = risky_info

        shape = self.shape_generator.generate(signal, tone=tone)
        strike = self.strike_planner.plan(signal, shape, preferred_platforms=preferred_platforms, goal=goal)
        score = self.score_engine.score(signal, shape, strike)
        markdown_pack = self.exporter.render(signal, shape, strike, score)

        actions = {
            "x_compose_url": "https://twitter.com/intent/tweet",
            "linkedin_url": "https://www.linkedin.com/feed/",
            "reddit_submit_url": "https://www.reddit.com/submit",
            "manual_delivery_instruction": "Send the markdown pack to the beta customer and ask which post they would actually publish.",
        }

        return {
            "signal": signal,
            "shape": shape,
            "strike": strike,
            "score": score,
            "markdown_pack": markdown_pack,
            "actions": actions,
        }

    def signal_only(self, raw_text: str, goal: str = "attention, feedback, leads, or sales") -> Dict[str, object]:
        redacted_text = self.privacy_filter.redact(raw_text)
        signal = self.signal_extractor.extract(redacted_text, goal=goal)
        signal["risky_info"] = self.privacy_filter.scan(raw_text)
        return signal

    def shape_only(self, signal: Dict[str, object], tone: str = "direct, intelligent, founder-building-in-public") -> Dict[str, object]:
        return self.shape_generator.generate(signal, tone=tone)

    def strike_only(self, signal: Dict[str, object], shape: Dict[str, object], preferred_platforms=None, goal: str = "attention, feedback, leads, or sales") -> Dict[str, object]:
        return self.strike_planner.plan(signal, shape, preferred_platforms=preferred_platforms, goal=goal)
