from typing import Dict, List


class StrikePlanner:
    PLATFORM_PRIORITY = {
        "X": 95,
        "Reddit": 90,
        "LinkedIn": 85,
        "Founder Update": 80,
        "Short Video": 70,
        "Newsletter": 65,
        "X Thread": 88,
        "Offer Post": 92,
        "Contrarian Take": 82,
    }

    def plan(self, signal: Dict[str, object], shape: Dict[str, object], preferred_platforms=None, goal: str = "attention, feedback, leads, or sales") -> Dict[str, object]:
        posts: List[Dict[str, str]] = shape.get("posts", [])
        preferred_platforms = preferred_platforms or []
        best = self._select_best_post(posts, preferred_platforms) if posts else {"platform": "X", "full_post": "Sample post", "cta": "Reply with feedback"}

        return {
            "best_platform": best["platform"],
            "best_first_post": best["full_post"],
            "cta": best["cta"],
            "target_audience": signal["audience"],
            "likely_objection": "People may think this is just another AI content generator unless the Signal -> Shape -> Strike workflow is clearly shown.",
            "reply_strategy": "Reply to every interested person with a simple intake request: send one sanitized chat, remove private details, and receive 10 posts plus a first-post recommendation.",
            "success_metric": "Within 24 hours, aim for 3 replies, 1 submitted chat, or 1 paid beta order. Views without replies do not count as validation.",
            "next_action": "Post the beta offer, then DM 20 AI builders, indie hackers, consultants, or creators who already discuss their work publicly.",
            "strike_score": self._score_strike(best, signal, goal),
        }

    def _select_best_post(self, posts: List[Dict[str, str]], preferred_platforms: List[str]) -> Dict[str, str]:
        def score(post):
            base = self.PLATFORM_PRIORITY.get(post["platform"], 50)
            if post["platform"] in preferred_platforms:
                base += 15
            if "Reply" in post["cta"] or "Send" in post["cta"]:
                base += 10
            if "$19" in post["full_post"]:
                base += 8
            return base

        return max(posts, key=score)

    def _score_strike(self, best: Dict[str, str], signal: Dict[str, object], goal: str) -> int:
        score = 40
        score += 15 if best["cta"] else 0
        score += 15 if "reply" in best["cta"].lower() or "send" in best["cta"].lower() else 0
        score += 15 if "pay" in str(signal["monetizable_angle"]).lower() or "$" in best["full_post"] else 8
        score += 10 if any(w in goal.lower() for w in ["feedback", "sales", "leads", "paid"] ) else 5
        score += 10 if len(best["full_post"]) > 100 else 0
        return max(0, min(100, score))
