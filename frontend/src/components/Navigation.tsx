'use client';
import React, { useState } from 'react';
import Link from 'next/link';

const Navigation = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 px-4 md:px-6 lg:px-8 py-4">
      <div className="max-w-7xl mx-auto">
        {/* Glassmorphic container */}
        <div className="bg-white/20 backdrop-blur-lg rounded-xl shadow-lg 
                      border border-white/30 p-4 flex justify-between items-center">
          
          {/* Logo */}
          <div className="font-bold text-xl text-white">Melian</div>
          
          {/* Desktop Navigation - Only visible on md and above */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/services" className="text-white/90 hover:text-white transition-colors">
              Services
            </Link>
            <Link href="/about" className="text-white/90 hover:text-white transition-colors">
              About Us
            </Link>
            <Link href="/login" className="px-4 py-2 bg-white/20 text-white rounded-lg 
                                          hover:bg-white/30 transition-colors border border-white/30">
              Login with your account
            </Link>
          </div>
          
          {/* Mobile burger menu button - Only visible on smaller screens */}
          <button 
            className="md:hidden text-white"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            )}
          </button>
        </div>
        
        {/* Mobile Navigation - Dropdown for mobile */}
        {isOpen && (
          <div className="md:hidden mt-2 bg-white/20 backdrop-blur-lg rounded-xl shadow-lg 
                        border border-white/30 p-4">
            <div className="flex flex-col space-y-4">
              <Link href="/services" className="text-white/90 hover:text-white transition-colors text-center py-2">
                Services
              </Link>
              <Link href="/about" className="text-white/90 hover:text-white transition-colors text-center py-2">
                About Us
              </Link>
              <Link href="/login" className="px-4 py-2 bg-white/20 text-white rounded-lg 
                                          hover:bg-white/30 transition-colors border border-white/30 text-center">
                Login with your account
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation;
