"use client";

import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Mic } from 'lucide-react';

type Message = {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
};

const Onboarding = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: 'Hi there! I\'m your AI health coach. I\'ll help you set up your profile. Let\'s start with your name.',
      role: 'assistant',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Mock function to simulate AI responses
  const mockAIResponse = async (userMessage: string): Promise<string> => {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Simple mock responses based on user input
    if (userMessage.toLowerCase().includes('name')) {
      return 'Great! Now, can you tell me your fitness goals?';
    } else if (userMessage.toLowerCase().includes('goal') || userMessage.toLowerCase().includes('fitness')) {
      return 'Excellent! How would you describe your current activity level?';
    } else if (userMessage.toLowerCase().includes('activity') || userMessage.toLowerCase().includes('level')) {
      return 'Thanks! What about your dietary preferences?';
    } else if (userMessage.toLowerCase().includes('diet') || userMessage.toLowerCase().includes('food')) {
      return 'Perfect! I\'ve created your profile. I\'ll now redirect you to your dashboard where you can start your health journey!';
    } else {
      return 'Tell me more about your health and fitness goals so I can customize your experience.';
    }
  };

  // Mock function to create user profile
  const createUserProfile = async (messages: Message[]) => {
    // In a real implementation, this would call a backend API
    console.log('Creating user profile based on chat:', messages);
    return { success: true };
  };

  // Mock function to redirect to dashboard
  const redirectToDashboard = () => {
    // In a real implementation, this would redirect to the dashboard
    console.log('Redirecting to dashboard...');
    // window.location.href = '/dashboard';
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Get AI response
      const aiResponse = await mockAIResponse(input);
      
      // Add AI message
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: aiResponse,
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);

      // Check if this is the last step in the onboarding process
      if (aiResponse.includes('redirect you to your dashboard')) {
        await createUserProfile(messages);
        // Add slight delay before redirect for user to read the message
        setTimeout(redirectToDashboard, 3000);
      }
    } catch (error) {
      console.error('Error getting AI response:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div 
      className="flex flex-col items-center justify-center min-h-screen bg-cover bg-center bg-no-repeat p-4"
      style={{ backgroundImage: "url('/images/onboarding-bg.jpg')" }}
    >
      {/* Chat History Container */}
      <div className="w-[90%] max-w-3xl h-[70vh] bg-white/20 backdrop-blur-md rounded-3xl overflow-hidden shadow-2xl border border-white/30 mb-4">
        {/* Chat Container */}
        <div className="flex-1 overflow-y-auto p-6 h-full space-y-5">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {message.role === 'assistant' && (
                <div className="h-10 w-10 rounded-full bg-emerald-500/70 mr-3 flex items-center justify-center">
                  <span className="text-white text-sm font-bold">Agent</span>
                </div>
              )}
              <div
                className={`max-w-[70%] p-3.5 rounded-2xl ${message.role === 'user'
                  ? 'bg-blue-600/90 backdrop-blur-sm text-white rounded-tr-none'
                  : 'bg-white/20 backdrop-blur-sm border border-white/30 text-white rounded-tl-none'
                  }`}
              >
                <p className="leading-relaxed">{message.content}</p>
                <span className="text-xs opacity-70 block mt-2">
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              {message.role === 'user' && (
                <div className="h-10 w-10 rounded-full bg-blue-500/70 ml-3 flex items-center justify-center">
                  <span className="text-white text-sm font-bold">You</span>
                </div>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Message Input - Separated from chat history */}
      <div className="w-[85%] max-w-2xl bg-white/25 backdrop-blur-lg rounded-full overflow-hidden shadow-xl border border-white/30">
        <div className="flex items-center px-3 py-1">
          <div className="flex-1 relative">
            <Input
              placeholder="Type your message..."
              value={input}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInput(e.target.value)}
              onKeyPress={(e: React.KeyboardEvent<HTMLInputElement>) => e.key === 'Enter' && handleSendMessage()}
              disabled={isLoading}
              className="w-full bg-transparent border-0 text-white placeholder-white/70 py-3 px-3 focus:outline-none"
            />
            <Button 
              variant="outline"
              size="icon"
              className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-transparent border-0 hover:bg-white/20 text-white"
            >
              <Mic className="h-5 w-5 opacity-70" />
            </Button>
          </div>
          <Button 
            onClick={handleSendMessage} 
            disabled={isLoading || !input.trim()}
            className="rounded-full h-12 w-12 bg-blue-600/90 hover:bg-blue-700 text-white flex items-center justify-center"
            size="icon"
          >
            <Send className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Onboarding;