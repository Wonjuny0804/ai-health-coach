import Navigation from '../components/Navigation';

export default function Home() {
  return (
    <main className="min-h-screen relative">
      {/* Navigation component */}
      <Navigation />
      
      {/* Main content area */}
      <div className="container mx-auto pt-24 px-4">
        <h1 className="text-3xl font-bold text-white">Welcome to Melian</h1>
        <p className="text-white/80 mt-4">Your personal AI health coach</p>
      </div>
      
      {/* This div can be used for the background image later */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-700">
        {/* Background will be replaced with an image by the user */}
      </div>
    </main>
  );
}
