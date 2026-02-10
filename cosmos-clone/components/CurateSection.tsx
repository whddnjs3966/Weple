import React from 'react';
import Button from './Button';

const CurateSection: React.FC = () => {
  return (
    <section className="relative w-full py-24 px-4 flex flex-col items-center">
      <div className="mb-20 text-center max-w-2xl">
        <h2 className="font-serif text-5xl md:text-6xl mb-6">Curate your inspiration</h2>
        <p className="text-secondary text-lg font-light leading-relaxed">
          Organize your elements into clusters that people can follow. Clusters can be made private or public, and you can collaborate with others.
        </p>
      </div>

      {/* Dark Container Card */}
      <div className="w-full max-w-5xl bg-[#0a0a0a] border border-white/5 rounded-[32px] p-8 md:p-16 relative overflow-hidden">
        {/* Subtle Glow at top */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-1/2 h-32 bg-white/5 blur-[80px]" />

        <div className="flex flex-col items-center mb-12">
          <h3 className="font-serif text-3xl mb-2">Ethereal Archives</h3>
          <div className="flex items-center gap-2 text-sm text-secondary mb-6">
            <span>700 Followers</span>
            <span className="w-1 h-1 bg-secondary rounded-full" />
            <span>By @kaurora</span>
          </div>
          <Button variant="primary" className="!px-8">Follow</Button>
        </div>

        {/* Masonry-ish Grid inside the card */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="space-y-4">
            <div className="group relative overflow-hidden rounded-xl bg-surface">
              <img src="https://picsum.photos/400/500?random=20" className="w-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-500" alt="Gallery" />
            </div>
            <div className="group relative overflow-hidden rounded-xl bg-surface">
              <img src="https://picsum.photos/400/300?random=21" className="w-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-500" alt="Gallery" />
            </div>
          </div>
          
          <div className="space-y-4 pt-12">
             <div className="group relative overflow-hidden rounded-xl bg-surface">
              <img src="https://picsum.photos/400/600?random=22" className="w-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-500" alt="Gallery" />
              <div className="absolute bottom-4 right-4 p-2 bg-black/50 backdrop-blur rounded-lg opacity-0 group-hover:opacity-100 transition-opacity">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div className="group relative overflow-hidden rounded-xl bg-surface">
              <img src="https://picsum.photos/400/400?random=23" className="w-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-500" alt="Gallery" />
            </div>
            <div className="group relative overflow-hidden rounded-xl bg-surface">
              <img src="https://picsum.photos/400/450?random=24" className="w-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-500" alt="Gallery" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CurateSection;