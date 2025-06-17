'use client';

import React, { useState } from 'react';
import useOnboarding from '@/hooks/useOnboarding';

const mockData = {
  "sessionId": "abc",
  "status": "question",
  "currentStepId": "display_name",
  "steps": [
      {
          "id": "display_name",
          "title": "Display name",
          "answer": null,
          "status": "current"
      },
      {
          "id": "birthday",
          "title": "Birthday",
          "answer": null,
          "status": "upcoming"
      },
      {
          "id": "sex",
          "title": "Sex / gender",
          "answer": null,
          "status": "upcoming"
      },
      {
          "id": "height",
          "title": "Height",
          "answer": null,
          "status": "upcoming"
      },
      {
          "id": "training_experience",
          "title": "Experience",
          "answer": null,
          "status": "upcoming"
      },
      {
          "id": "training_style",
          "title": "Training style",
          "answer": null,
          "status": "upcoming"
      },
      {
          "id": "equipment",
          "title": "Equipment",
          "answer": null,
          "status": "upcoming"
      },
      {
          "id": "availability",
          "title": "Availability",
          "answer": null,
          "status": "upcoming"
      },
      {
          "id": "limitations",
          "title": "Limitations",
          "answer": null,
          "status": "upcoming"
      }
  ],
  "payload": {
      "kind": "text",
      "id": "display_name",
      "prompt": "What would you like us to call you?",
      "placeholder": "Enter a display name",
      "required": true,
      "minLen": 2,
      "maxLen": 40
  },
  "paraphrasedAnswers": {}
}

const OnboardingPage = () => {
  // Generic steps for the onboarding process
  const data = useOnboarding() || mockData;
  console.log(data);

  const steps = data.steps;
  const payload = data.payload;


  const [inputValue, setInputValue] = useState('');


  // const handleSubmit = async () => {
  //   try {
  //     const response = await fetch('http://localhost:8000/api/onboarding/chat', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({
  //         message: inputValue,
  //       }),
  //     });
  //     const { data } = await response.json();

  //   } catch(error) {
  //     console.log(error);
  //   }
  // };

  return (
    <div className="flex h-screen w-full overflow-hidden">
      {/* Left sidebar with steps */}
      <div className="w-1/4 bg-white text-white p-6 flex flex-col">
        {/* Logo */}
        <div className="mb-12">
          <h3 className="text-black text-2xl font-bold flex items-center">
            <span className="mr-2">■</span> Melian
          </h3>
        </div>
        
        {/* Steps */}
        <div className="flex-grow">
          <h4 className="text-gray-400 uppercase text-xs font-semibold tracking-wider mb-4">Onboarding Steps</h4>
          <div className="relative">
            {/* Steps */}
            <div className="space-y-5 relative z-10">
              {steps.map((step) => (
                <div key={step.id} className="flex items-center">
                  {/* Step indicator */}
                  {step.status === 'done' ? (
                    <div className="flex-shrink-0 w-7 h-7 rounded-full bg-green-500 flex items-center justify-center mr-3">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
                      </svg>
                    </div>
                  ) : step.status === 'current' ? (
                    <div className="flex-shrink-0 w-7 h-7 rounded-full border-2 border-blue-500 flex items-center justify-center mr-3">
                      <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                    </div>
                  ) : (
                    <div className="flex-shrink-0 w-7 h-7 rounded-full border border-gray-500 flex items-center justify-center mr-3">
                    </div>
                  )}
                  
                  <span className={`text-sm ${
                    step.status === 'done' ? 'text-gray-300' : 
                    step.status === 'current' ? 'text-blue-500 font-medium' : 
                    'text-gray-400'
                  }`}>
                    {step.title}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* Company branding at the bottom */}
        <div className="mt-auto">
          <p className="text-gray-400 text-xs">© Melian Health 2025</p>
        </div>
      </div>

      {/* Main content area */}
      <div className="w-3/4 bg-white flex items-center justify-center">
        <div className="max-w-3xl mx-auto p-10 mb-20">
          {/*  This is where the main content goes, using the payload from the API response */}
          {/* Question */}
          <h2 className="text-3xl text-black  font-bold mb-4">{payload.prompt}</h2>
          {/* Input */}
          <input type="text" className="w-full p-2 border border-gray-300 rounded text-black" onChange={(e) => { setInputValue(e.target.value) }} />
          {/* Button */}
          <button 
          className="w-full p-2 bg-blue-500 text-white rounded mt-4 hover:bg-blue-600 transition-colors disabled:bg-gray-400"
          disabled={true} onClick={() => {}}>Submit</button>
        </div>
      </div>
    </div>
  );
};

export default OnboardingPage;