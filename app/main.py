from fastapi import FastAPI
from app.schemas import SiphonInput
from engine.siphon_engine import SiphonEngine

app = FastAPI(
    title="Siphon MVP",
    description="Triadic content engine: Signal -> Shape -> Strike.",
    version="0.1.0",
)

engine = SiphonEngine()


@app.get("/")
def root():
    return {
        "name": "Siphon MVP",
        "flow": "Signal -> Shape -> Strike",
        "try": ["/health", "/docs", "/siphon"],
    }


@app.get("/health")
def health():
    return {"status": "ok", "app": "Siphon MVP", "version": "0.1.0"}


@app.post("/siphon")
def siphon(payload: SiphonInput):
    return engine.run(
        raw_text=payload.raw_text,
        preferred_platforms=payload.preferred_platforms,
        tone=payload.tone,
        goal=payload.goal,
    )


@app.post("/siphon/signal")
def signal(payload: SiphonInput):
    return engine.signal_only(payload.raw_text, goal=payload.goal)


@app.post("/siphon/shape")
def shape(payload: SiphonInput):
    signal_output = engine.signal_only(payload.raw_text, goal=payload.goal)
    return engine.shape_only(signal_output, tone=payload.tone)


@app.post("/siphon/strike")
def strike(payload: SiphonInput):
    signal_output = engine.signal_only(payload.raw_text, goal=payload.goal)
    shape_output = engine.shape_only(signal_output, tone=payload.tone)
    return engine.strike_only(
        signal_output,
        shape_output,
        preferred_platforms=payload.preferred_platforms,
        goal=payload.goal,
    )
