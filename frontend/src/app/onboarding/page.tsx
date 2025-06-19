'use client';

import React, { useState } from 'react';
import { LogOut } from 'lucide-react';

interface UserProfile {
  userId: string;
  birthday: Date;
  sex: string;
  trainingYears: number;
  trainingStyle: string;
  heightCm: number;
  equipmentNotes: string;
  availability_notes: string;
  limitation_notes: string;
  createdAt: number;
  updatedAt: number;
}


const steps = [
  {
    id: 'display_name',

  }
]

const OnboardingPage = () => {

  return (
    <div className="h-screen w-full overflow-hidden">
      {/* Left sidebar with steps */}
      <header className="w-full p-4 bg-white text-white flex justify-between border border-b ">
        {/* Logo */}
        <div className="px-2">
          <h3 className="text-foreground text-2xl font-bold flex items-center">
            Melian
          </h3>
        </div>

        <div className="flex items-center gap-2">
          <LogOut className="text-black" />
          <button className="text-foreground font-medium">Log out</button>
        </div>
      </header>
    </div>
  );
};

export default OnboardingPage;