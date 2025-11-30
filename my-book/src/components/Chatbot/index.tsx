import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import './styles.css'; // Import the CSS file for styling

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  source_documents?: string[];
}

interface ChatRequest {
  message: string;
  chat_history?: ChatMessage[];
  selected_text?: string | null;
  user_profile?: any;
  user_id?: string | null;
}

interface ChatResponse {
  response: string;
  source_documents: string[];
  chat_history: ChatMessage[];
}

const Chatbot: React.FC = () => {
  const { user } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedText, setSelectedText] = useState('');
  const [hasSelection, setHasSelection] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const API_BASE_URL = typeof window !== 'undefined'
    ? (process.env.FRONTEND_API_BASE_URL || 'http://localhost:8000')
    : 'http://localhost:8000';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Capture text selection when chatbot opens
  const handleChatbotOpen = () => {
    setIsOpen(true);

    // Capture any selected text when opening
    const selection = window.getSelection();
    const text = selection?.toString().trim();

    if (text && text.length > 10) {
      setSelectedText(text);
      setHasSelection(true);
    }
  };

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

      // Build user profile for personalization
      const userProfile = user ? {
        programmingExperience: user.programmingExperience,
        rosExperience: user.rosExperience,
        aiMlExperience: user.aiMlExperience,
        roboticsExperience: user.roboticsExperience,
        learningGoals: user.learningGoals,
        preferredDifficulty: user.preferredDifficulty
      } : null;

      const requestBody: ChatRequest = {
        message: inputMessage,
        chat_history: chatHistoryForRequest,
        selected_text: hasSelection ? selectedText : null,
        user_profile: userProfile,
        user_id: user?.id || null,
      };

      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Something went wrong with the API request.');
      }

      const data: ChatResponse = await response.json();
      setMessages(data.chat_history);

      // Clear selection after using it
      if (hasSelection) {
        setSelectedText('');
        setHasSelection(false);
      }
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
      <button className="chatbot-toggle-button" onClick={handleChatbotOpen}>
        {isOpen ? 'Close Chat' : 'Open Chat'}
      </button>
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <h3>Book Assistant</h3>
            <button className="chatbot-close-button" onClick={() => setIsOpen(false)}>×</button>
          </div>
          <div className="chatbot-messages">
            {hasSelection && (
              <div className="selected-text-banner">
                <div className="banner-header">
                  <span>📌 Selected Text</span>
                  <button
                    className="banner-close"
                    onClick={() => {
                      setSelectedText('');
                      setHasSelection(false);
                    }}
                  >
                    ✕
                  </button>
                </div>
                <div className="banner-text">
                  {selectedText.substring(0, 150)}
                  {selectedText.length > 150 && '...'}
                </div>
                <p className="banner-hint">
                  Your question will be answered in the context of this selected text
                </p>
              </div>
            )}
            {messages.length === 0 && !isLoading && !error && (
              <div className="chatbot-welcome-message">
                {user
                  ? `Hi ${user.name}! Ask me anything about the book.`
                  : 'Hi there! Ask me anything about the book. Sign in for personalized responses.'}
              </div>
            )}
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                <div className="message-content">{msg.content}</div>
                {msg.role === 'assistant' && (msg as any).source_documents && (msg as any).source_documents.length > 0 && (
                  <div className="source-documents-container">
                    <details>
                      <summary>Source Documents</summary>
                      <ul className="source-documents-list">
                        {(msg as any).source_documents.map((doc: string, docIndex: number) => (
                          <li key={docIndex}>{doc}</li>
                        ))}
                      </ul>
                    </details>
                  </div>
                )}
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