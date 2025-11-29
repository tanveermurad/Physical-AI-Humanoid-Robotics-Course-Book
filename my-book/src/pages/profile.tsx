import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../contexts/AuthContext';
import { useHistory } from '@docusaurus/router';
import styles from './profile.module.css';

export default function ProfilePage() {
  const { user, loading, updateProfile, signOut } = useAuth();
  const history = useHistory();
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Form state
  const [programmingExperience, setProgrammingExperience] = useState('');
  const [programmingLanguages, setProgrammingLanguages] = useState<string[]>([]);
  const [aiMlExperience, setAiMlExperience] = useState('');
  const [rosExperience, setRosExperience] = useState('');
  const [roboticsExperience, setRoboticsExperience] = useState('');
  const [hardwareProjects, setHardwareProjects] = useState<string[]>([]);
  const [hasRoboticsHardware, setHasRoboticsHardware] = useState(false);
  const [hardwareDescription, setHardwareDescription] = useState('');
  const [learningGoals, setLearningGoals] = useState<string[]>([]);
  const [preferredDifficulty, setPreferredDifficulty] = useState('');

  useEffect(() => {
    if (!loading && !user) {
      history.push('/signin');
    }
  }, [user, loading, history]);

  useEffect(() => {
    if (user) {
      setProgrammingExperience(user.programmingExperience || '');
      setProgrammingLanguages(user.programmingLanguages || []);
      setAiMlExperience(user.aiMlExperience || '');
      setRosExperience(user.rosExperience || '');
      setRoboticsExperience(user.roboticsExperience || '');
      setHardwareProjects(user.hardwareProjects || []);
      setHasRoboticsHardware(user.hasRoboticsHardware || false);
      setHardwareDescription(user.hardwareDescription || '');
      setLearningGoals(user.learningGoals || []);
      setPreferredDifficulty(user.preferredDifficulty || '');
    }
  }, [user]);

  const handleLanguageToggle = (lang: string) => {
    setProgrammingLanguages(prev =>
      prev.includes(lang) ? prev.filter(l => l !== lang) : [...prev, lang]
    );
  };

  const handleProjectToggle = (project: string) => {
    setHardwareProjects(prev =>
      prev.includes(project) ? prev.filter(p => p !== project) : [...prev, project]
    );
  };

  const handleGoalToggle = (goal: string) => {
    setLearningGoals(prev =>
      prev.includes(goal) ? prev.filter(g => g !== goal) : [...prev, goal]
    );
  };

  const handleSave = async () => {
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      await updateProfile({
        programmingExperience: programmingExperience as any,
        programmingLanguages,
        aiMlExperience: aiMlExperience as any,
        rosExperience: rosExperience as any,
        roboticsExperience: roboticsExperience as any,
        hardwareProjects,
        hasRoboticsHardware,
        hardwareDescription,
        learningGoals,
        preferredDifficulty: preferredDifficulty as any,
      });
      setSuccess('Profile updated successfully!');
      setEditing(false);
    } catch (err) {
      setError(err.message || 'Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleSignOut = async () => {
    await signOut();
    history.push('/');
  };

  if (loading) {
    return (
      <Layout title="Profile">
        <div className={styles.container}>
          <p>Loading...</p>
        </div>
      </Layout>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <Layout title="Profile" description="Manage your profile and learning preferences">
      <div className={styles.container}>
        <div className={styles.profileCard}>
          <div className={styles.header}>
            <div>
              <h1>{user.name}</h1>
              <p className={styles.email}>{user.email}</p>
            </div>
            <div className={styles.headerActions}>
              {!editing ? (
                <button onClick={() => setEditing(true)} className={styles.editButton}>
                  Edit Profile
                </button>
              ) : (
                <>
                  <button onClick={() => setEditing(false)} className={styles.cancelButton}>
                    Cancel
                  </button>
                  <button onClick={handleSave} className={styles.saveButton} disabled={saving}>
                    {saving ? 'Saving...' : 'Save Changes'}
                  </button>
                </>
              )}
              <button onClick={handleSignOut} className={styles.signOutButton}>
                Sign Out
              </button>
            </div>
          </div>

          {error && <div className={styles.error}>{error}</div>}
          {success && <div className={styles.success}>{success}</div>}

          <div className={styles.section}>
            <h2>Software Background</h2>
            <div className={styles.field}>
              <label>Programming Experience</label>
              {editing ? (
                <select value={programmingExperience} onChange={(e) => setProgrammingExperience(e.target.value)}>
                  <option value="">Select...</option>
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                  <option value="expert">Expert</option>
                </select>
              ) : (
                <p>{programmingExperience || 'Not set'}</p>
              )}
            </div>

            <div className={styles.field}>
              <label>Programming Languages</label>
              {editing ? (
                <div className={styles.checkboxGrid}>
                  {['Python', 'C++', 'JavaScript', 'Java', 'C', 'Rust', 'Go'].map(lang => (
                    <label key={lang} className={styles.checkboxLabel}>
                      <input
                        type="checkbox"
                        checked={programmingLanguages.includes(lang)}
                        onChange={() => handleLanguageToggle(lang)}
                      />
                      {lang}
                    </label>
                  ))}
                </div>
              ) : (
                <p>{programmingLanguages.length > 0 ? programmingLanguages.join(', ') : 'Not set'}</p>
              )}
            </div>

            <div className={styles.field}>
              <label>AI/ML Experience</label>
              {editing ? (
                <select value={aiMlExperience} onChange={(e) => setAiMlExperience(e.target.value)}>
                  <option value="">Select...</option>
                  <option value="none">None</option>
                  <option value="basic">Basic</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              ) : (
                <p>{aiMlExperience || 'Not set'}</p>
              )}
            </div>

            <div className={styles.field}>
              <label>ROS Experience</label>
              {editing ? (
                <select value={rosExperience} onChange={(e) => setRosExperience(e.target.value)}>
                  <option value="">Select...</option>
                  <option value="none">None</option>
                  <option value="basic">Basic</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              ) : (
                <p>{rosExperience || 'Not set'}</p>
              )}
            </div>
          </div>

          <div className={styles.section}>
            <h2>Hardware Background</h2>
            <div className={styles.field}>
              <label>Robotics Experience</label>
              {editing ? (
                <select value={roboticsExperience} onChange={(e) => setRoboticsExperience(e.target.value)}>
                  <option value="">Select...</option>
                  <option value="none">None</option>
                  <option value="hobbyist">Hobbyist</option>
                  <option value="student">Student</option>
                  <option value="professional">Professional</option>
                </select>
              ) : (
                <p>{roboticsExperience || 'Not set'}</p>
              )}
            </div>

            <div className={styles.field}>
              <label>Hardware Projects</label>
              {editing ? (
                <div className={styles.checkboxGrid}>
                  {[
                    'Arduino/Raspberry Pi',
                    'Robot Kits',
                    'Custom Robot Builds',
                    '3D Printing',
                    'Microcontrollers',
                    'Sensors & Actuators',
                  ].map(project => (
                    <label key={project} className={styles.checkboxLabel}>
                      <input
                        type="checkbox"
                        checked={hardwareProjects.includes(project)}
                        onChange={() => handleProjectToggle(project)}
                      />
                      {project}
                    </label>
                  ))}
                </div>
              ) : (
                <p>{hardwareProjects.length > 0 ? hardwareProjects.join(', ') : 'Not set'}</p>
              )}
            </div>

            <div className={styles.field}>
              <label>
                {editing ? (
                  <label className={styles.checkboxLabel}>
                    <input
                      type="checkbox"
                      checked={hasRoboticsHardware}
                      onChange={(e) => setHasRoboticsHardware(e.target.checked)}
                    />
                    I have access to robotics hardware
                  </label>
                ) : (
                  <>Has Robotics Hardware: {hasRoboticsHardware ? 'Yes' : 'No'}</>
                )}
              </label>
            </div>

            {hasRoboticsHardware && (
              <div className={styles.field}>
                <label>Hardware Description</label>
                {editing ? (
                  <textarea
                    value={hardwareDescription}
                    onChange={(e) => setHardwareDescription(e.target.value)}
                    rows={3}
                  />
                ) : (
                  <p>{hardwareDescription || 'Not set'}</p>
                )}
              </div>
            )}
          </div>

          <div className={styles.section}>
            <h2>Learning Preferences</h2>
            <div className={styles.field}>
              <label>Learning Goals</label>
              {editing ? (
                <div className={styles.checkboxGrid}>
                  {[
                    'Humanoid Robotics',
                    'ROS 2',
                    'Computer Vision',
                    'Motion Planning',
                    'Simulation (Gazebo/Isaac)',
                    'Physical AI',
                    'Robot Control',
                    'SLAM & Navigation',
                  ].map(goal => (
                    <label key={goal} className={styles.checkboxLabel}>
                      <input
                        type="checkbox"
                        checked={learningGoals.includes(goal)}
                        onChange={() => handleGoalToggle(goal)}
                      />
                      {goal}
                    </label>
                  ))}
                </div>
              ) : (
                <p>{learningGoals.length > 0 ? learningGoals.join(', ') : 'Not set'}</p>
              )}
            </div>

            <div className={styles.field}>
              <label>Preferred Content Difficulty</label>
              {editing ? (
                <select value={preferredDifficulty} onChange={(e) => setPreferredDifficulty(e.target.value)}>
                  <option value="">Select...</option>
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              ) : (
                <p>{preferredDifficulty || 'Not set'}</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
