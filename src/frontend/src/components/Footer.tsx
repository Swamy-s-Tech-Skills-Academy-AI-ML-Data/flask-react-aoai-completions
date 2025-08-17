const Footer: React.FC = () => {
    const year = new Date().getFullYear();
    return (
        <footer className="mt-auto bg-white/90 backdrop-blur border-t border-gray-200 text-gray-600 text-xs md:text-sm py-3 px-4 flex flex-col md:flex-row items-center justify-between gap-2">
            <div className="flex items-center gap-2">
                <span className="font-medium">Azure OpenAI Chat</span>
                <span className="hidden md:inline text-gray-400">•</span>
                <span className="text-gray-500">© {year}</span>
            </div>
            <div className="flex items-center gap-4 text-gray-500">
                <a href="https://learn.microsoft.com/azure/ai-services/openai" target="_blank" rel="noreferrer" className="hover:text-gray-700 transition">Docs</a>
                <a href="#" className="hover:text-gray-700 transition">Privacy</a>
                <a href="#" className="hover:text-gray-700 transition">Status</a>
            </div>
        </footer>
    );
};

export default Footer;
