'use client';
import React, { useState } from 'react';
import Link from 'next/link';

const Navigation = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 px-4 md:px-6 lg:px-8 py-4 bg-white">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center">
          
          {/* Logo */}
          <div className="font-bold text-xl">FLOWSYNC</div>
          
          {/* Desktop Navigation - Only visible on md and above */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/features" className="text-gray-700 hover:text-gray-900 transition-colors">
              Features
            </Link>
            <Link href="/about" className="text-gray-700 hover:text-gray-900 transition-colors">
              About us
            </Link>
            <Link href="/pricing" className="text-gray-700 hover:text-gray-900 transition-colors">
              Pricing
            </Link>
            <Link href="/functionalities" className="text-gray-700 hover:text-gray-900 transition-colors">
              Functionalities
            </Link>
            <Link href="/integration" className="text-gray-700 hover:text-gray-900 transition-colors">
              Integration
            </Link>
            <Link href="/signup" className="ml-4 px-6 py-2 bg-purple-800 text-white rounded-lg 
                                          hover:bg-purple-900 transition-colors">
              Try it for free
            </Link>
          </div>
          
          {/* Mobile burger menu button - Only visible on smaller screens */}
          <button 
            className="md:hidden text-gray-800"
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
          <div className="md:hidden mt-2 bg-white shadow-lg rounded-lg">
            <div className="flex flex-col space-y-4 p-4">
              <Link href="/features" className="text-gray-700 hover:text-gray-900 transition-colors text-center py-2">
                Features
              </Link>
              <Link href="/about" className="text-gray-700 hover:text-gray-900 transition-colors text-center py-2">
                About us
              </Link>
              <Link href="/pricing" className="text-gray-700 hover:text-gray-900 transition-colors text-center py-2">
                Pricing
              </Link>
              <Link href="/functionalities" className="text-gray-700 hover:text-gray-900 transition-colors text-center py-2">
                Functionalities
              </Link>
              <Link href="/integration" className="text-gray-700 hover:text-gray-900 transition-colors text-center py-2">
                Integration
              </Link>
              <Link href="/signup" className="px-6 py-2 bg-purple-800 text-white rounded-lg 
                                            hover:bg-purple-900 transition-colors text-center">
                Try it for free
              </Link>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation;
