# React + TypeScript + Vite + Tailwind CSS

Some Description.

## 📌 Step 1: Set Up the React + TypeScript Project

```powershell
# Create a new Vite + React + TypeScript project
npm create vite@latest cgpt-clone-gaih -- --template react-ts
Run the following `PowerShell` commands:

```powershell
# Create a new Vite + React + TypeScript pr---

## **✅ What's Next?**

- **Enhance the UI** – Improve styling, add animations.
- **Integrate Auth0** – Implement login/logout properly.
- **Improve API Calls** – Handle streaming responses from Flask.

---

## **📌 Common Layout Issues & Fixes**

### **Issue: Gap Between Chat Area and Footer**

**Problem:** You may notice a purple/empty gap between the chat container and footer when using flexbox layout. This happens when:
- Using `min-h-screen` instead of `h-screen`
- The main content area doesn't properly expand to fill available space
- Footer has `mt-auto` but the parent container allows extra height

**Symptoms:**
- Visible gap/space between chat area and footer
- Chat container not utilizing full viewport height
- Overall layout shorter than expected

**✅ Solution:**

Update your main layout container (`App.tsx`) to use proper height constraints:

```tsx
const App: React.FC = () => {
  return (
    <div className="h-screen flex flex-col bg-gradient-to-b from-slate-50 to-slate-100">
      <TopNav />
      <main className="flex-1 min-h-0 w-full px-3 md:px-6 py-3 flex justify-center items-stretch">
        <Chat />
      </main>
      <Footer />
    </div>
  );
};
```

**Key Changes:**

- `min-h-screen` → `h-screen`: Forces container to exact viewport height
- `flex-grow` → `flex-1`: More explicit space distribution
- `min-h-0`: Prevents flex items from having minimum content size

**Result:** Chat area expands to fill all available space between header and footer with no gaps.

---

This should give you a **React + TypeScript UI** integrated with **Flask & Azure OpenAI**! 🚀 Let me know if you need further refinements. 😃create vite@latest cgpt-clone-gaih

# Move into the project folder

cd cgpt-clone-gaih

# Install Tailwind CSS

npm install -D tailwindcss@3 postcss autoprefixer
npm install @heroicons/react
npx tailwindcss init -p

```

## 📌 Step 2: Configure Tailwind

### Modify `tailwind.config.ts`

```ts
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    container: {
      center: true,
      padding: "1rem",
      screens: {
        sm: "100%",
        md: "100%",
        lg: "1200px",
        xl: "1500px",
        "2xl": "1600px",
      },
    },
    extend: {},
  },
  plugins: [],
};
```

### Update `src/index.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

Got it! We'll build the **React UI with TypeScript and Tailwind CSS**, and integrate it with our **Flask API (Azure OpenAI backend).**

---

## ✅ **Project Plan**

✔ **Header** – Shows **Login/Logout** (Auth0 integration later).  
✔ **Main Content Area** – Chat UI to interact with Flask API.  
✔ **Footer** – Simple branding/info section.  
✔ **Integration with Flask** – Calls the `/api/completions` endpoint.

---

---

---

## **📌 Step 3: Build the App Layout**

Now, let’s create the **Header, Chat, and Footer** components.

### **1️⃣ `src/components/Header.tsx` (Login/Logout)**

```tsx
import { useState } from "react";

const Header: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);

  return (
    <header className="bg-blue-600 text-white p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold">ChatGPT Clone</h1>
      <button
        className="bg-white text-blue-600 px-4 py-2 rounded"
        onClick={() => setIsLoggedIn(!isLoggedIn)}
      >
        {isLoggedIn ? "Logout" : "Login"}
      </button>
    </header>
  );
};

export default Header;
```

---

### **2️⃣ `src/components/Chat.tsx` (Main Chat UI)**

```tsx
import { useState } from "react";

const Chat: React.FC = () => {
  const [prompt, setPrompt] = useState<string>("");
  const [response, setResponse] = useState<string>("");

  const sendRequest = async () => {
    setResponse("Loading...");

    try {
      const res = await fetch("http://127.0.0.1:5009/api/completions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.text();
      setResponse(data);
    } catch (error) {
      setResponse("Error fetching response.");
    }
  };

  return (
    <div className="p-6 text-center">
      <h2 className="text-2xl font-semibold mb-4">Chat with AI</h2>
      <textarea
        className="border w-full p-2 rounded"
        rows={3}
        placeholder="Type your question..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button
        onClick={sendRequest}
        className="bg-blue-600 text-white px-4 py-2 mt-2 rounded"
      >
        Send
      </button>
      <div className="mt-4 bg-gray-100 p-4 rounded">{response}</div>
    </div>
  );
};

export default Chat;
```

---

### **3️⃣ `src/components/Footer.tsx`**

```tsx
const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-800 text-white text-center p-3">
      © 2025 AI Chat App - Built with Flask & Azure OpenAI
    </footer>
  );
};

export default Footer;
```

---

## **📌 Step 4: Set Up the Main App**

Now, modify **`src/App.tsx`** to use the components:

```tsx
import Header from "./components/Header";
import Chat from "./components/Chat";
import Footer from "./components/Footer";

const App: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow flex justify-center items-center bg-gray-100">
        <Chat />
      </main>
      <Footer />
    </div>
  );
};

export default App;
```

---

## **📌 Step 5: Start the React App**

Run the following commands:

```powershell
npm install  # Install dependencies
npm run dev  # Start the development server
```

The app will be available at **`http://localhost:5173/`** 🎉

---

## **✅ What’s Next?**

- **Enhance the UI** – Improve styling, add animations.
- **Integrate Auth0** – Implement login/logout properly.
- **Improve API Calls** – Handle streaming responses from Flask.

---

This should give you a **React + TypeScript UI** integrated with **Flask & Azure OpenAI**! 🚀 Let me know if you need further refinements. 😃

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default tseslint.config({
  extends: [
    // Remove ...tseslint.configs.recommended and replace with this
    ...tseslint.configs.recommendedTypeChecked,
    // Alternatively, use this for stricter rules
    ...tseslint.configs.strictTypeChecked,
    // Optionally, add this for stylistic rules
    ...tseslint.configs.stylisticTypeChecked,
  ],
  languageOptions: {
    // other options...
    parserOptions: {
      project: ["./tsconfig.node.json", "./tsconfig.app.json"],
      tsconfigRootDir: import.meta.dirname,
    },
  },
});
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from "eslint-plugin-react-x";
import reactDom from "eslint-plugin-react-dom";

export default tseslint.config({
  plugins: {
    // Add the react-x and react-dom plugins
    "react-x": reactX,
    "react-dom": reactDom,
  },
  rules: {
    // other rules...
    // Enable its recommended typescript rules
    ...reactX.configs["recommended-typescript"].rules,
    ...reactDom.configs.recommended.rules,
  },
});
```
