import React from 'react';
import Button from './Button';

const ExtensionsSection: React.FC = () => {
  return (
    <section className="relative w-full py-32 flex flex-col items-center justify-center bg-background px-4">
      
      <div className="text-center mb-16 space-y-6 max-w-xl">
        <h2 className="font-serif text-4xl md:text-6xl text-white leading-tight">
          Save from anywhere <br />
          <span className="text-secondary/70">with our extensions</span>
        </h2>
        
        <div className="flex flex-wrap justify-center gap-4 pt-4">
          <Button variant="secondary" className="flex items-center gap-2 !rounded-lg !px-4">
            {/* Chrome Icon Placeholder */}
            <div className="w-4 h-4 rounded-full bg-gradient-to-tr from-red-500 via-green-500 to-yellow-500" />
            Chrome
          </Button>
          <Button variant="secondary" className="flex items-center gap-2 !rounded-lg !px-4">
            {/* Safari Icon Placeholder */}
            <div className="w-4 h-4 rounded-full bg-blue-500" />
            Safari
          </Button>
          <Button variant="secondary" className="flex items-center gap-2 !rounded-lg !px-4">
            {/* Apple Icon Placeholder */}
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.23-3.14-2.47-1.71-2.45-3.03-6.93-1.27-9.98 1.5-2.5 3.3-2.67 4.77-2.62 1.21.04 2.37.81 3.12.81.75 0 2.16-1.02 3.65-.87 1.25.13 2.19.64 2.81 1.55-2.45 1.5-2.04 5.37.4 6.37-.19.6-.47 1.19-.73 1.71zM13 3.5c.57-1.16 1.94-2.07 3.32-2.07.16 2.05-1.99 3.96-3.32 3.96-.34-1.22-.52-1.57 0-1.89z"/></svg>
            iOS
          </Button>
        </div>
      </div>

      {/* Mockup Grid for Extensions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full max-w-6xl">
        <div className="aspect-[4/5] rounded-card overflow-hidden relative group">
          <img src="https://picsum.photos/600/800?random=10" className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700" alt="Extension Demo 1" />
          <div className="absolute inset-0 bg-black/40 group-hover:bg-transparent transition-colors duration-500" />
           {/* Floating Tooltip Mockup */}
           <div className="absolute bottom-1/2 right-10 bg-surface/90 backdrop-blur border border-white/10 p-2 rounded-lg transform translate-y-12 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-all duration-500">
             <span className="text-xs text-white">Save Image +</span>
           </div>
        </div>

        <div className="aspect-[4/5] rounded-card overflow-hidden relative group translate-y-12">
          <img src="https://picsum.photos/600/800?random=11" className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700" alt="Extension Demo 2" />
           <div className="absolute top-10 left-10 p-4 max-w-[200px]">
             <p className="font-serif text-xl italic leading-snug">"I am always doing things I can't do, that's how I get to do them."</p>
             <p className="text-xs text-secondary mt-2">— Picasso</p>
           </div>
        </div>

        <div className="aspect-[4/5] rounded-card overflow-hidden relative group">
          <img src="https://picsum.photos/600/800?random=12" className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700" alt="Extension Demo 3" />
          <div className="absolute top-4 right-4 bg-black/50 p-2 rounded-full backdrop-blur-md">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          </div>
        </div>
      </div>
    </section>
  );
};

export default ExtensionsSection;