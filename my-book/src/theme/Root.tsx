
import React from 'react';
import Chatbot from '@site/src/components/Chatbot';
import { AuthProvider } from '@site/src/contexts/AuthContext';

export default function Root({children}) {
  return (
    <AuthProvider>
      {children}
      <Chatbot />
    </AuthProvider>
  );
}
