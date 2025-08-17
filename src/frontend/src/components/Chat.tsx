import { useEffect, useRef, useState } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faRobot } from '@fortawesome/free-solid-svg-icons';
import { fetchAIResponse } from "../services/api";

interface Message { role: 'user' | 'assistant'; content: string; timestamp: number }

const Chat: React.FC = () => {
    const [prompt, setPrompt] = useState<string>("");
    const [messages, setMessages] = useState<Message[]>([
        { role: 'assistant', content: 'Ask me something about Azure OpenAI.', timestamp: Date.now() }
    ]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const sendRequest = async () => {
        if (!prompt.trim() || loading) return;
        setError(null);
        const userMsg: Message = { role: 'user', content: prompt, timestamp: Date.now() };
        setMessages(prev => [...prev, userMsg, { role: 'assistant', content: 'Thinking... 🤔', timestamp: Date.now() }]);
        setLoading(true);

        const result = await fetchAIResponse(prompt);
        setLoading(false);
        setPrompt("");

        setMessages(prev => {
            // Replace last placeholder assistant message
            const updated = [...prev];
            const idx = updated.findIndex((m, i) => i === updated.length - 1 && m.role === 'assistant' && m.content.startsWith('Thinking'));
            if ('error' in result) {
                if (idx >= 0) updated[idx] = { ...updated[idx], content: `Error: ${result.error}` };
                else updated.push({ role: 'assistant', content: `Error: ${result.error}`, timestamp: Date.now() });
            } else {
                if (idx >= 0) updated[idx] = { ...updated[idx], content: result.response };
                else updated.push({ role: 'assistant', content: result.response, timestamp: Date.now() });
            }
            return updated;
        });
        if ('error' in result) setError(result.error);
    };

    // Auto-scroll to the newest message when messages update
    const scrollRef = useRef<HTMLDivElement | null>(null);
    useEffect(() => {
        const el = scrollRef.current;
        if (!el) return;
        // Use rAF to ensure layout is settled
        requestAnimationFrame(() => {
            el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
        });
    }, [messages]);

    const formatTimestamp = (ts: number) => new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    return (
        <div className="font-inter w-full max-w-6xl 2xl:max-w-7xl mx-auto flex flex-col h-full min-h-0 rounded-xl border border-gray-200 shadow-sm bg-white/80 backdrop-blur p-5 overflow-hidden">
            <h2 className="text-lg md:text-xl font-semibold text-gray-800 mb-3 flex items-center gap-2"><span role="img" aria-label="robot">🤖</span> Chat with Azure OpenAI</h2>
            <div ref={scrollRef} className="bg-gray-50 text-gray-900 p-4 rounded-lg shadow-inner border border-gray-200 flex-1 min-h-0 overflow-y-auto space-y-4">
                {messages.map((m, i) => {
                    const isUser = m.role === 'user';
                    return (
                        <div
                            key={i}
                            className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[85%] md:max-w-[70%] px-4 py-2 rounded-2xl shadow-sm whitespace-pre-wrap break-words leading-relaxed text-sm border transition-colors ${isUser
                                    ? 'bg-blue-100 text-blue-900 border-blue-300 rounded-br-sm hover:bg-blue-50'
                                    : 'bg-white text-gray-800 border-gray-200 rounded-bl-sm hover:bg-gray-50'}
                            hover:shadow`}
                                title={`Sent at ${formatTimestamp(m.timestamp)}`}
                            >
                                <div className="font-semibold mb-0.5 text-xs opacity-80 tracking-wide flex items-center gap-1">
                                    <FontAwesomeIcon icon={isUser ? faUser : faRobot} className="h-3.5 w-3.5" aria-hidden="true" />
                                    <span>{isUser ? 'You' : 'AI'}</span>
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
