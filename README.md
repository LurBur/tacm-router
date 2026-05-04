# Siphon MVP

Siphon is a triadic content engine that turns raw AI conversations, founder notes, transcripts, and idea dumps into platform-ready content.

It runs through three modes:

1. **Signal**: extract the strongest idea.
2. **Shape**: turn the idea into posts, scripts, and threads.
3. **Strike**: choose the best platform, CTA, and validation move.

## One-sentence positioning

Siphon extracts signal from your AI conversations, shapes it into platform-ready content, and helps you strike where it can create traction.

## MVP offer

Send one sanitized AI chat. Siphon turns it into 10 ready-to-post assets plus a first-post recommendation.

Beta price: **$19**.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python demo.py
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python demo.py
```

## Run API

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

- `GET /health`
- `POST /siphon`
- `POST /siphon/signal`
- `POST /siphon/shape`
- `POST /siphon/strike`

## Validation target

Get 3 beta users in 72 hours.

If no one pays, fix the offer before building more software. Very tragic, also correct.
