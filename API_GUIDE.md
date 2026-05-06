"""
Siphon MVP - Quick API Usage Guide
"""

# ============================================================================
# EXAMPLE 1: Full Pipeline (Signal → Shape → Strike)
# ============================================================================

import requests
import json

BASE_URL = "http://localhost:8000"

# Prepare input
payload = {
    "raw_text": (
        "I'm thinking about building a content distribution tool for indie hacker. "
        "The problem: founders spend hours converting AI conversations into shareable posts. "
        "The solution: Siphon extracts the core idea, shapes it into platform-ready content, "
        "and recommends the best platform to post first. "
        "We're validating this with a $19 beta offer."
    ),
    "preferred_platforms": ["X", "LinkedIn"],
    "tone": "direct, intelligent, founder-building-in-public",
    "goal": "attention, feedback, leads, or sales"
}

# Send request
response = requests.post(f"{BASE_URL}/siphon", json=payload)

# Check for errors
if response.status_code == 200:
    result = response.json()
    print("✅ Pipeline Success!")
    print(f"Best Platform: {result['strike']['best_platform']}")
    print(f"Overall Score: {result['score']['current_mode']}")
else:
    error = response.json()
    print(f"❌ Error: {error['error']}")
    print(f"   Code: {error['error_code']}")
    print(f"   Request ID: {error['request_id']}")


# ============================================================================
# EXAMPLE 2: Signal-Only Extraction
# ============================================================================

payload = {
    "raw_text": "Your AI chat here...",
    "goal": "attention, feedback, leads, or sales"
}

response = requests.post(f"{BASE_URL}/siphon/signal", json=payload)

if response.status_code == 200:
    signal = response.json()
    print(f"Core Insight: {signal['core_insight']}")
    print(f"Audience: {signal['audience']}")
    print(f"Signal Quality Score: {signal['signal_score']}/100")


# ============================================================================
# EXAMPLE 3: Content Shaping (Signal → Posts)
# ============================================================================

payload = {
    "raw_text": "Your AI chat here...",
    "tone": "direct, intelligent, founder-building-in-public"
}

response = requests.post(f"{BASE_URL}/siphon/shape", json=payload)

if response.status_code == 200:
    shape = response.json()
    print(f"Generated {len(shape['posts'])} posts:")
    for i, post in enumerate(shape['posts'], 1):
        print(f"\n{i}. {post['platform']}")
        print(f"   {post['content'][:100]}...")


# ============================================================================
# EXAMPLE 4: Strike Planning (Select Best Platform)
# ============================================================================

payload = {
    "raw_text": "Your AI chat here...",
    "preferred_platforms": ["X", "LinkedIn", "Reddit"]
}

response = requests.post(f"{BASE_URL}/siphon/strike", json=payload)

if response.status_code == 200:
    strike = response.json()
    print(f"Best Platform: {strike['best_platform']}")
    print(f"Call-to-Action: {strike['cta']}")
    print(f"Validation Metrics: {strike['validation_move']}")


# ============================================================================
# EXAMPLE 5: Error Handling
# ============================================================================

# Invalid input (text too short)
payload = {
    "raw_text": "short"  # Less than 20 characters
}

response = requests.post(f"{BASE_URL}/siphon", json=payload)

if response.status_code != 200:
    error = response.json()
    print(f"❌ Status: {error['status_code']}")
    print(f"   Error: {error['error']}")
    print(f"   Code: {error['error_code']}")
    print(f"   Request ID: {error['request_id']}")  # For debugging


# ============================================================================
# EXAMPLE 6: Valid Options
# ============================================================================

# Valid platforms
VALID_PLATFORMS = [
    "X",
    "LinkedIn",
    "Reddit", 
    "TikTok",
    "Newsletter",
    "Threads",
    "Instagram",
    "YouTube"
]

# Valid tones
VALID_TONES = [
    "direct, intelligent, founder-building-in-public",
    "casual, witty, storytelling",
    "technical, detailed, instructional",
    "inspirational, motivational, vision-focused"
]

# Valid goals
VALID_GOALS = [
    "attention, feedback, leads, or sales",
    "community, engagement, discussion",
    "authority, expertise, thought leadership"
]

# Use any combination
payload = {
    "raw_text": "Your text...",
    "preferred_platforms": ["Reddit", "TikTok"],
    "tone": "casual, witty, storytelling",
    "goal": "community, engagement, discussion"
}

response = requests.post(f"{BASE_URL}/siphon", json=payload)


# ============================================================================
# EXAMPLE 7: Response Headers
# ============================================================================

response = requests.post(f"{BASE_URL}/siphon", json=payload)

print(f"Request ID: {response.headers.get('X-Request-ID')}")
print(f"Process Time: {response.headers.get('X-Process-Time')} seconds")


# ============================================================================
# EXAMPLE 8: Python Class Wrapper
# ============================================================================

class SiphonClient:
    """Simple Python client for Siphon API."""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def full_pipeline(self, text, platforms=None, tone=None, goal=None):
        """Run full pipeline."""
        payload = {
            "raw_text": text,
            "preferred_platforms": platforms,
            "tone": tone or "direct, intelligent, founder-building-in-public",
            "goal": goal or "attention, feedback, leads, or sales"
        }
        response = requests.post(f"{self.base_url}/siphon", json=payload)
        return response.json() if response.status_code == 200 else None
    
    def signal_only(self, text, goal=None):
        """Extract signal only."""
        payload = {
            "raw_text": text,
            "goal": goal or "attention, feedback, leads, or sales"
        }
        response = requests.post(f"{self.base_url}/siphon/signal", json=payload)
        return response.json() if response.status_code == 200 else None
    
    def health(self):
        """Check if service is healthy."""
        response = requests.get(f"{self.base_url}/health")
        return response.json() if response.status_code == 200 else None


# Usage
client = SiphonClient()

# Check health
print(client.health())

# Run pipeline
result = client.full_pipeline(
    "Your AI chat here...",
    platforms=["X", "LinkedIn"],
    tone="direct, intelligent, founder-building-in-public",
    goal="attention, feedback, leads, or sales"
)

if result:
    print(result["markdown_pack"])
