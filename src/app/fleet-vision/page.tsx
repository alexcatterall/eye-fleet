'use client';
import React, { useEffect, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import BackButton from '@/components/BackButton';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

// Ensure Mapbox access token is set
mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN || '';

const FleetVision = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [contextMessages, setContextMessages] = useState<string[]>([]);

  React.useEffect(() => {
    const map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [-74.5, 40], // Starting position [lng, lat]
      zoom: 9 // Starting zoom
    });

    return () => map.remove();
  }, []);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    const newMessage: Message = { role: 'user', content: inputMessage };
    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');
    setIsGenerating(true);

    try {
      const response = await fetch('http://localhost:5328/ollama_api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: [...messages, newMessage],
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate response');
      }

      const data = await response.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.generated_text }]);
    } catch (error) {
      console.error('Error generating response:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handlePushToContext = (message: string) => {
    setContextMessages(prev => [...prev, message]);
  };

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div id="map" style={{ flex: 1 }}></div>
      
      {/* Chat Interface */}
      <div className="w-96 bg-white dark:bg-gray-800 shadow-lg flex flex-col border-l border-gray-200 dark:border-gray-700">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white">Fleet Assistant</h2>
        </div>

        {/* Chat Section */}
        <div className="flex-1 flex flex-col h-1/2 border-b border-gray-200 dark:border-gray-700">
          <div className="flex-1 p-4 overflow-y-auto space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className="flex flex-col">
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-2 ${
                      message.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white'
                    }`}
                  >
                    {message.content}
                  </div>
                  {message.role === 'assistant' && (
                    <button
                      onClick={() => handlePushToContext(message.content)}
                      className="text-sm text-blue-600 dark:text-blue-400 mt-1 hover:underline"
                    >
                      Push to Context
                    </button>
                  )}
                </div>
              </div>
            ))}
            {isGenerating && (
              <div className="flex justify-start">
                <div className="bg-gray-100 dark:bg-gray-700 rounded-lg px-4 py-2">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="p-4 border-t border-gray-200 dark:border-gray-700">
            <div className="flex space-x-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Ask about fleet locations..."
                className="flex-1 rounded-lg border border-gray-300 dark:border-gray-600 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
              />
              <button
                onClick={handleSendMessage}
                disabled={isGenerating || !inputMessage.trim()}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Send
              </button>
            </div>
          </div>
        </div>

        {/* Context Section */}
        <div className="flex-1 h-1/2 p-4 overflow-y-auto">
          <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-4">Context</h3>
          <div className="space-y-4 text-gray-600 dark:text-gray-300">
            {contextMessages.map((context, index) => (
              <div key={index} className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
                <p className="text-sm">{context}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
      <BackButton />
    </div>
  );
};

export default FleetVision;