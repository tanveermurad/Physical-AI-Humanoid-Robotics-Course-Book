import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

interface PersonalizeChapterProps {
  chapter: string;
  topic: string;
}

export default function PersonalizeChapterWrapper(props: PersonalizeChapterProps) {
  return (
    <BrowserOnly fallback={<div>Loading personalization...</div>}>
      {() => {
        const PersonalizeChapter = require('./index').default;
        return <PersonalizeChapter {...props} />;
      }}
    </BrowserOnly>
  );
}
