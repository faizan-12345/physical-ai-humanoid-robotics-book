import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import Chatbot from '../components/Chatbot'; // Import the Chatbot component

// Define a fixed position for the chatbot (e.g., bottom right corner)
const chatbotStyle = {
  position: 'fixed',
  bottom: '20px',
  right: '20px',
  zIndex: 1000, // Ensure it appears above other elements
  width: '350px', // Adjust width as needed
  height: '500px', // Adjust height as needed
};

const Layout = (props) => {
  return (
    <>
      <OriginalLayout {...props} />
      {/* Render the Chatbot component in a fixed position */}
      <div style={chatbotStyle}>
        <Chatbot />
      </div>
    </>
  );
};

export default Layout;
