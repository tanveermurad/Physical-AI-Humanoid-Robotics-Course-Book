import React from 'react';
import Layout from '@theme/Layout';
import BrowserOnly from '@docusaurus/BrowserOnly';

function ChatbotPage() {
  return (
    <Layout
      title="Chatbot"
      description="Chat with the book content using AI."
    >
      <main>
        <BrowserOnly fallback={<div>Loading chatbot...</div>}>
          {() => {
            const Chatbot = require('../components/Chatbot').default;
            return <Chatbot />;
          }}
        </BrowserOnly>
      </main>
    </Layout>
  );
}

export default ChatbotPage;