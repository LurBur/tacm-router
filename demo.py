from engine.siphon_engine import SiphonEngine


sample = """
Look the Siphon app literally is just a bunch of actions for LLMs to post to socials plus the core prompt.
Can I make it triadic? The model should know when to shift gears.
Signal extracts the idea, Shape turns it into posts, Strike picks the platform and CTA.
I want to validate this as an MVP before building the full app.
The beta offer is $19 to turn one sanitized AI chat into 10 posts.
"""


if __name__ == "__main__":
    engine = SiphonEngine()
    result = engine.run(
        sample,
        preferred_platforms=["X", "Reddit"],
        goal="validated learning and paid beta customers",
    )
    print(result["markdown_pack"])
