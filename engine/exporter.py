from datetime import datetime
from typing import Dict


class ContentPackExporter:
    def render(self, signal: Dict[str, object], shape: Dict[str, object], strike: Dict[str, object], score: Dict[str, object]) -> str:
        risky = signal.get("risky_info", [])
        if risky:
            privacy_summary = "\n".join([f"- {item['label']}: {item['excerpt']} | {item['recommendation']}" for item in risky])
        else:
            privacy_summary = "No obvious risky/private info detected by the local heuristic scanner."

        posts_md = []
        for idx, post in enumerate(shape["posts"], start=1):
            posts_md.append(
                f"### Post {idx} — {post['platform']}: {post['title']}\n\n"
                f"**Hook:** {post['hook']}\n\n"
                f"{post['full_post']}\n\n"
                f"**Platform Fit:** {post['platform_fit']}"
            )

        return f"""# Siphon Content Pack

Generated: {datetime.utcnow().isoformat()}Z

## SIGNAL

**Core Insight:**  
{signal['core_insight']}

**Audience:**  
{signal['audience']}

**Tension:**  
{signal['tension']}

**Pain Point:**  
{signal['pain_point']}

**Best Angle:**  
{signal['best_angle']}

**Monetizable Angle:**  
{signal['monetizable_angle']}

**Proof or Credibility:**  
{signal['proof_or_credibility']}

**Private/Risky Info Removed or Flagged:**  
{privacy_summary}

**Strongest Single Sentence:**  
{signal['strongest_sentence']}

---

## SHAPE

{chr(10).join(posts_md)}

---

## STRIKE

**Best First Platform:**  
{strike['best_platform']}

**Best First Post:**  
{strike['best_first_post']}

**CTA:**  
{strike['cta']}

**Target Audience:**  
{strike['target_audience']}

**Likely Objection:**  
{strike['likely_objection']}

**Reply Strategy:**  
{strike['reply_strategy']}

**Success Metric:**  
{strike['success_metric']}

**Next Move Within 24 Hours:**  
{strike['next_action']}

---

## SCORES

- Signal Score: {score['signal_score']}/100
- Shape Score: {score['shape_score']}/100
- Strike Score: {score['strike_score']}/100
- Current Mode: {score['current_mode']}
- Recommended Next Mode: {score['recommended_next_mode']}
- Reason: {score['reason']}
"""
