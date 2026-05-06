from engine.siphon_engine import SiphonEngine


def test_siphon_engine_returns_content_pack():
    text = "Siphon turns AI chats into posts for founders. The beta offer is $19 for 10 posts."
    result = SiphonEngine().run(text, preferred_platforms=["X"])
    assert result["signal"]["core_insight"]
    assert len(result["shape"]["posts"]) == 10
    assert result["strike"]["best_platform"]
    assert "Siphon Content Pack" in result["markdown_pack"]
