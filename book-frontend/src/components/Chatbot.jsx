import React, { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

// Define the backend API URL as a constant
// This can be changed to point to a different server if needed
const BACKEND_API_URL = 'http://localhost:8000';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef(null);

  // Function to scroll to the bottom of the chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Function to handle sending a message to the backend
  const sendMessage = async (messageText, isQueryingSelectedText = false) => {
    if (!messageText.trim() || isLoading) return;

    setIsLoading(true);

    // Add user message to the chat
    const userMessage = { text: messageText, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);

    try {
      let response;
      if (isQueryingSelectedText && selectedText) {
        // Use the /selected-text-query endpoint
        response = await fetch(`${BACKEND_API_URL}/selected-text-query`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: messageText,
            selected_text: selectedText,
          }),
        });
      } else {
        // Use the standard /query endpoint
        response = await fetch(`${BACKEND_API_URL}/query`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: messageText,
          }),
        });
      }

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      // Add bot response to the chat
      const botMessage = { text: data.answer, sender: 'bot' };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = { text: `Error: ${error.message}`, sender: 'bot' };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setInputValue(''); // Clear the input field after sending
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(inputValue, false); // Standard query
  };

  const handleSelectedTextQuery = () => {
    if (!selectedText) {
      alert('Please select some text on the page first.');
      return;
    }
    sendMessage(inputValue, true); // Query with selected text
  };

  // Function to get selected text from the page (basic implementation)
  const getSelectedText = () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      setSelectedText(selectedText);
      alert(`Selected text captured: "${selectedText.substring(0, 50)}..."`); // Inform user briefly
    } else {
      alert('No text selected. Please select some text on the page.');
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h3>Humanoid Robotics Book Chat</h3>
        <button onClick={getSelectedText} className="select-text-btn" title="Select text on the page for context-specific queries">
          Use Selected Text
        </button>
      </div>
      <div className="chatbot-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <div className="message-text">{msg.text}</div>
          </div>
        ))}
        {isLoading && <div className="message bot"><div className="message-text typing-indicator">Typing...</div></div>}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="chatbot-input-form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask a question about the book..."
          disabled={isLoading}
          className="chatbot-input"
        />
        <button type="submit" disabled={isLoading} className="chatbot-send-btn">
          Send
        </button>
        {selectedText && (
          <button type="button" onClick={handleSelectedTextQuery} disabled={isLoading} className="chatbot-selected-text-btn">
            Ask about Selected
          </button>
        )}
      </form>
    </div>
  );
};

export default Chatbot;
