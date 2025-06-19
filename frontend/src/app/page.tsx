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


    </main>
  );
}
