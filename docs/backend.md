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

---

# Flask Azure Open AI api

A Simple Python Flask API to Interact with Azure Open AI

## Executing the API

```bash
python app.py           # On Windows
```

```Powershell
$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"
flask run
```

## Few Commands to get started

```bash
pip install virtualenv
python.exe -m pip install --upgrade pip
python -m venv .venv
.venv/Scripts/activate
pip freeze
deactivate

pip install Flask python-dotenv openai
pip freeze > ./requirements.txt

pip install -r ./requirements.txt
```

## Steps to create the API

> 1. Create a new folder
> 1. Create an .env file and Environment Variables
> 1. Create a virtual environment
> 1. Install `pip install Flask python-dotenv openai` and other dependencies
> 1. pip freeze > requirements.txt
> 1. Create a `app.py` file

Your **README.md** is clear and provides a good starting point! ✅

### 🔹 **Suggestions for Improvement:**

1. **Expand API Usage Section** – Add a sample API request & response.
2. **Environment Variables Section** – Mention required `.env` variables for Azure OpenAI.
3. **Project Structure Section** – Briefly describe your folders.
4. **Streaming Support (if included)** – Note how responses will be streamed.

---

### 📌 **Updated `README.md` with More Details**

````markdown
# Flask Azure OpenAI API

A Simple Python Flask API to interact with Azure OpenAI.

## 🔹 Executing the API

```bash
python app.py           # On Windows
```
````

```powershell
$env:FLASK_APP = "app"
$env:FLASK_ENV = "development"
flask run
```

## 🔹 Environment Variables

Create a `.env` file in the root folder with:

```ini
AZURE_OPENAI_API_KEY="your-api-key"
AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4"
```

## 🔹 Installation & Setup

```bash
pip install virtualenv
python.exe -m pip install --upgrade pip
python -m venv .venv
.venv/Scripts/activate
pip install Flask python-dotenv openai
pip freeze > requirements.txt
```

To install dependencies later:

```bash
pip install -r requirements.txt
```

## 🔹 Project Structure

```
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

## 🔹 API Usage

### **1️⃣ Get Completion Response**

#### **Request**

```http
POST /api/completions
Content-Type: application/json

{
    "prompt": "Write a short story about AI."
}
```

#### **Response**

```json
{
  "response": "Once upon a time, an AI named Nova..."
}
```

### **2️⃣ Streamed Response (Optional)**

If streaming is enabled, responses will be sent **chunk by chunk**.

---

🚀 **Ready to implement the API? Let me know!** 🚀  
I can generate `app.py` + `completions_routes.py` + `azure_openai_service.py` to kickstart the API. ✅
