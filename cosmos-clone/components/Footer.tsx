import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="w-full py-12 px-6 border-t border-white/5 flex flex-col md:flex-row justify-between items-center text-sm text-tertiary">
      <div className="flex items-center gap-2 mb-4 md:mb-0">
        <span className="w-3 h-3 rounded-full bg-white/20" />
        <span className="font-serif text-white">COSMOS</span>
      </div>
      
      <div className="flex gap-6">
        <a href="#" className="hover:text-white transition-colors">Privacy</a>
        <a href="#" className="hover:text-white transition-colors">Terms</a>
        <a href="#" className="hover:text-white transition-colors">Twitter</a>
        <a href="#" className="hover:text-white transition-colors">Instagram</a>
      </div>
    </footer>
  );
};

export default Footer;