import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import styles from './styles.module.css';

export default function AuthNav() {
  const { user, loading } = useAuth();

  if (loading) {
    return null;
  }

  if (!user) {
    return (
      <div className={styles.authNav}>
        <a href="/signin" className={styles.link}>Sign In</a>
        <a href="/signup" className={styles.linkPrimary}>Sign Up</a>
      </div>
    );
  }

  return (
    <div className={styles.authNav}>
      <span className={styles.welcome}>Welcome, {user.name}!</span>
      <a href="/profile" className={styles.link}>Profile</a>
    </div>
  );
}
