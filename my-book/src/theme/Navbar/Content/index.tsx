import React from 'react';
import Content from '@theme-original/Navbar/Content';
import AuthNav from '../../../components/AuthNav';

export default function ContentWrapper(props) {
  return (
    <>
      <Content {...props} />
      <AuthNav />
    </>
  );
}
