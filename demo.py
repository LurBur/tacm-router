"""Demo script for Siphon MVP - complete pipeline example."""

import json
from engine.siphon_engine import SiphonEngine
from app.logger import get_logger, configure_logging
from app.utils import extract_metrics

# Configure logging
configure_logging()
logger = get_logger(__name__)


sample = """
Look the Siphon app literally is just a bunch of actions for LLMs to post to socials plus the core prompt.
Can I make it triadic? The model should know when to shift gears.
Signal extracts the idea, Shape turns it into posts, Strike picks the platform and CTA.
I want to validate this as an MVP before building the full app.
The beta offer is $19 to turn one sanitized AI chat into 10 posts.
"""


def main():
    """Run Siphon demo."""
    logger.info("🚀 Starting Siphon MVP Demo")
    
    try:
        # Initialize engine
        engine = SiphonEngine()
        logger.info("✓ Engine initialized")
        
        # Run full pipeline
        logger.info("📍 Running full pipeline: Signal → Shape → Strike")
        result = engine.run(
            sample,
            preferred_platforms=["X", "Reddit"],
            goal="attention, feedback, leads, or sales",
        )
        logger.info("✓ Pipeline completed successfully")
        
        # Extract and display metrics
        metrics = extract_metrics(result)
        logger.info(f"📊 Pipeline Metrics: {json.dumps(metrics, indent=2)}")
        
        # Display markdown pack
        print("\n" + "=" * 80)
        print("SIPHON CONTENT PACK")
        print("=" * 80 + "\n")
        print(result["markdown_pack"])
        print("\n" + "=" * 80)
        
        # Display score recommendation
        score = result["score"]
        logger.info(f"🎯 Current Status: {score['current_mode']}")
        logger.info(f"💡 Recommendation: {score['recommended']}")
        logger.info(f"   Reason: {score['reason']}")
        
        # Display action items
        logger.info("📋 Next Steps:")
        for action_name, action_url in result["actions"].items():
            logger.info(f"   - {action_name}: {action_url}")
        
        logger.info("✅ Demo completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Demo failed: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
