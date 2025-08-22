# Frontend: React + TypeScript + Vite + Tailwind

This app is a Vite + React (TypeScript) UI that talks to the Flask backend.

## 1) Setup

PowerShell (Windows):

```powershell
# from repo root
cd src/frontend
npm install
```

Tailwind is already configured in this repo. If you are creating a new project from scratch, see Tailwind docs. In this repo the key files are `tailwind.config.js`, `postcss.config.js`, and `src/index.css`.

## 2) Configure API base URL

The frontend uses `VITE_API_BASE_URL` to call the backend.

- Without a proxy, set it to the Flask API base: `http://127.0.0.1:5009/api`
- Or use the Vite dev proxy option below and set it to `/api`

Create `.env.local` in `src/frontend` if needed:

```env
VITE_API_BASE_URL=http://127.0.0.1:5009/api
```

You can verify backend config via: `GET http://127.0.0.1:5009/api/config/info`.

## 3) Optional: Vite dev proxy (avoids CORS in dev)

Update `vite.config.ts` to proxy `/api` to Flask when running `npm run dev`:

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
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

Then set `VITE_API_BASE_URL=/api` in `.env.local`.

## 4) Running the frontend

```powershell
cd src/frontend
npm run dev
```

App runs at <http://localhost:5173>.

## 5) Using the API client

The helper in `src/frontend/src/services/api.ts` reads `VITE_API_BASE_URL` and calls `/completions`.

Example usage inside a React component:

```tsx
import { useState } from 'react'
import { fetchAIResponse } from '../services/api'

export default function Chat() {
  const [prompt, setPrompt] = useState('')
  const [answer, setAnswer] = useState('')

  const send = async () => {
    const res = await fetchAIResponse(prompt)
    setAnswer('error' in res ? res.error : res.response)
  }

  return (
    <div className="p-4">
      <textarea className="border w-full p-2" value={prompt} onChange={e => setPrompt(e.target.value)} />
      <button className="mt-2 px-3 py-2 bg-blue-600 text-white" onClick={send}>Send</button>
      <div className="mt-4 whitespace-pre-wrap">{answer}</div>
    </div>
  )
}
```

## 6) Layout tips

If you see a gap between chat area and footer, ensure your top-level container uses `h-screen`, the content area uses `flex-1 min-h-0`, and Footer is after the main content.

## 7) Troubleshooting

- CORS errors in the browser? Either enable Flask-CORS on the backend or use the Vite proxy (recommended in dev).
- 404 for `/api/config/info`? Make sure the Flask server is running and the endpoint is registered as `/api/config/info`.
- Mixed content or wrong port? Verify `VITE_API_BASE_URL` or dev proxy targets the backend `http://127.0.0.1:5009`.
