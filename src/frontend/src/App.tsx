// Sidebar & old Header removed in redesign
import TopNav from "./components/TopNav";
import Chat from "./components/Chat";
import Footer from "./components/Footer";

const App: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-slate-50 to-slate-100">
      <TopNav />
      <main className="flex-grow w-full px-3 md:px-6 py-4 flex justify-center items-stretch">
        <Chat />
      </main>
      <Footer />
    </div>
  );
};

export default App;
