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
        <div className="font-inter w-full max-w-6xl 2xl:max-w-7xl mx-auto flex flex-col rounded-xl border border-gray-200 shadow-sm bg-white/80 backdrop-blur p-5">
            <h2 className="text-lg md:text-xl font-semibold text-gray-800 mb-3 flex items-center gap-2"><span role="img" aria-label="robot">🤖</span> Chat with Azure OpenAI</h2>
            <div className="bg-gray-50 text-gray-900 p-4 rounded-lg shadow-inner border border-gray-200 overflow-y-auto flex-grow min-h-[50vh] max-h-[60vh] space-y-4">
                {messages.map((m, i) => {
                    const isUser = m.role === 'user';
                    return (
                        <div
                            key={i}
                            className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[85%] md:max-w-[70%] px-4 py-2 rounded-2xl shadow-sm whitespace-pre-wrap break-words leading-relaxed text-sm border transition-colors ${isUser
                                    ? 'bg-blue-600 text-white border-blue-500 rounded-br-sm'
                                    : 'bg-white text-gray-800 border-gray-200 rounded-bl-sm'}
                            hover:shadow`}
                            >
                                <div className="font-semibold mb-0.5 text-xs opacity-80 tracking-wide">
                                    {isUser ? 'You' : 'AI'}
                                </div>
                                <div>{m.content}</div>
                            </div>
                        </div>
                    );
                })}
            </div>
            <div className="mt-4 flex flex-col">
                {error && <div className="text-red-600 mb-2 text-sm">{error}</div>}
                <textarea
                    className="border w-full p-3 rounded-lg shadow-sm resize-none focus:outline-none focus:ring focus:ring-blue-300 transition text-gray-800 text-sm font-normal leading-relaxed min-h-[10vh] max-h-[20vh] bg-white"
                    placeholder="Type your question..."
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendRequest(); } }}
                />
                <div className="flex justify-end mt-3">
                    <button
                        onClick={sendRequest}
                        disabled={loading}
                        className="bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium px-5 py-2.5 rounded-md shadow hover:bg-blue-700 transition focus:outline-none focus:ring-2 focus:ring-blue-400 flex items-center gap-2"
                    >
                        {loading ? 'Sending…' : 'Send'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Chat;
