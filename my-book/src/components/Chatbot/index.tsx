import React, { useState, useRef, useEffect } from 'react';
import './styles.css'; // Import the CSS file for styling

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatRequest {
  message: string;
  chat_history?: ChatMessage[];
}

interface ChatResponse {
  response: string;
  source_documents: string[];
  chat_history: ChatMessage[];
}

const Chatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const API_BASE_URL = 'http://localhost:8000'; // Replace with your FastAPI backend URL in production

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (inputMessage.trim() === '') return;

    setError(null);
    setIsLoading(true);
    const userMessage: ChatMessage = { role: 'user', content: inputMessage };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputMessage('');

    try {
      const chatHistoryForRequest = messages.map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      const requestBody: ChatRequest = {
        message: inputMessage,
        chat_history: chatHistoryForRequest,
      };

      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Something went wrong with the API request.');
      }

      const data: ChatResponse = await response.json();
      setMessages(data.chat_history);
    } catch (err: any) {
      console.error('Error sending message:', err);
      setError(err.message || 'Failed to get response from the chatbot.');
      setMessages((prevMessages) => [
        ...prevMessages,
        { role: 'assistant', content: "Sorry, I'm having trouble right now. Please try again later." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !isLoading) {
      handleSendMessage();
    }
  };

  return (
    <div className={`chatbot-container ${isOpen ? 'open' : ''}`}>
      <button className="chatbot-toggle-button" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? 'Close Chat' : 'Open Chat'}
      </button>
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <h3>Book Assistant</h3>
            <button className="chatbot-close-button" onClick={() => setIsOpen(false)}>×</button>
          </div>
          <div className="chatbot-messages">
            {messages.length === 0 && !isLoading && !error && (
              <div className="chatbot-welcome-message">
                Hi there! Ask me anything about the book.
              </div>
            )}
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                <div className="message-content">{msg.content}</div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant loading">
                <div className="message-content">Typing...</div>
              </div>
            )}
            {error && (
              <div className="message error">
                <div className="message-content">Error: {error}</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <div className="chatbot-input-area">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your question..."
              disabled={isLoading}
            />
            <button onClick={handleSendMessage} disabled={isLoading}>
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;