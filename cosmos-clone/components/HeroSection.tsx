import React, { useEffect, useState } from 'react';

const scatteredImages = [
  "https://picsum.photos/200/300?random=1",
  "https://picsum.photos/250/200?random=2",
  "https://picsum.photos/220/320?random=3",
  "https://picsum.photos/200/200?random=4",
  "https://picsum.photos/180/280?random=5",
  "https://picsum.photos/260/190?random=6",
  "https://picsum.photos/210/290?random=7",
  "https://picsum.photos/230/230?random=8",
];

const HeroSection: React.FC = () => {
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setOffset(window.scrollY);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <section className="relative w-full min-h-screen flex flex-col items-center justify-center overflow-hidden pt-32">
      
      {/* Background Ambience */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-white/5 rounded-full blur-[120px] pointer-events-none" />

      {/* Scattered Images Layer */}
      <div className="absolute inset-0 w-full h-full pointer-events-none">
        {scatteredImages.map((src, index) => {
          // Deterministic "random" positions based on index
          const top = 50 + (Math.sin(index * 2) * 35);
          const left = 50 + (Math.cos(index * 2) * 35);
          const rotate = (index % 2 === 0 ? 1 : -1) * (index * 5);
          const zIndex = index;
          
          // Parallax effect
          const parallaxY = offset * (0.05 + (index * 0.01));

          return (
            <div 
              key={index}
              className="absolute transition-transform duration-100 ease-linear shadow-2xl"
              style={{
                top: `${top}%`,
                left: `${left}%`,
                width: '180px',
                zIndex: zIndex,
                transform: `translate(-50%, -50%) rotate(${rotate}deg) translateY(-${parallaxY}px)`,
                opacity: 0.6 - (offset * 0.001)
              }}
            >
              <div className="relative group overflow-hidden rounded-card border border-white/5 bg-surface">
                <img 
                  src={src} 
                  alt="Scattered element" 
                  className="w-full h-auto object-cover opacity-80 group-hover:opacity-100 transition-opacity"
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Main Content */}
      <div className="relative z-10 text-center space-y-6 max-w-2xl px-6">
        <h1 className="font-serif text-6xl md:text-8xl lg:text-9xl text-white tracking-tight leading-none mix-blend-screen">
          COSMOS<sup className="text-3xl md:text-5xl align-super">©</sup>
        </h1>
        
        <p className="text-lg md:text-xl text-secondary font-sans tracking-wide">
          A discovery engine for <span className="inline-block px-3 py-1 bg-white/10 rounded-full border border-white/10 text-white text-sm align-middle mx-1">creatives</span>
        </p>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-10 animate-bounce text-secondary text-xs uppercase tracking-widest">
        Scroll to explore
      </div>
    </section>
  );
};

export default HeroSection;