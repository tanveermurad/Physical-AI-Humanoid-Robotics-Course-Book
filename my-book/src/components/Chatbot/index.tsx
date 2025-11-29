import React, { useState } from 'react';
import Layout from '@theme/Layout';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (input.trim() === '') return;

    const userMessage: Message = { text: input, sender: 'user' };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', { // Assuming API runs on port 8000
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });
      const data = await response.json();
      const botMessage: Message = { text: data.response, sender: 'bot' };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = { text: 'Sorry, something went wrong.', sender: 'bot' };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', border: '1px solid #ddd', borderRadius: '8px', display: 'flex', flexDirection: 'column', height: '70vh' }}>
      <h2 style={{ textAlign: 'center', marginBottom: '20px' }}>Book Chatbot</h2>
      <div style={{ flexGrow: 1, overflowY: 'auto', border: '1px solid #eee', padding: '10px', borderRadius: '4px', marginBottom: '10px' }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: '10px', textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
            <span
              style={{
                display: 'inline-block',
                padding: '8px 12px',
                borderRadius: '18px',
                backgroundColor: msg.sender === 'user' ? '#007bff' : '#f0f0f0',
                color: msg.sender === 'user' ? 'white' : '#333',
                maxWidth: '70%',
                wordWrap: 'break-word',
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}
        {loading && (
          <div style={{ textAlign: 'left', marginBottom: '10px' }}>
            <span style={{ display: 'inline-block', padding: '8px 12px', borderRadius: '18px', backgroundColor: '#f0f0f0', color: '#333' }}>
              Typing...
            </span>
          </div>
        )}
      </div>
      <div style={{ display: 'flex' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !loading) {
              sendMessage();
            }
          }}
          placeholder="Ask a question about the book..."
          style={{ flexGrow: 1, padding: '10px', border: '1px solid #ddd', borderRadius: '4px', marginRight: '10px' }}
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          style={{ padding: '10px 15px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
          disabled={loading}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default Chatbot;