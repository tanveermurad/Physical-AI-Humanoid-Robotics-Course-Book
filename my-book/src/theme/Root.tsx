
import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

export default function Root({children}) {
  return (
    <BrowserOnly fallback={<div>{children}</div>}>
      {() => {
        const { AuthProvider } = require('@site/src/contexts/AuthContext');
        const Chatbot = require('@site/src/components/Chatbot').default;

        return (
          <AuthProvider>
            {children}
            <Chatbot />
          </AuthProvider>
        );
      }}
    </BrowserOnly>
  );
}
