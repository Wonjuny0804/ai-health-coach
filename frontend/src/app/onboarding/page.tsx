'use client';

import React from 'react';

const OnboardingPage = () => {
  // Generic steps for the onboarding process
  const steps = [
    { id: 1, name: 'Basic Information', completed: true, current: false },
    { id: 2, name: 'Health Goals', completed: false, current: true },
    { id: 3, name: 'Lifestyle Assessment', completed: false, current: false },
    { id: 4, name: 'Preferences', completed: false, current: false },
    { id: 5, name: 'Review & Complete', completed: false, current: false },
  ];

  return (
    <div className="flex h-screen w-full overflow-hidden">
      {/* Left sidebar with steps */}
      <div className="w-1/4 bg-gray-900 text-white p-6 flex flex-col">
        {/* Logo */}
        <div className="mb-12">
          <h3 className="text-white text-2xl font-bold flex items-center">
            <span className="mr-2">■</span> Melian
          </h3>
        </div>
        
        {/* Steps */}
        <div className="flex-grow">
          <h4 className="text-gray-400 uppercase text-xs font-semibold tracking-wider mb-4">Onboarding Steps</h4>
          <div className="space-y-6">
            {steps.map((step) => (
              <div key={step.id} className="flex items-center">
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center mr-3 ${step.completed ? 'bg-green-500' : step.current ? 'bg-indigo-500' : 'bg-gray-700'}`}>
                  {step.completed ? (
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                    </svg>
                  ) : (
                    <span className="text-white text-sm">{step.id}</span>
                  )}
                </div>
                <span className={`text-sm ${step.current ? 'text-white font-medium' : 'text-gray-300'}`}>
                  {step.name}
                </span>
              </div>
            ))}
          </div>
        </div>
        
        {/* Company branding at the bottom */}
        <div className="mt-auto">
          <p className="text-gray-400 text-xs">© Melian Health 2025</p>
        </div>
      </div>

      {/* Main content area */}
      <div className="w-3/4 bg-white">
        <div className="max-w-3xl mx-auto p-10">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Health Goals</h1>
            <p className="text-gray-500 mt-2">Tell us about your health goals and what you hope to achieve.</p>
          </div>
          
          {/* Placeholder content */}
          <div className="bg-gray-100 rounded-lg p-8 flex flex-col items-center justify-center min-h-[400px] border border-dashed border-gray-300">
            <svg className="w-16 h-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z"></path>
            </svg>
            <p className="text-gray-500 text-center mb-2">Onboarding Step Content</p>
            <p className="text-sm text-gray-400 text-center">This is a placeholder for the main onboarding content</p>
          </div>
          
          {/* Navigation buttons */}
          <div className="flex justify-between mt-10">
            <button className="px-6 py-3 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors">
              Back
            </button>
            <button className="px-6 py-3 bg-gray-900 text-white rounded-md hover:bg-gray-800 transition-colors">
              Continue
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OnboardingPage;