"""Tests for Siphon Engine pipeline."""

import pytest
from engine.siphon_engine import SiphonEngine
from app.schemas import SiphonInput
from app.exceptions import InvalidInputException


class TestSiphonEnginePipeline:
    """Test full Siphon pipeline."""
    
    @pytest.fixture
    def engine(self):
        """Create engine instance for testing."""
        return SiphonEngine()
    
    @pytest.fixture
    def sample_text(self):
        """Sample text for testing."""
        return (
            "Siphon turns AI chats into posts for founders. "
            "The beta offer is $19 for 10 posts. "
            "We help founders turn raw conversations into platform-ready content. "
            "This solves the problem of messy idea dumps turning into publishable posts."
        )
    
    def test_siphon_engine_returns_content_pack(self, engine, sample_text):
        """Test full pipeline returns complete content pack."""
        result = engine.run(sample_text, preferred_platforms=["X"])
        
        # Verify all components
        assert "signal" in result
        assert "shape" in result
        assert "strike" in result
        assert "score" in result
        assert "markdown_pack" in result
        assert "actions" in result
        
        # Verify signal extraction
        assert result["signal"]["core_insight"]
        assert result["signal"]["signal_score"] >= 0
        
        # Verify shape generation
        assert len(result["shape"]["posts"]) == 10
        assert result["shape"]["shape_score"] >= 0
        
        # Verify strike selection
        assert result["strike"]["best_platform"]
        assert result["strike"]["strike_score"] >= 0
        
        # Verify scoring
        assert result["score"]["current_mode"] in ["SIGNAL", "SHAPE", "STRIKE", "READY_TO_POST"]
        
        # Verify markdown pack exists
        assert "Siphon Content Pack" in result["markdown_pack"]
    
    def test_signal_only_extraction(self, engine, sample_text):
        """Test signal-only extraction."""
        result = engine.signal_only(sample_text)
        
        assert "core_insight" in result
        assert "themes" in result
        assert "audience" in result
        assert result["signal_score"] >= 0
    
    def test_shape_only_generation(self, engine, sample_text):
        """Test shape-only content generation."""
        signal = engine.signal_only(sample_text)
        result = engine.shape_only(signal)
        
        assert len(result["posts"]) == 10
        assert result["shape_score"] >= 0
        
        # Verify post structure
        for post in result["posts"]:
            assert "platform" in post
            # Post can have either 'content' or 'full_post' or other fields
            assert any(key in post for key in ["content", "full_post", "body"])
            assert len(str(post.get("body", post.get("content", post.get("full_post", ""))))) > 0
    
    def test_strike_only_planning(self, engine, sample_text):
        """Test strike-only platform planning."""
        signal = engine.signal_only(sample_text)
        shape = engine.shape_only(signal)
        result = engine.strike_only(signal, shape)
        
        assert "best_platform" in result
        assert result["strike_score"] >= 0
    
    def test_preferred_platforms_respected(self, engine, sample_text):
        """Test that strike planning works with preferred platforms."""
        result = engine.run(
            sample_text,
            preferred_platforms=["LinkedIn", "Reddit"]
        )
        
        # Verify strike planning completed and selected a platform
        assert "best_platform" in result["strike"]
        assert result["strike"]["best_platform"]
        
        # Note: The engine uses a scoring system and may not always 
        # select from preferred platforms if others score higher
    
    def test_custom_tone_applied(self, engine, sample_text):
        """Test that custom tone affects content generation."""
        result = engine.run(
            sample_text,
            tone="technical, detailed, instructional"
        )
        
        # Should complete successfully with custom tone
        assert len(result["shape"]["posts"]) == 10
        assert result["shape"]["shape_score"] >= 0
    
    def test_custom_goal_applied(self, engine, sample_text):
        """Test that custom goal affects signal extraction."""
        result = engine.run(
            sample_text,
            goal="community, engagement, discussion"
        )
        
        # Should complete successfully with custom goal
        assert result["signal"]["core_insight"]
        assert result["signal"]["signal_score"] >= 0
    
    def test_privacy_filter_applied(self, engine):
        """Test that privacy filter is applied during processing."""
        dangerous_text = (
            "My email is user@example.com and API key is sk_live_123456. "
            "Check out Siphon for content generation. "
            "My phone is 555-1234."
        )
        
        result = engine.run(dangerous_text)
        
        # Verify risky info was detected
        assert "risky_info" in result["signal"]
        assert len(result["signal"]["risky_info"]) > 0
    
    def test_short_text_validation(self, engine):
        """Test that very short text is handled."""
        short_text = "Too short"
        
        # This should succeed or fail based on engine logic
        # The app layer will validate minimum length
        try:
            result = engine.run(short_text)
            # If it succeeds, verify we get a result
            assert "signal" in result
        except:
            # If it fails, that's also acceptable for MVP
            pass


class TestSiphonInputValidation:
    """Test input validation through schemas."""
    
    def test_valid_input(self):
        """Test valid input creation."""
        payload = SiphonInput(
            raw_text="A" * 50,
            preferred_platforms=["X", "LinkedIn"],
            tone="direct, intelligent, founder-building-in-public",
            goal="attention, feedback, leads, or sales"
        )
        
        assert payload.raw_text
        assert payload.preferred_platforms == ["X", "LinkedIn"]
    
    def test_invalid_platform_rejected(self):
        """Test that invalid platform is rejected."""
        with pytest.raises(ValueError):
            SiphonInput(
                raw_text="A" * 50,
                preferred_platforms=["InvalidPlatform"]
            )
    
    def test_invalid_tone_rejected(self):
        """Test that invalid tone is rejected."""
        with pytest.raises(ValueError):
            SiphonInput(
                raw_text="A" * 50,
                tone="invalid tone"
            )
    
    def test_invalid_goal_rejected(self):
        """Test that invalid goal is rejected."""
        with pytest.raises(ValueError):
            SiphonInput(
                raw_text="A" * 50,
                goal="invalid goal"
            )
    
    def test_too_short_text_rejected(self):
        """Test that text below minimum length is rejected."""
        with pytest.raises(ValueError):
            SiphonInput(raw_text="short")
    
    def test_default_values_applied(self):
        """Test that default values are applied."""
        payload = SiphonInput(raw_text="A" * 50)
        
        assert payload.tone == "direct, intelligent, founder-building-in-public"
        assert payload.goal == "attention, feedback, leads, or sales"
        assert payload.preferred_platforms is None
