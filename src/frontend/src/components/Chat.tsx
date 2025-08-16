import { useState } from "react";
import { fetchAIResponse } from "../services/api";

interface Message { role: 'user' | 'assistant'; content: string }

const Chat: React.FC = () => {
    const [prompt, setPrompt] = useState<string>("");
    const [messages, setMessages] = useState<Message[]>([
        { role: 'assistant', content: 'Ask me something about Azure OpenAI.' }
    ]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const sendRequest = async () => {
        if (!prompt.trim() || loading) return;
        setError(null);
        const userMsg: Message = { role: 'user', content: prompt };
        setMessages(prev => [...prev, userMsg, { role: 'assistant', content: 'Thinking... 🤔' }]);
        setLoading(true);

        const result = await fetchAIResponse(prompt);
        setLoading(false);
        setPrompt("");

        setMessages(prev => {
            // Replace last placeholder assistant message
            const updated = [...prev];
            const idx = updated.findIndex((m, i) => i === updated.length - 1 && m.role === 'assistant' && m.content.startsWith('Thinking'));
            if ('error' in result) {
                if (idx >= 0) updated[idx] = { role: 'assistant', content: `Error: ${result.error}` };
                else updated.push({ role: 'assistant', content: `Error: ${result.error}` });
            } else {
                if (idx >= 0) updated[idx] = { role: 'assistant', content: result.response };
                else updated.push({ role: 'assistant', content: result.response });
            }
            return updated;
        });
        if ('error' in result) setError(result.error);
    };

    return (
        <div className="font-inter p-6 text-center w-full max-w-6xl mx-auto border-2 border-gray-200 rounded-lg shadow-lg bg-white flex flex-col h-[80vh]">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Chat with Azure OpenAI 🤖</h2>
            <div className="bg-gray-50 text-gray-900 p-5 rounded-lg shadow-inner text-left border border-gray-300 overflow-y-auto h-[50vh] flex-grow space-y-4">
                {messages.map((m, i) => (
                    <div key={i} className={m.role === 'user' ? 'text-blue-700' : 'text-gray-800'}>
                        <strong>{m.role === 'user' ? 'You' : 'AI'}:</strong>{' '}
                        <span className="whitespace-pre-wrap break-words">{m.content}</span>
                    </div>
                ))}
            </div>
            <div className="mt-4 flex flex-col">
                {error && <div className="text-red-600 mb-2 text-sm">{error}</div>}
                <textarea
                    className="border w-full p-4 rounded-lg shadow-sm resize-none focus:outline-none focus:ring focus:ring-blue-300 transition text-gray-800 text-base font-normal leading-relaxed min-h-[10vh] max-h-[15vh]"
                    placeholder="Type your question..."
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendRequest(); } }}
                />
                <div className="flex justify-center mt-3">
                    <button
                        onClick={sendRequest}
                        disabled={loading}
                        className="bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold px-6 py-3 rounded-lg shadow-md hover:bg-gray-700 transition focus:outline-none focus:ring-2 focus:ring-gray-400 w-40 flex items-center justify-center"
                    >
                        {loading ? 'Sending...' : '🚀 Send'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Chat;
