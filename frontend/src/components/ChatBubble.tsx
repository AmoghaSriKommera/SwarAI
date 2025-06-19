import React from 'react';

interface ChatBubbleProps {
  message: string;
  sender: 'user' | 'ai';
  source?: string;
  latency?: number;
}

const ChatBubble: React.FC<ChatBubbleProps> = ({ 
  message, 
  sender, 
  source, 
  latency 
}) => {
  // Determine bubble styling based on sender
  const bubbleClass = sender === 'user' 
    ? 'chat-bubble user-bubble bg-user-light' 
    : 'chat-bubble ai-bubble bg-ai-light';
  
  return (
    <div className={bubbleClass}>
      <div className="flex flex-col">
        <div className="message-text whitespace-pre-wrap">
          {message}
        </div>
        
        {/* Display metadata for AI messages */}
        {sender === 'ai' && (source || latency) && (
          <div className="metadata mt-2 text-xs text-gray-500 flex items-center">
            {source && (
              <span className="source mr-2">
                Source: <span className="font-medium">{source}</span>
              </span>
            )}
            {latency && (
              <span className="latency">
                Latency: <span className="font-medium">{latency}ms</span>
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatBubble;