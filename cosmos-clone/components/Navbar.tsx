import React from 'react';
import Button from './Button';
import { NavItem } from '../types';

const navItems: NavItem[] = [
  { label: 'Manifesto', href: '#' },
  { label: 'Careers', href: '#' },
  { label: 'Discover', href: '#' },
];

const Navbar: React.FC = () => {
  return (
    <div className="fixed top-6 left-0 right-0 z-50 flex justify-center w-full px-4">
      <nav className="flex items-center gap-1 p-1.5 pl-6 bg-surface/60 backdrop-blur-xl border border-white/10 rounded-pill shadow-2xl shadow-black/50">
        
        {/* Logo / Brand Icon Placeholder */}
        <div className="mr-4 text-white opacity-90">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" strokeDasharray="4 4" className="animate-spin-slow" />
            <circle cx="12" cy="12" r="4" fill="currentColor" />
          </svg>
        </div>

        {/* Navigation Links */}
        <div className="hidden md:flex items-center gap-6 mr-6">
          {navItems.map((item) => (
            <a 
              key={item.label} 
              href={item.href} 
              className="text-xs font-medium text-secondary hover:text-white transition-colors uppercase tracking-wider"
            >
              {item.label}
            </a>
          ))}
        </div>

        {/* Auth Buttons */}
        <div className="flex items-center gap-2">
          <Button variant="ghost" className="!px-4">Log In</Button>
          <Button variant="primary">Sign up</Button>
        </div>
      </nav>
    </div>
  );
};

export default Navbar;