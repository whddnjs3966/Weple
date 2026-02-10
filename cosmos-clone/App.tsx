import React from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import ExtensionsSection from './components/ExtensionsSection';
import CurateSection from './components/CurateSection';
import Footer from './components/Footer';

function App() {
  return (
    <div className="min-h-screen bg-background text-primary font-sans selection:bg-white selection:text-black">
      <Navbar />
      
      <main className="flex flex-col w-full">
        <HeroSection />
        <ExtensionsSection />
        <CurateSection />
      </main>

      <Footer />
      
      {/* Floating Theme Toggle / Help Button (Bottom Left as seen in screenshot) */}
      <div className="fixed bottom-6 left-6 z-40 hidden md:flex items-center gap-2">
         <button className="w-10 h-10 rounded-full bg-surface border border-white/10 flex items-center justify-center text-white hover:bg-white hover:text-black transition-colors">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
         </button>
      </div>
      
      {/* Floating Scroll Top / Action (Bottom Right) */}
      <div className="fixed bottom-6 right-6 z-40">
         <button className="w-10 h-10 rounded-full bg-white text-black flex items-center justify-center hover:scale-110 transition-transform">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="19" x2="12" y2="5"></line><polyline points="5 12 12 5 19 12"></polyline></svg>
         </button>
      </div>

    </div>
  );
}

export default App;