# Azure OpenAI Text Generation Starter (Flask API + Vite React)

ChatGPT Clone – Python Flask + React (Vite + TypeScript) using Azure OpenAI Chat Completions.

## 🔍 Overview

This project provides:

- A Flask backend exposing:
  - `GET /` and `GET /api/` (welcome JSON)
  - `POST /api/completions` (single‑turn chat completion)
  - `GET /api/health/config` (non‑secret config + source: env / file)
- A React + TypeScript frontend with a simple multi‑message chat UI.
- Structured logging (plain text or JSON) with request correlation IDs & latency.
- Unified JSON error handling (404 / HTTPException / generic 500) + masked internal errors.
- Fast isolated tests (pytest) without `pytest-flask`; Azure calls fully mocked.

## 🗂 Project Structure

```text
src/
 backend/
  app.py
  api/
  services/
  utils/
  requirements.txt
 frontend/
  src/
   components/
## 🔹 Installation & Setup
python --version

pip install virtualenv
pip install flask-cors
pip freeze > requirements.txt
```

Optional (version pinning): A `.python-version` file at repo root specifies the recommended interpreter (used by `pyenv` / some IDEs) – currently `3.13.5`.

```mermaid
%%{init: { 'flowchart': { 'useMaxWidth': true, 'htmlLabels': true } }}%%
flowchart LR
pip --version

  direction TB
pip install virtualenv
python -m venv .venv
. .venv/Scripts/Activate.ps1   # PowerShell activation (Windows)
python -m pip install --upgrade pip

pip install -r requirements.txt  # Preferred (already committed)
# OR initial manual install (when bootstrapping):
  direction TB
# pip install Flask python-dotenv openai flask-cors
# pip freeze > requirements.txt
```

Interpreter versioning: For consistent environments, add a `.python-version` file at the repo root (recommended for pyenv/IDE integration). Example content:

```text
3.13.5
```

### Check installed Python versions (Windows)

Use the Python launcher to list all installed Python versions it recognizes:

```powershell

### Architecture (columns)

| Frontend | Backend | Platform |
|---|---|---|
| Vite + React (TypeScript) UI<br/>`Chat.tsx`, components | Flask API (`/api/*`)<br/>Blueprints: `home_routes`, `completions_routes` | Azure OpenAI Deployment |
| API client<br/>`src/frontend/src/services/api.ts` | Service layer<br/>`services/azure_openai_service.py` | — |
| Local message state | Utilities<br/>`utils/env_config.py`, `utils/logging_config.py` | — |
| Dev proxy (optional) in `vite.config.ts` | Diagnostics<br/>`GET /api/config/info` | — |
py -0
```

To include install paths as well:

```powershell
py -0p
```

## ⚙️ Environment Loading Precedence

Each configuration key resolves in this order:

1. Exported OS / process environment variable
2. First `.env` discovered walking upward from `src/backend/utils/env_config.py` to repo root
3. Absent (null)

Inspect non‑secret effective values & their source at `GET /api/health/config`. Secrets are never returned.

## 🔹 To install dependencies later

```bash
pip install -r requirements.txt
```

## 🎯 45‑Minute Demo Agenda (Suggested Flow)

| Time (min) | Segment | Focus |
|-----------:|---------|-------|
| 0 – 5 | Introduction | What & why, quick architecture preview |
| 5 – 20 | Backend Tour | Flask factory, route, Azure service wrapper, logging |
| 20 – 30 | Frontend Tour | Components, state (messages), API abstraction, tests |
| 30 – 40 | Live Prompt Use Cases | Run 5 scenarios below; observe responses & logs |
| 40 – 45 | Wrap Up | Roadmap, security, Q&A |

> Tip: Keep an eye on time; if running long, compress the Frontend Tour to 5 mins and move straight to prompts.

## 🧠 Architecture (High-Level)

```mermaid
flowchart LR
  %% Frontend
  subgraph Frontend
    direction TB
    UI["Chat.tsx + components"]
    APIClient["services/api.ts"]
    UI --> APIClient
  end

  %% Backend
  subgraph Backend
    direction TB
    Gateway["/api/*"]
    Routes["Blueprints: home_routes, completions_routes"]
    Service["services/azure_openai_service.py"]
    Utils["utils: env_config, logging_config"]
    Gateway --> Routes --> Service
    Utils -. "config & logging" .- Gateway
    Utils -. "config & logging" .- Routes
  end

  Browser["User Browser"] --> UI
  APIClient -- "fetch JSON" --> Gateway
  Service --> Azure["Azure OpenAI Deployment"]
  Gateway -. diagnostics .- ConfigInfo["GET /api/config/info"]
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
cd src/backend
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

Tests live in `tests/` and mock Azure OpenAI (no real API calls). We **do not** use `pytest-flask` (avoids dependency on deprecated Flask 2.x internals). Fixtures explicitly build the app + test client.

```powershell
cd <repo-root>
. .\src\backend\.venv\Scripts\Activate.ps1
pytest -q
```

Sample (current) output:

```text
......  [100%]
6 passed in 0.xx s
```

Covered:

1. Root & `/api/` welcome routes
2. Completions validation (missing prompt)
3. Completions success (mocked Azure)
4. 404 JSON handler
5. Generic exception path returns masked message
6. Usage object structure

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

## 🌐 CORS: Connecting Frontend and Backend

The backend enables CORS via Flask-CORS so the Vite dev server (<http://localhost:5173>) can call the API (<http://127.0.0.1:5009>).

### Option A — Keep CORS open for local dev (already enabled)

`src/backend/app.py` calls `CORS(app)` which allows requests from any origin in development. To restrict to your dev UI origin, tighten it like this:

```python
# src/backend/app.py
from flask_cors import CORS

CORS(app,
     resources={r"/api/*": {"origins": [
         "http://localhost:5173",
         "http://127.0.0.1:5173"
     ]}},
     supports_credentials=True)
```

If you enable `supports_credentials=True`, include credentials on the client when needed:

```ts
// src/frontend/src/services/api.ts (example)
fetch(`${baseUrl}/completions`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ prompt }),
  credentials: 'include', // only if you rely on cookies/auth
})
```

### Option B — Use the Vite dev proxy (avoids CORS during dev)

Proxy all `/api` calls from the Vite server to the Flask backend to keep everything same-origin in dev:

```ts
// src/frontend/vite.config.ts
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5009',
        changeOrigin: true,
      },
    },
  },
})
```

Then call relative paths from the frontend (no base URL needed):

```ts
await fetch('/api/completions', { /* ... */ })
```

### Common CORS errors and fixes

- “CORS Missing Allow Origin”: Ensure the backend sets `Access-Control-Allow-Origin` to your UI origin (or `*` for dev).
- Preflight (OPTIONS) blocked: Make sure Flask-CORS is installed and applied to your routes; avoid custom blocks on `OPTIONS`.
- Credentials rejected: Use `supports_credentials=True` and `credentials: 'include'` in fetch. Avoid wildcard `*` with credentials.

See MDN’s CORS error guide for detailed cases and fixes:
<https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS/Errors>

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

## 🗒 Key API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | / | Root welcome JSON |
| GET | /api/ | API namespace welcome |
| GET | /api/health/config | Non‑secret config values + source |
| POST | /api/completions | Single‑turn chat completion |

Example request:

```json
{ "prompt": "Explain Azure OpenAI" }
```

Example success response:

```json
{ "response": "...", "usage": { "prompt_chars": 23, "response_chars": 42 } }
```

Example validation error:

```json
{ "error": "'prompt' is required" }
```

### Future Endpoint Targets (Roadmap Talking Points)

- Streaming tokens (SSE) endpoint.
- Multi‑turn conversation with server-side context trimming.
- Moderation / safety pre-check endpoint.

## 🧪 Test Philosophy

Backend: minimal fast tests (routes, validation, success, error handlers) with a dummy Azure client (no network).
Frontend: UI rendering & interaction for Chat component; mock API layer.

## 🪵 Logging

Configure via `LOG_LEVEL` & `LOG_FORMAT`.

- Text example: `2025-08-16 18:20:11 | INFO | Starting Chat Completions API`
- JSON example: `{ "ts": "2025-08-16T18:20:11Z", "level": "INFO", "msg": "Starting Chat Completions API" }`
  - Request logs also include: `correlation_id`, `path`, `method`, `latency_ms`.

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

- Backend deep dive: `docs/backend.md`
- Frontend walkthrough: `docs/frontend.md`

## 🧭 Demo Script Cheat Sheet

| Step | Action | Callout |
|------|--------|---------|
| 1 | Show architecture diagram | Separation of concerns; stateless backend |
| 2 | Open `app.py` | Factory pattern, blueprint registration |
| 3 | Open `azure_openai_service.py` | Lazy client + env vars + testability |
| 4 | Run `pytest -q` | Fast isolated tests (mocked Azure, 6 passing) |
| 5 | Open `Chat.tsx` | Local message state; simple UX flow |
| 6 | Run `npm run test` | UI tests with Testing Library |
| 7 | Execute prompts 1–5 | Different capability categories |
| 8 | Toggle LOG_FORMAT | Plain vs JSON logs; correlation & latency |
| 9 | Discuss roadmap | Streaming, multi‑turn, moderation, security |

## 🔐 Security Talking Points (Brief)

- Keys never sent to frontend; server mediates Azure access.
- Future: rate limiting (Flask-Limiter), JWT / session auth, Azure Key Vault + Managed Identity.
- Add content moderation before calling completions for production safety.

## 📦 Quick Commands (Copy/Paste Convenience)

```powershell
# Backend
cd src/backend; if (!(Test-Path .venv)) { python -m venv .venv }; . .venv/Scripts/Activate.ps1; pip install -r requirements.txt; python app.py

# Backend tests
cd (Resolve-Path ../..); . .\src\backend\.venv\Scripts\Activate.ps1; pytest -q

# Frontend
cd src/frontend; npm install; npm run dev

# Frontend tests
cd src/frontend; npm run test
```

```powershell
# Backend
cd src/backend
if (!(Test-Path .venv)) { python -m venv .venv }
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
python app.py

# Backend tests
cd (Resolve-Path ../..)
. .\src\backend\.venv\Scripts\Activate.ps1
pytest -q

# Frontend
cd src/frontend
npm install
npm run dev

# Frontend tests
cd src/frontend
npm run test
```

## 📜 License

See `LICENSE`.

---
*Optimized for a 45‑minute, demo-heavy session. Trim sections to reclaim time if live questions expand.*
