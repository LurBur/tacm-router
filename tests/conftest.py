"""Shared pytest configuration and fixtures."""

import pytest


@pytest.fixture(scope="session")
def sample_content():
    """Sample content for testing."""
    return {
        "short": "A" * 50,
        "medium": "A" * 100 + " Siphon helps founders turn AI conversations into content.",
        "long": (
            "A" * 500
            + " Siphon is a triadic content engine that turns raw AI conversations, "
            "founder notes, transcripts, and idea dumps into platform-ready content. "
            "It extracts the signal, shapes it into posts, and strikes with validation moves."
        ),
    }


@pytest.fixture(scope="session")
def valid_platforms():
    """List of valid platforms."""
    return ["X", "LinkedIn", "Reddit", "TikTok", "Newsletter", "Threads", "Instagram", "YouTube"]


@pytest.fixture(scope="session")
def valid_tones():
    """List of valid tones."""
    return [
        "direct, intelligent, founder-building-in-public",
        "casual, witty, storytelling",
        "technical, detailed, instructional",
        "inspirational, motivational, vision-focused",
    ]


@pytest.fixture(scope="session")
def valid_goals():
    """List of valid goals."""
    return [
        "attention, feedback, leads, or sales",
        "community, engagement, discussion",
        "authority, expertise, thought leadership",
    ]


# Configure pytest
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (deselect with '-m \"not integration\"')"
    )
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
