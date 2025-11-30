import React from 'react';

export default function Root({children}) {
  // Only load auth/chatbot in browser, not during SSR build
  if (typeof window === 'undefined') {
    return <>{children}</>;
  }

  // Dynamically import only in browser
  const BrowserOnly = require('@docusaurus/BrowserOnly').default;

  return (
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
  );
}
