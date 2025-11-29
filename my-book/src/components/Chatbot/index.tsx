
import React, { useState } from 'react';
import './styles.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (input.trim()) {
      const userMessage = { text: input, sender: 'user' };
      setMessages(prevMessages => [...prevMessages, userMessage]);
      setInput('');

      try {
        const response = await fetch('http://localhost:8000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: input }),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        const botMessage = { text: data.response, sender: 'bot' };
        setMessages(prevMessages => [...prevMessages, botMessage]);
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        const errorMessage = { text: 'Sorry, something went wrong.', sender: 'bot' };
        setMessages(prevMessages => [...prevMessages, errorMessage]);
      }
    }
  };

  return (
    <div className="chatbot">
      <div className="chatbot-header">
        <h2>Chatbot</h2>
      </div>
      <div className="chatbot-messages">
        {messages.map((message, index) => (
          <div key={index} className={`chatbot-message ${message.sender}`}>
            {message.text}
          </div>
        ))}
      </div>
      <div className="chatbot-input">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyPress={e => e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
