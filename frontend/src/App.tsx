import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { openDB } from 'idb';
import Recorder from './components/Recorder';
import ChatBubble from './components/ChatBubble';

// Define types for chat messages
interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: number;
  source?: string;
  latency?: number;
}

// Database name and version
const DB_NAME = 'swarai-db';
const DB_VERSION = 1;

const App: React.FC = () => {
  // State for chat messages
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  // State for recording status
  const [isRecording, setIsRecording] = useState<boolean>(false);
  // State for loading status (when waiting for AI response)
  const [isLoading, setIsLoading] = useState<boolean>(false);
  // State for online status
  const [isOnline, setIsOnline] = useState<boolean>(navigator.onLine);

  // Initialize IndexedDB
  useEffect(() => {
    const initDB = async () => {
      const db = await openDB(DB_NAME, DB_VERSION, {
        upgrade(db) {
          // Create a store for chat messages
          db.createObjectStore('messages', { keyPath: 'id' });
        },
      });
      
      // Load stored messages from IndexedDB
      const storedMessages = await db.getAll('messages');
      if (storedMessages.length > 0) {
        setMessages(storedMessages);
      }
    };
    
    initDB();
    
    // Set up online/offline event listeners
    window.addEventListener('online', () => setIsOnline(true));
    window.addEventListener('offline', () => setIsOnline(false));
    
    return () => {
      window.removeEventListener('online', () => setIsOnline(true));
      window.removeEventListener('offline', () => setIsOnline(false));
    };
  }, []);

  // Save messages to IndexedDB when messages change
  useEffect(() => {
    const saveMessages = async () => {
      if (messages.length === 0) return;
      
      const db = await openDB(DB_NAME, DB_VERSION);
      const tx = db.transaction('messages', 'readwrite');
      
      messages.forEach(message => {
        tx.store.put(message);
      });
      
      await tx.done;
    };
    
    saveMessages();
  }, [messages]);

  // Handle transcription from Recorder component
  const handleTranscription = async (text: string) => {
    if (!text.trim()) return;
    
    // Add user message to chat
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      timestamp: Date.now(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    
    try {
      // Send query to backend API
      const response = await axios.post('http://localhost:8000/ask', {
        query: text
      });
      
      // Calculate latency (unused for now, but available for future use)
      // const latency = Date.now() - startTime;
      
      // Add AI response to chat
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: response.data.response,
        sender: 'ai',
        timestamp: Date.now(),
        source: response.data.source,
        latency: response.data.latency_ms
      };
      
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error getting AI response:', error);
      
      // Add error message to chat
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I couldn\'t process your request. Please try again later.',
        sender: 'ai',
        timestamp: Date.now(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Clear all messages
  const clearMessages = async () => {
    setMessages([]);
    
    // Clear messages from IndexedDB
    const db = await openDB(DB_NAME, DB_VERSION);
    const tx = db.transaction('messages', 'readwrite');
    await tx.store.clear();
    await tx.done;
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-primary text-white p-4 shadow-md">
        <div className="max-w-3xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">SwarAI</h1>
          <div className="flex items-center gap-2">
            <span className={`h-3 w-3 rounded-full ${isOnline ? 'bg-green-400' : 'bg-red-500'}`}></span>
            <span className="text-sm">{isOnline ? 'Online' : 'Offline'}</span>
            <button 
              onClick={clearMessages}
              className="ml-4 bg-primary-dark hover:bg-primary-light rounded px-3 py-1 text-sm transition"
            >
              Clear Chat
            </button>
          </div>
        </div>
      </header>
      
      {/* Chat area */}
      <main className="flex-1 overflow-auto p-4">
        <div className="chat-container flex flex-col h-full">
          {/* Messages */}
          <div className="flex-1 overflow-auto mb-4 space-y-4">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 mt-8">
                <p className="text-lg">Welcome to SwarAI!</p>
                <p className="mt-2">Press the microphone button and start speaking.</p>
              </div>
            ) : (
              messages.map(message => (
                <ChatBubble
                  key={message.id}
                  message={message.text}
                  sender={message.sender}
                  source={message.source}
                  latency={message.latency}
                />
              ))
            )}
            {isLoading && (
              <div className="flex justify-center items-center mt-4">
                <div className="animate-bounce-slow h-2 w-2 bg-primary rounded-full mx-1"></div>
                <div className="animate-bounce-slow h-2 w-2 bg-primary rounded-full mx-1" style={{ animationDelay: '0.2s' }}></div>
                <div className="animate-bounce-slow h-2 w-2 bg-primary rounded-full mx-1" style={{ animationDelay: '0.4s' }}></div>
              </div>
            )}
          </div>
          
          {/* Voice recorder */}
          <div className="sticky bottom-0 bg-white rounded-lg shadow-lg p-4 border border-gray-200">
            <Recorder
              isRecording={isRecording}
              onRecordingChange={setIsRecording}
              onTranscription={handleTranscription}
            />
          </div>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="bg-gray-100 text-center p-2 text-sm text-gray-600">
        <p>SwarAI - Voice-enabled AI assistant with hybrid LLM support</p>
      </footer>
    </div>
  );
};

export default App;