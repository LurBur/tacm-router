from typing import Dict, List


class ShapeGenerator:
    def generate(self, signal: Dict[str, object], tone: str = "direct, intelligent, founder-building-in-public") -> Dict[str, object]:
        insight = str(signal["core_insight"])
        audience = str(signal["audience"])
        pain = str(signal["pain_point"])
        strongest = str(signal["strongest_sentence"])
        monetizable = str(signal["monetizable_angle"])

        hooks = [
            "Your best content might already be buried in your AI chats.",
            "The problem is not idea generation. It is extraction.",
            "Most builders are sitting on a content library they never publish.",
        ]
        ctas = [
            "Reply 'siphon' and I’ll turn one chat into 5 posts.",
            "Send one sanitized AI chat and I’ll show you what can be extracted.",
            "If your notes are better than your posting habit, this is for you.",
        ]

        posts = [
            self._post("X", "AI chats are hidden content libraries", hooks[0], f"{pain}\n\nSiphon turns raw conversations into posts, threads, and validation moves.\n\n{insight}", ctas[0], "Best for AI builders and quick feedback loops."),
            self._post("X", "Extraction beats blank-page posting", "Blank-page content creation is the wrong starting point.", f"Start from conversations where the thinking already happened.\n\nStrongest extracted signal:\n{strongest}\n\nThen shape it into posts and strike where feedback can happen.", ctas[1], "Best for compact insight and fast replies."),
            self._post("LinkedIn", "Turn conversations into market-facing assets", "A lot of useful founder thinking never becomes market-facing content.", f"{insight}\n\nFor {audience}, content is not just posting. It is a feedback loop.\n\nWorkflow:\n1. Signal: extract the strongest idea\n2. Shape: turn it into platform-native content\n3. Strike: choose the CTA, audience, and validation move\n\nPain being solved:\n{pain}", ctas[2], "Best for B2B credibility and founder positioning."),
            self._post("Reddit", "Feedback-seeking MVP post", "I’m testing a simple service and want honest feedback.", f"It is for {audience} who have useful AI chats or messy notes but do not turn them into posts.\n\nThe pain:\n{pain}\n\nThe service turns one sanitized conversation into 10 posts plus a recommended first platform and CTA.", "Would you use this if it saved you an hour of content work?", "Best for validation and objections."),
            self._post("Founder Update", "Build in public update", "Building Siphon as a manual-first MVP.", "The first version is not a giant SaaS. It is a triadic workflow:\n\nSignal: extract the insight\nShape: create the posts\nStrike: pick the best platform and CTA\n\nI’m validating whether people will pay before I build the full action layer.", "Goal: get 3 beta users before building more software.", "Best for build-in-public audiences."),
            self._post("Short Video", "AI chats into content", hooks[0], f"Scene 1: Show a messy AI chat.\nLine: Most people think this is just a conversation.\n\nScene 2: Highlight one strong insight.\nLine: Inside it is a post, a thread, a video, and maybe a customer conversation.\n\nScene 3: Show Signal -> Shape -> Strike.\nLine: Siphon extracts the signal, shapes it into content, and tells you where to strike first.\n\nPain point: {pain}", "Send one chat. Get 10 content assets.", "Best for TikTok, Reels, and Shorts."),
            self._post("X Thread", "Siphon thread", "Most AI chats die in the sidebar.", f"1/ Most AI chats die in the sidebar.\n\n2/ That is waste because the thinking already happened.\n\n3/ Core insight: {insight}\n\n4/ Pain: {pain}\n\n5/ Siphon uses Signal -> Shape -> Strike.\n\n6/ Signal extracts the strongest idea.\n\n7/ Shape turns it into platform-native posts.\n\n8/ Strike picks the CTA, audience, and validation move.\n\n9/ The goal is not content volume. The goal is traction.\n\n10/ The MVP is manual first because payment beats fantasy-roadmap dopamine.", "Reply 'siphon' if you want one chat turned into posts.", "Best for explaining the concept and generating inbound interest."),
            self._post("Newsletter", "Conversation extraction note", "This week’s useful idea: your AI chats may already contain your content strategy.", f"{insight}\n\nThe opportunity is simple:\n{monetizable}\n\nThe workflow is intentionally small. Extract the signal, shape the assets, strike with one clear validation move.", "Try reviewing one old AI chat and extracting one public post from it today.", "Best for deeper reflection and audience nurturing."),
            self._post("Contrarian Take", "Do not build the app first", "The app is not the product yet.", "The product is the repeatable result: one messy conversation becomes content that gets replies, leads, or learning.\n\nIf people will not pay for the manual version, they probably will not care about the automated version either.", "Sell the pack first. Build the software second.", "Best for founders who overbuild."),
            self._post("Offer Post", "Beta offer", "I’m testing Siphon.", "It turns your messy AI chats, founder notes, or idea dumps into platform-ready content.\n\nThe process:\nSignal: extract the strongest idea\nShape: turn it into posts/scripts/threads\nStrike: choose the platform, CTA, and validation move\n\nBeta offer:\nSend me 1 sanitized AI conversation.\nI’ll turn it into 10 usable posts for $19.\n\nNo private info. No API keys. No fake guru polish.", "Reply 'siphon' and I’ll send details.", "Best for immediate monetization."),
        ]
        return {"posts": posts, "hooks": hooks, "ctas": ctas, "shape_score": self._score_shape(posts)}

    def _post(self, platform: str, title: str, hook: str, body: str, cta: str, fit: str) -> Dict[str, str]:
        return {
            "platform": platform,
            "title": title,
            "hook": hook,
            "body": body,
            "cta": cta,
            "platform_fit": fit,
            "full_post": f"{hook}\n\n{body}\n\n{cta}".strip(),
        }

    def _score_shape(self, posts: List[Dict[str, str]]) -> int:
        score = 35 + min(len(posts), 10) * 4
        score += 10 if any(p["platform"] == "X" for p in posts) else 0
        score += 10 if any(p["platform"] == "LinkedIn" for p in posts) else 0
        score += 10 if any("Reply" in p["cta"] or "Send" in p["cta"] for p in posts) else 0
        return max(0, min(100, score))
