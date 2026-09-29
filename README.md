# LegalEase — AI-Powered Legal Document Generator

Complete Streamlit + FastAPI + Gemini project based on the supplied LegalEase documentation.

## Features
- Employment contracts, NDAs, lease agreements, freelance contracts, offer letters and custom document types
- FastAPI POST `/generate` endpoint
- Gemini AI integration through the current `google-genai` SDK
- Editable Streamlit preview
- TXT, DOCX and PDF export
- Logo and footer in DOCX/PDF
- Demo mode when `GEMINI_API_KEY` is empty
- API validation and automated tests

## Setup on Windows
Use Python 3.12 for the easiest dependency setup.

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `GEMINI_API_KEY` when you want real Gemini generation.

Terminal 1:
```powershell
python -m uvicorn backend.main:app --reload --port 8000
```

Terminal 2:
```powershell
streamlit run frontend/app.py
```

Run tests:
```powershell
pytest -q
```

## Notes
The supplied specification names Gemini 1.5 Pro and the older `google-generativeai` package. This implementation uses Google's current `google-genai` SDK and a configurable current Gemini model instead of relying on that legacy integration.

LegalEase produces AI-assisted drafts and is not a substitute for legal advice or professional review.
