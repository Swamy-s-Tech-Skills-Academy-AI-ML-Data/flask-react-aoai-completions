const Footer: React.FC = () => {
    const year = new Date().getFullYear();
    return (
        <footer className="mt-auto bg-gray-400 border-t border-gray-300 text-white/95 text-xs md:text-sm py-3 px-4 flex flex-col md:flex-row items-center justify-between gap-2 shadow-inner">
            <div className="flex items-center gap-2">
                <span className="font-medium text-white">Azure OpenAI Text Generation</span>
                <span className="hidden md:inline text-white/70">•</span>
                <span className="text-white/90">© {year}</span>
            </div>
            <div className="flex items-center gap-4 text-white/90">
                <a href="https://learn.microsoft.com/azure/ai-services/openai" target="_blank" rel="noreferrer" className="hover:text-white transition">Docs</a>
                <a href="#" className="hover:text-white transition">Privacy</a>
                <a href="#" className="hover:text-white transition">Status</a>
            </div>
        </footer>
    );
};

export default Footer;
