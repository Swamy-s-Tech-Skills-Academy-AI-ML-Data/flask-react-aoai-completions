# Flask Azure OpenAI API

A Simple Python Flask API to interact with Azure OpenAI.

## 🔹 Installation & Setup

> 1. Changed Directory to `D:\STSA\flask-react-aoai-completions\src\backend`

```bash
python --version
pip --version

pip install virtualenv
python -m venv .venv
.venv/Scripts/activate
python -m pip install --upgrade pip

pip install Flask python-dotenv openai
pip install flask-cors
pip freeze > requirements.txt
```

## 🔹 Testing (Pytest) – No need for `pytest-flask`

We intentionally do **not** install the `pytest-flask` plugin. It tries to import deprecated internal Flask symbols (e.g. `_request_ctx_stack`) that were removed in Flask 3.x, causing an `ImportError`. Our tests stay lightweight by defining only the fixtures we actually need.

### How it works

`tests/conftest.py` provides:

1. A dummy Azure OpenAI client via an `autouse` fixture (`patch_azure_openai`) so no real network call occurs.
2. An `app` fixture that imports and calls `create_app()` from `app.py`.
3. A `client` fixture that simply returns `app.test_client()` (the standard Flask test client—no plugin wrapper needed).

Minimal snippet (simplified):

```python
@pytest.fixture
def app():
  from app import create_app
  return create_app()

@pytest.fixture
def client(app):
  return app.test_client()
```

### Why this is enough

- Flask already ships a `test_client()` method.
- We don’t rely on any extra helpers that `pytest-flask` would add.
- Fewer dependencies → faster, more stable test runs.

### Running the tests

From repo root (ensures `pyproject.toml` pytest config is picked up):

```powershell
cd <repo-root>
. .\src\backend\.venv\Scripts\Activate.ps1
pytest -q
```

### Configuration

`pyproject.toml` includes:

```toml
[tool.pytest.ini_options]
addopts = "-q"
pythonpath = [".", "src/backend"]
```

That `pythonpath` entry lets tests import backend modules without adjusting `PYTHONPATH` manually.

Result: fast, isolated tests (mocked Azure) with **zero** need for `pytest-flask`.

## 🔹 To install dependencies later

```bash
pip install -r requirements.txt
```

## Update the .env file

## Update the environment variable `AZURE_OPENAI_API_KEY`

> 1. After updating verify the `AZURE_OPENAI_API_KEY`. **Only for INTERNAL USE.**

```PowerShell
$env:AZURE_OPENAI_API_KEY
```

## 🔹 Project Structure

```text
flask-react-aoai-completions/
│── docs/
│── src/
│   ├── backend/
│   │   ├── api/ (Routes)
│   │   ├── services/ (Azure OpenAI Integration)
│   │   ├── utils/ (Configs & Logging)
│   │   ├── app.py
│── .gitignore
│── README.md
```

## 🔹 How to Execute

### ✅ Method 1: Run `app.py` Directly

```powershell
python .\app.py
py .\app.py
```

This will start the Flask server, and you should see output like:

```text
Starting Flask Azure OpenAI API Server...
 * Running on http://127.0.0.1:5009/ (Press CTRL+C to quit)
```

Now, visit `[http://127.0.0.1:5009/api/](http://127.0.0.1:5009/api/)` in your browser.

---

### ✅ Method 2: Use `flask run` (Requires Setting Environment Variables)

Before running the app, set environment variables:

```powershell
$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"
flask run --host=0.0.0.0 --port=5009
```

This will also start the Flask server.

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5009/api/completions" `
                  -Method POST `
                  -Headers @{"Content-Type"="application/json"} `
                  -Body '{"prompt": "What is an Orange"}'

```

---

### **Stopping the Server**

Press **CTRL + C** in the PowerShell terminal to stop the server.

---

🚀 **Try it out and let me know if you need any help!** 😃

---

## 🔹 API Usage (Example)

```http
POST /api/completions
Content-Type: application/json

{"prompt": "Explain Azure OpenAI"}
```

Example response:

```json
{
  "response": "Azure OpenAI provides...",
  "usage": { "prompt_chars": 21, "response_chars": 42 }
}
```
