# flask-react-aoai-completions

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

## 🧪 Test Philosophy

Backend: minimal fast tests (route availability, validation, success) with a dummy client to avoid network calls.
Frontend: UI rendering & interaction for Chat component; mock API layer.

## 🪵 Logging

Configure via `LOG_LEVEL` & `LOG_FORMAT`.

- Text example: `2025-08-16 18:20:11 | INFO | Starting Chat Completions API`
- JSON example: `{ "ts": "2025-08-16T18:20:11Z", "level": "INFO", "msg": "Starting Chat Completions API" }`

## 🛠 Troubleshooting 401 Errors (Azure OpenAI)

1. Endpoint form: `https://<resource>.openai.azure.com` (no extra path).
2. Deployment name must match portal deployment.
3. Key must be active (try regenerating Key 1, update `.env`, restart backend).
4. API version supported by your model.
5. Remove stray quotes or spaces around keys.

## 🚀 Next Ideas

- SSE streaming
- Multi‑turn with conversation trimming
- Rate limiting & auth
- Docker / CI pipeline

## UI First Look

![UI First Looks](./docs/images/Session2_FirstLook.PNG)
