const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5009/api";

interface CompletionSuccess {
    response: string;
    usage?: { prompt_chars: number; response_chars: number };
}
interface CompletionError { error: string }

export const fetchAIResponse = async (prompt: string): Promise<CompletionSuccess | CompletionError> => {
    try {
        const res = await fetch(`${BASE_URL}/completions`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt })
        });

        const ct = res.headers.get("content-type") || "";
        let parsed: any;
        if (ct.includes("application/json")) {
            parsed = await res.json();
        } else {
            // Fallback: attempt text
            const txt = await res.text();
            try { parsed = JSON.parse(txt); } catch { parsed = { error: txt || 'Unknown response format' }; }
        }

        if (!res.ok) {
            return { error: parsed?.error || `HTTP ${res.status}` };
        }
        if (parsed.error) return { error: parsed.error };
        return { response: parsed.response ?? "", usage: parsed.usage };
    } catch (e) {
        return { error: e instanceof Error ? e.message : 'Unexpected error' };
    }
};
