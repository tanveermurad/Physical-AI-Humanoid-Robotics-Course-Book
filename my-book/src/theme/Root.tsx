
import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

export default function Root({children}) {
  return (
    <>
      <BrowserOnly fallback={<>{children}</>}>
        {() => {
          try {
            const { AuthProvider } = require('@site/src/contexts/AuthContext');
            const Chatbot = require('@site/src/components/Chatbot').default;

            return (
              <AuthProvider>
                {children}
                <Chatbot />
              </AuthProvider>
            );
          } catch (error) {
            console.error('Failed to load auth/chatbot:', error);
            return <>{children}</>;
          }
        }}
      </BrowserOnly>
    </>
  );
}
