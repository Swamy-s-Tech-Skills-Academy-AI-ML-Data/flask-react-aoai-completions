# Azure OpenAI Text Generation Starter (Flask API + Vite React)

ChatGPT Clone – Python Flask + React (Vite + TypeScript) using Azure OpenAI Chat Completions.

## 🔍 Overview

This project provides:

- A Flask backend exposing `/api/` and `/api/completions` (single‑turn chat) calling Azure OpenAI.
- A React + TypeScript frontend with a simple multi‑message chat UI.
- Basic logging (text or JSON) and unit tests (pytest & Vitest + Testing Library).

## 🗂 Project Structure

```text
src/
 backendpy/
  app.py
  api/
  services/
  utils/
  requirements.txt
 frontend/
  package.json
  src/
   components/
   services/
   __tests__/  (Vitest tests)
tests/            (Python pytest tests)
```

## 🎯 45‑Minute Demo Agenda (Suggested Flow)

| Time (min) | Segment | Focus |
|-----------:|---------|-------|
| 0 – 5 | Introduction | What & why, quick architecture preview |
| 5 – 15 | Backend Tour | Flask factory, route, Azure service wrapper, logging |
| 15 – 25 | Frontend Tour | Components, state (messages), API abstraction, tests |
| 25 – 35 | Live Prompt Use Cases | Run 5 scenarios below; observe responses & logs |
| 35 – 42 | Quality & Testing | Pytest + Vitest runs, validation, mocking strategy |
| 42 – 45 | Wrap Up | Roadmap, security, Q&A |

> Tip: Keep an eye on time; if running long, compress the Frontend Tour to 5 mins and move straight to prompts.

## 🧠 Architecture (High-Level)

```text
          +------------------+             +----------------------------+
          |   React (Vite)   |  fetch JSON |   Flask API (/api/*)       |
          |  Chat Component  +-----------> | completions_routes.py      |
          |  Local Messages  |             |  Validation / Logging      |
          +---------+--------+             +--------------+-------------+
                    |                                     |
                    |                                     v
                    |                           azure_openai_service.py
                    |                            (_get_client -> Azure)
                    |                                     |
          User <----+                           Azure OpenAI Deployment
```

Highlights:

- Stateless backend (single‑turn) + frontend-held conversation history.
- Lazy Azure client creation; easy to mock in tests.
- Validation (prompt length) + consistent JSON error shape.
- Configurable logging: plain text or structured JSON.

## ⚙️ Environment Variables (Backend `.env`)

```env
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_API_KEY_V1=<your-key>        # (optional duplicate for compatibility)
AZURE_OPENAI_DEPLOYMENT_NAME=<your-deployment-name>
AZURE_OPENAI_API_VERSION=2024-05-01-preview
# Optional logging controls
LOG_LEVEL=INFO
LOG_FORMAT=json          # or 'text'
```

> Ensure the deployment name matches the name shown under “Deployments” in the Azure OpenAI portal (NOT just the model name).

## 🐍 Backend Setup & Run

```powershell
cd src/backendpy
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
python app.py   # starts on http://127.0.0.1:5009
```

Alternate (Flask CLI) if preferred:

```powershell
$env:FLASK_APP="app"
flask run --port=5009
```

## 🐍 Running Backend Tests (pytest)

Tests live in `tests/` and mock Azure OpenAI (no real API calls).

```powershell
cd <repo-root>
. .\src\backendpy\.venv\Scripts\Activate.ps1
pytest -q
```

Sample output:

```text
....  [100%]
4 passed in 0.30s
```

During demo: point out tests are fast, isolated (no network), giving rapid feedback for refactors.

## ⚛️ Frontend Setup & Run

```powershell
cd src/frontend
npm install
npm run dev   # http://localhost:5173
```

Configure a proxy or set `VITE_API_BASE_URL` (create `src/frontend/.env`):

```env
VITE_API_BASE_URL=http://127.0.0.1:5009/api
```

## ⚛️ Running Frontend Tests (Vitest + Testing Library)

```powershell
cd src/frontend
npm run test        # headless
npm run test:ui     # interactive (watch/UI if supported)
```

Sample output:

```text
✓ Chat component (2)
 ✓ renders initial assistant message
 ✓ sends a prompt and displays response

Test Files  1 passed (1)
Tests       2 passed (2)
```

Demo tip: Open `Chat.test.tsx` to show `vi.mock` usage isolating UI from network.

## 🗒 API Endpoint

`POST /api/completions`

```jsonc
Request: { "prompt": "Explain Azure OpenAI" }
Response: {
 "response": "Azure OpenAI provides...",
 "usage": { "prompt_chars": 23, "response_chars": 42 }
}
```

Errors return:

```json
{ "error": "Prompt too long. Max 4000 characters." }
```

### Future Endpoint Targets (Roadmap Talking Points)

- Streaming tokens (SSE) endpoint.
- Multi‑turn conversation with server-side context trimming.
- Moderation / safety pre-check endpoint.

## 🧪 Test Philosophy

Backend: minimal fast tests (route availability, validation, success) with a dummy client to avoid network calls.
Frontend: UI rendering & interaction for Chat component; mock API layer.

## 🪵 Logging

Configure via `LOG_LEVEL` & `LOG_FORMAT`.

- Text example: `2025-08-16 18:20:11 | INFO | Starting Chat Completions API`
- JSON example: `{ "ts": "2025-08-16T18:20:11Z", "level": "INFO", "msg": "Starting Chat Completions API" }`

Demo tips:

1. Tail the log file, send a valid prompt, then an empty one to show INFO vs ERROR lines.
2. Toggle `LOG_FORMAT=json` live (restart) to compare formats.

## 🛠 Troubleshooting 401 Errors (Azure OpenAI)

1. Endpoint form: `https://<resource>.openai.azure.com` (no extra path).
2. Deployment name must match portal deployment.
3. Key must be active (try regenerating Key 1, update `.env`, restart backend).
4. API version supported by your model.
5. Remove stray quotes or spaces around keys.

If still failing: regenerate key, verify deployment *name* (not model), ensure region matches endpoint, and confirm API version supported.

## 🚀 Next Ideas

- SSE streaming
- Multi‑turn with conversation trimming
- Rate limiting & auth
- Docker / CI pipeline

## 💬 Five Prompt Use Cases (with Intent)

| # | Intent | What To Highlight |
|---|--------|-------------------|
| 1 | Summarization | Model condenses dense technical text (One-Hot Encoding) |
| 2 | Sentiment Classification | Consistency across positive / negative / neutral samples |
| 3 | Multilingual + Translation | Story generation + Telugu → Hindi → English chain |
| 4 | Semantic Interpretation | Short phrase meaning / context inference |
| 5 | Factual Recall | Educational math concept clarity |

Use these in order (roughly 2 minutes / prompt). Keep logs visible.

### Use case 1 – Summarization

## UI First Look

![UI First Looks](./docs/images/Session2_FirstLook.PNG)

## Prompts to text in the live session

### Use case 1

```text
One-Hot Encoding is a technique used in machine learning and data preprocessing to convert categorical variables into a numerical format that algorithms can understand. Since many models cannot directly process text or categorical labels, one-hot encoding represents each category as a binary vector. For example, if you have three categories—Red, Green, and Blue—they would be represented as [1,0,0], [0,1,0], and [0,0,1] respectively. This ensures that no ordinal relationship is implied between categories, which is important because Red is not inherently greater or smaller than Blue or Green.

However, while One-Hot Encoding is simple and effective, it can lead to what is known as the “curse of dimensionality” when dealing with features that have a large number of categories. Each unique category requires its own column in the encoded dataset, which significantly increases memory usage and computational cost. For this reason, alternatives like label encoding, frequency encoding, or embedding techniques are sometimes preferred for high-cardinality features. Still, one-hot encoding remains one of the most widely used and reliable methods for handling categorical variables, especially when the number of categories is manageable.

Please summarize
```

### Use case 2

```text
This book on AI was absolutely fantastic! The explanations were clear, the examples were practical, and I walked away with a strong understanding of both the fundamentals and real-world applications. A must-read for anyone serious about AI.

Sentiment?


I was very disappointed with this AI book. The writing was confusing, the code samples didn’t work, and the content felt outdated. Honestly, it was a waste of money and time.

Sentiment?

The book provided a decent overview of AI concepts. It wasn’t too detailed, but it gave a general sense of the subject. If you’re looking for depth, you may need to consult other resources, but as an introduction, it’s okay.

Sentiment?
```

### Use case 3

```text
Tell me a story about the Sun, the Moon, the Stars, and other planets in Telugu. Translate that into Hindi and English
```

### Use case 4

```text
Way to go

What is the meaning of the above?
```

### Use case 5

```text  
What is Pythagoras' theorem?
```

## 📄 Consolidated Documentation

- Backend deep dive: `docs/backendpy.md`
- Frontend walkthrough: `docs/frontend.md`

## 🧭 Demo Script Cheat Sheet

| Step | Action | Callout |
|------|--------|---------|
| 1 | Show architecture diagram | Separation of concerns; stateless backend |
| 2 | Open `app.py` | Factory pattern, blueprint registration |
| 3 | Open `azure_openai_service.py` | Lazy client + env vars + testability |
| 4 | Run `pytest -q` | Fast isolated tests (mocked Azure) |
| 5 | Open `Chat.tsx` | Local message state; simple UX flow |
| 6 | Run `npm run test` | UI tests with Testing Library |
| 7 | Execute prompts 1–5 | Different capability categories |
| 8 | Toggle LOG_FORMAT | Plain vs JSON logs; observability angle |
| 9 | Discuss roadmap | Streaming, multi‑turn, moderation, security |

## 🔐 Security Talking Points (Brief)

- Keys never sent to frontend; server mediates Azure access.
- Future: rate limiting (Flask-Limiter), JWT / session auth, Azure Key Vault + Managed Identity.
- Add content moderation before calling completions for production safety.

## 📦 Quick Commands (Copy/Paste Convenience)

```powershell
# Backend
cd src/backendpy; if (!(Test-Path .venv)) { python -m venv .venv }; . .venv/Scripts/Activate.ps1; pip install -r requirements.txt; python app.py

# Backend tests
cd (Resolve-Path ../..); . .\src\backendpy\.venv\Scripts\Activate.ps1; pytest -q

# Frontend
cd src/frontend; npm install; npm run dev

# Frontend tests
cd src/frontend; npm run test
```

## 📜 License

See `LICENSE`.

---
*Optimized for a 45‑minute, demo-heavy session. Trim sections to reclaim time if live questions expand.*
