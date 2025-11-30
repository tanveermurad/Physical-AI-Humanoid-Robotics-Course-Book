import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';

interface TranslateChapterProps {
  chapter: string;
  title: string;
  contentSelector?: string;
}

export default function TranslateChapterWrapper(props: TranslateChapterProps) {
  return (
    <BrowserOnly fallback={<div>Loading translation...</div>}>
      {() => {
        const TranslateChapter = require('./index').default;
        return <TranslateChapter {...props} />;
      }}
    </BrowserOnly>
  );
}
