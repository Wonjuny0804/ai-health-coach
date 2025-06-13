'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { createClient } from '@/utils/supabase/client';

export default function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const supabase = createClient();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      setError(null);
      setLoading(true);
      
      const { error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      console.log('LOGIN::')
      
      if (error) {
        setError(error.message);
        return;
      }
      
      // Successful login - redirect to dashboard or home page
      router.push('/dashboard');
      router.refresh();
    } catch (err) {
      console.error('Login error:', err);
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const handleGoogleSignIn = async () => {
    try {
      setError(null);
      setLoading(true);
      
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/auth/callback`,
        },
      });
      
      if (error) {
        setError(error.message);
      }
      // The OAuth flow will handle the redirect
    } catch (err) {
      console.error('Google sign-in error:', err);
      setError('An error occurred with Google sign-in. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-full overflow-hidden">
      {/* Left side - Dark panel with vertical lines */}
      <div className="hidden md:block w-1/2 bg-gray-900 relative">
        <div className="absolute inset-0" 
             style={{
               backgroundImage: 'repeating-linear-gradient(to right, rgba(255,255,255,0.1) 0px, rgba(255,255,255,0.1) 1px, transparent 1px, transparent 30px)',
               backgroundSize: '100% 100%',
             }}>
        </div>
        
        {/* Left panel content */}
        <div className="absolute top-6 left-6 bg-gray-800/70 px-5 py-3 rounded-full flex items-center space-x-2">
          <div className="w-4 h-4 rounded-full bg-gray-600"></div>
          <span className="text-gray-300 text-sm font-medium">Melian Login</span>
        </div>
        
        {/* Company branding at the bottom */}
        <div className="absolute bottom-8 left-8">
          <h3 className="text-white text-2xl font-bold flex items-center">
            <span className="mr-2">■</span> Melian
          </h3>
          <p className="text-gray-400 text-xs mt-1">© Melian Health 2025</p>
        </div>
      </div>

      {/* Right side - Login form */}
      <div className="w-full md:w-1/2 bg-white flex items-center justify-center p-8">
        <div className="max-w-md w-full space-y-8">
          {/* Header information */}
          <div>
            <h2 className="mt-6 text-4xl font-extrabold text-gray-900">Welcome, login to your account.</h2>
            <div className="mt-2">
              <p className="text-sm text-gray-500">
                Melian Health Coach Platform
              </p>
            </div>
          </div>

          {/* Form */}
          {error && (
            <div className="p-4 mb-4 text-sm text-red-700 bg-red-100 rounded-lg" role="alert">
              {error}
            </div>
          )}
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            <div className="space-y-6 rounded-md">
              <div>
                <label htmlFor="email-address" className="block text-sm font-medium text-gray-700">
                  Username or Email Address
                </label>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="mt-1 appearance-none relative block w-full px-4 py-3 bg-gray-100 text-gray-800 placeholder-gray-500 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="user@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                  Password
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  className="mt-1 appearance-none relative block w-full px-4 py-3 bg-gray-100 text-gray-800 placeholder-gray-500 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                  placeholder="Your Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            <div className="flex items-center justify-between">
              <button
                type="submit"
                disabled={loading}
                className={`group relative w-32 flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white ${loading ? 'bg-gray-500' : 'bg-gray-900 hover:bg-gray-800'} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500`}
              >
                {loading ? 'Signing in...' : 'Sign In Here'}
              </button>
              <div className="text-sm">
                <Link href="/forgot-password" className="font-medium text-gray-600 hover:text-gray-900">
                  Lost your password?
                </Link>
              </div>
            </div>
            
            <div className="mt-6 flex items-center justify-center">
              <span className="absolute bg-white px-4 text-sm text-gray-500">Or continue with</span>
              <div className="w-full border-t border-gray-300"></div>
            </div>
            
            <div>
              <button
                type="button"
                onClick={handleGoogleSignIn}
                disabled={loading}
                className={`w-full flex justify-center items-center py-3 px-4 border border-gray-700 rounded-md shadow-sm bg-gray-800 text-white ${loading ? 'opacity-70' : 'hover:bg-gray-700'} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500`}
              >
                <svg className="h-5 w-5 mr-2" viewBox="0 0 24 24" width="24" height="24" xmlns="http://www.w3.org/2000/svg">
                  <g transform="matrix(1, 0, 0, 1, 27.009001, -39.238998)">
                    <path fill="#4285F4" d="M -3.264 51.509 C -3.264 50.719 -3.334 49.969 -3.454 49.239 L -14.754 49.239 L -14.754 53.749 L -8.284 53.749 C -8.574 55.229 -9.424 56.479 -10.684 57.329 L -10.684 60.329 L -6.824 60.329 C -4.564 58.239 -3.264 55.159 -3.264 51.509 Z" />
                    <path fill="#34A853" d="M -14.754 63.239 C -11.514 63.239 -8.804 62.159 -6.824 60.329 L -10.684 57.329 C -11.764 58.049 -13.134 58.489 -14.754 58.489 C -17.884 58.489 -20.534 56.379 -21.484 53.529 L -25.464 53.529 L -25.464 56.619 C -23.494 60.539 -19.444 63.239 -14.754 63.239 Z" />
                    <path fill="#FBBC05" d="M -21.484 53.529 C -21.734 52.809 -21.864 52.039 -21.864 51.239 C -21.864 50.439 -21.724 49.669 -21.484 48.949 L -21.484 45.859 L -25.464 45.859 C -26.284 47.479 -26.754 49.299 -26.754 51.239 C -26.754 53.179 -26.284 54.999 -25.464 56.619 L -21.484 53.529 Z" />
                    <path fill="#EA4335" d="M -14.754 43.989 C -12.984 43.989 -11.404 44.599 -10.154 45.789 L -6.734 42.369 C -8.804 40.429 -11.514 39.239 -14.754 39.239 C -19.444 39.239 -23.494 41.939 -25.464 45.859 L -21.484 48.949 C -20.534 46.099 -17.884 43.989 -14.754 43.989 Z" />
                  </g>
                </svg>
                Sign in with Google
              </button>
            </div>
          </form>
          
          {/* Footer info */}
          <div className="pt-8 mt-8 border-t border-gray-200">
            <div className="flex justify-center">
              <Link href="https://melian.health" className="text-xs text-gray-400">
                www.melian.health
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
