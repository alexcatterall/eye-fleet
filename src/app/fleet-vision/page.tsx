'use client';
import React, { useEffect, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import { toast } from 'sonner';
import BackButton from '@/components/BackButton';
import { usePlayer } from '@/lib/usePlayer';
import 'mapbox-gl/dist/mapbox-gl.css';

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
  const [selectedAgent, setSelectedAgent] = useState('livetracking agent');
  const [scratchpadInput, setScratchpadInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);

  const player = usePlayer();

  // Convert audio blob to base64
  const blobToBase64 = (blob: Blob): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        if (typeof reader.result === 'string') {
          resolve(reader.result.split(',')[1]);
        }
      };
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  };

  // Handle speech-to-text conversion
  const handleSpeechToText = async (blob: Blob) => {
    const formData = new FormData();
    formData.append('file', blob, 'audio.wav');
    formData.append('model', 'whisper-1');
    
    console.log('my openai key is :', process.env.OPENAI_API_KEY);
    try {
      const response = await fetch('https://api.openai.com/v1/audio/transcriptions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.NEXT_PUBLIC_OPENAI_API_KEY}`,
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error('Speech to text conversion failed');
      }

      const data = await response.json();
      return data.text;
    } catch (error) {
      console.error('STT error:', error);
      throw error;
    }
  };

  // Handle text-to-speech conversion
  const handleTextToSpeech = async (text: string) => {
    try {
      const response = await fetch("https://api.cartesia.ai/tts/bytes", {
        method: "POST",
        headers: {
          "Cartesia-Version": "2024-06-30",
          "Content-Type": "application/json",
          "X-API-Key":  'sk_car_AOkmSi_cxx42tGW_5jYsq',
        },
        body: JSON.stringify({
          model_id: "sonic-english",
          transcript: text,
          voice: {
            mode: "id",
            id: "79a125e8-cd45-4c13-8a67-188112f4dd22",
          },
          output_format: {
            container: "raw",
            encoding: "pcm_f32le",
            sample_rate: 24000,
          },
        }),
      });

      if (!response.ok) {
        throw new Error('Text to speech conversion failed');
      }

      return response.body;
    } catch (error) {
      console.error('TTS error:', error);
      throw error;
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks: BlobPart[] = [];

      recorder.ondataavailable = (e) => chunks.push(e.data);
      
      recorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/wav' });
        
        try {
          // Convert speech to text
          const text = await handleSpeechToText(audioBlob);
          setInputMessage(text);

          // Send text to backend
          const url = `http://localhost:8000/api/${selectedAgent.split(' ')[0]}/agent/chat/`;
          const response = await fetch(url, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              message: text
            }),
          });

          if (!response.ok) {
            throw new Error('Failed to generate response');
          }

          const data = await response.json();

          // Update messages
          setMessages(prev => [
            ...prev,
            { role: 'user', content: text },
            { role: 'assistant', content: data.response }
          ]);

          // Convert response to speech and play
          const audioStream = await handleTextToSpeech(data.response);
          if (audioStream) {
            await player.play(audioStream, () => {
              console.log('Audio playback completed');
            });
          }

        } catch (error) {
          console.error('Processing error:', error);
          toast.error('Speech processing failed');
        }
      };

      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
    } catch (error) {
      console.error('Error starting recording:', error);
      toast.error('Could not start recording');
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop();
      setIsRecording(false);
      // Stop all audio tracks
      mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
  };

  React.useEffect(() => {
    // Initialize map with default center
    const map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [-74.5, 40], // Default position [lng, lat]
      zoom: 15
    });

    // Function to generate random points around a center
    const generateRandomPoints = (center: [number, number], count: number, radius: number) => {
      const points: [number, number][] = [];
      for (let i = 0; i < count; i++) {
        // Convert radius from kilometers to degrees
        const radiusInDeg = radius / 111.32;
        // Generate random angle and distance
        const angle = Math.random() * 2 * Math.PI;
        const distance = Math.random() * radiusInDeg;
        // Calculate offset
        const dx = distance * Math.cos(angle);
        const dy = distance * Math.sin(angle);
        // Add offset to center
        points.push([
          center[0] + dx,
          center[1] + dy
        ]);
      }
      return points;
    };

    // Create custom marker element for fleet vehicles
    const createMarkerElement = () => {
      const element = document.createElement('div');
      element.className = 'custom-marker';
      element.style.width = '30px';
      element.style.height = '30px';
      element.style.backgroundImage = `url(/icons/${['car', 'drone', 'robot'][Math.floor(Math.random() * 3)]}.png)`;
      element.style.backgroundSize = 'contain';
      element.style.backgroundRepeat = 'no-repeat';
      element.style.backgroundPosition = 'center';
      element.style.borderRadius = '50%';
      element.style.border = '2px solid #fff';
      element.style.boxShadow = '0 0 10px rgba(0,0,0,0.3)';
      element.style.cursor = 'pointer';
      return element;
    };

    // Function to add fleet markers
    const addFleetMarkers = (center: [number, number]) => {
      const points = generateRandomPoints(center, 10, 2); // 2km radius
      points.forEach((point, index) => {
        const markerElement = createMarkerElement();
        new mapboxgl.Marker({
          element: markerElement,
          anchor: 'bottom'
        })
          .setLngLat(point)
          .setPopup(new mapboxgl.Popup().setHTML(`<h3>Fleet Vehicle ${index + 1}</h3><p>Random Location</p>`))
          .addTo(map);
      });
    };

    // Wait for map to load before getting user location
    map.on('load', () => {
      // Get user's location and update map center
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const { longitude, latitude } = position.coords;
            map.setCenter([longitude, latitude]);
            
            // Create custom marker for user location
            const userMarkerElement = document.createElement('div');
            userMarkerElement.className = 'user-marker';
            userMarkerElement.style.width = '30px';
            userMarkerElement.style.height = '30px';
            userMarkerElement.style.backgroundImage = `url(/icons/${['car', 'drone', 'robot'][Math.floor(Math.random() * 3)]}.png)`;
            userMarkerElement.style.backgroundSize = 'contain';
            userMarkerElement.style.backgroundColor = '#4A90E2';
            userMarkerElement.style.borderRadius = '50%';
            userMarkerElement.style.border = '3px solid #fff';
            userMarkerElement.style.boxShadow = '0 0 10px rgba(0,0,0,0.3)';

            // Add marker at user's location with custom element
            new mapboxgl.Marker({
              element: userMarkerElement,
              anchor: 'center'
            })
              .setLngLat([longitude, latitude])
              .setPopup(new mapboxgl.Popup().setHTML("<h3>Focus Asset</h3>"))
              .addTo(map);

            // Generate fleet markers around user location
            addFleetMarkers([longitude, latitude]);
          },
          (error) => {
            console.error("Error getting location:", error);
            // If location access fails, use default location
            addFleetMarkers([-74.5, 40]);
          }
        );
      } else {
        // If geolocation not supported, use default location
        addFleetMarkers([-74.5, 40]);
      }
    });

    return () => map.remove();
  }, []);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;
    
    const newMessage: Message = { role: 'user', content: inputMessage };
    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');
    setIsGenerating(true);
    let url = '';

    if(selectedAgent === 'livetracking agent'){
      url = 'http://localhost:8000/api/livetracking/agent/chat/'
    }
    else if (selectedAgent === 'maintenance agent'){
      url = 'http://localhost:8000/api/maintenance/agent/chat/'
    }
    else if (selectedAgent === 'scheduling agent'){
      url = 'http://localhost:8000/api /scheduling/agent/chat/'
    }
    else{
      console.log('No agent selected')
    }

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate response');
      }

      const data = await response.json();
      console.log('Response from llm server :', data);

      // Convert response to speech
      const audioStream = await handleTextToSpeech(data.response);
      if (audioStream) {
        await player.play(audioStream, () => {
          console.log('Audio playback completed');
        });
      }

      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      console.error('Error generating response:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handlePushToContext = (message: string) => {
    setContextMessages(prev => [...prev, message]);
  };

  const handleAddToScratchpad = () => {
    if (scratchpadInput.trim()) {
      setContextMessages(prev => [...prev, scratchpadInput]);
      setScratchpadInput('');
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div id="map" style={{ flex: 1 }}></div>
      
      {/* Chat Interface */}
      <div className="w-96 bg-white dark:bg-gray-800 shadow-lg flex flex-col border-l border-gray-200 dark:border-gray-700">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white">Fleet Assistant</h2>
          <select 
            value={selectedAgent}
            onChange={(e) => setSelectedAgent(e.target.value)}
            className="px-3 py-1 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="livetracking agent">Livetracking Agent</option>
            <option value="maintenance agent">Maintenance Agent</option>
            <option value="scheduling agent">Scheduling Agent</option>
          </select>
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
                placeholder="Ask about your fleet..."
                className="flex-1 rounded-lg border border-gray-300 dark:border-gray-600 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
              />
              <button
                onClick={isRecording ? stopRecording : startRecording}
                className={`w-10 h-10 flex items-center justify-center rounded-full ${isRecording ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'} text-white focus:outline-none focus:ring-2 focus:ring-blue-500`}
              >
                {isRecording ? '⬛' : '🎤'}
              </button>
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
          <h3 className="text-lg font-medium text-gray-800 dark:text-white mb-4">Context Scratch Pad</h3>
          <div className="mb-4 flex space-x-2">
            <input
              type="text"
              value={scratchpadInput}
              onChange={(e) => setScratchpadInput(e.target.value)}
              placeholder="Add a note..."
              className="flex-1 rounded-lg border border-gray-300 dark:border-gray-600 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white text-sm"
            />
            <button
              onClick={handleAddToScratchpad}
              disabled={!scratchpadInput.trim()}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
            >
              Add Note
            </button>
          </div>
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