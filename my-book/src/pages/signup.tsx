import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../contexts/AuthContext';
import { useHistory } from '@docusaurus/router';
import styles from './auth.module.css';

export default function SignupPage() {
  const { signUp } = useAuth();
  const history = useHistory();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Step 1: Basic info
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');

  // Step 2: Software background
  const [programmingExperience, setProgrammingExperience] = useState('');
  const [programmingLanguages, setProgrammingLanguages] = useState<string[]>([]);
  const [aiMlExperience, setAiMlExperience] = useState('');
  const [rosExperience, setRosExperience] = useState('');

  // Step 3: Hardware background
  const [roboticsExperience, setRoboticsExperience] = useState('');
  const [hardwareProjects, setHardwareProjects] = useState<string[]>([]);
  const [hasRoboticsHardware, setHasRoboticsHardware] = useState(false);
  const [hardwareDescription, setHardwareDescription] = useState('');

  // Step 4: Learning preferences
  const [learningGoals, setLearningGoals] = useState<string[]>([]);
  const [preferredDifficulty, setPreferredDifficulty] = useState('');

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (step < 4) {
      setStep(step + 1);
      return;
    }

    setLoading(true);
    setError('');

    try {
      await signUp(email, password, name, {
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
        onboardingCompleted: true,
      });
      history.push('/');
    } catch (err) {
      setError(err.message || 'Sign up failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout title="Sign Up" description="Create your account and personalize your learning">
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <h1>Create Your Account</h1>
          <div className={styles.progressBar}>
            <div className={styles.progressStep + (step >= 1 ? ' ' + styles.active : '')}>1</div>
            <div className={styles.progressStep + (step >= 2 ? ' ' + styles.active : '')}>2</div>
            <div className={styles.progressStep + (step >= 3 ? ' ' + styles.active : '')}>3</div>
            <div className={styles.progressStep + (step >= 4 ? ' ' + styles.active : '')}>4</div>
          </div>

          <form onSubmit={handleSubmit}>
            {/* Step 1: Basic Information */}
            {step === 1 && (
              <div className={styles.formStep}>
                <h2>Basic Information</h2>
                <div className={styles.formGroup}>
                  <label>Name</label>
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                </div>
                <div className={styles.formGroup}>
                  <label>Email</label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <div className={styles.formGroup}>
                  <label>Password</label>
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    minLength={8}
                  />
                </div>
              </div>
            )}

            {/* Step 2: Software Background */}
            {step === 2 && (
              <div className={styles.formStep}>
                <h2>Software Background</h2>
                <div className={styles.formGroup}>
                  <label>Programming Experience</label>
                  <select
                    value={programmingExperience}
                    onChange={(e) => setProgrammingExperience(e.target.value)}
                    required
                  >
                    <option value="">Select...</option>
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                    <option value="expert">Expert</option>
                  </select>
                </div>

                <div className={styles.formGroup}>
                  <label>Programming Languages (select all that apply)</label>
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
                </div>

                <div className={styles.formGroup}>
                  <label>AI/ML Experience</label>
                  <select
                    value={aiMlExperience}
                    onChange={(e) => setAiMlExperience(e.target.value)}
                    required
                  >
                    <option value="">Select...</option>
                    <option value="none">None</option>
                    <option value="basic">Basic</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </select>
                </div>

                <div className={styles.formGroup}>
                  <label>ROS Experience</label>
                  <select
                    value={rosExperience}
                    onChange={(e) => setRosExperience(e.target.value)}
                    required
                  >
                    <option value="">Select...</option>
                    <option value="none">None</option>
                    <option value="basic">Basic</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </select>
                </div>
              </div>
            )}

            {/* Step 3: Hardware Background */}
            {step === 3 && (
              <div className={styles.formStep}>
                <h2>Hardware Background</h2>
                <div className={styles.formGroup}>
                  <label>Robotics Experience</label>
                  <select
                    value={roboticsExperience}
                    onChange={(e) => setRoboticsExperience(e.target.value)}
                    required
                  >
                    <option value="">Select...</option>
                    <option value="none">None</option>
                    <option value="hobbyist">Hobbyist</option>
                    <option value="student">Student</option>
                    <option value="professional">Professional</option>
                  </select>
                </div>

                <div className={styles.formGroup}>
                  <label>Hardware Projects (select all that apply)</label>
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
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.checkboxLabel}>
                    <input
                      type="checkbox"
                      checked={hasRoboticsHardware}
                      onChange={(e) => setHasRoboticsHardware(e.target.checked)}
                    />
                    I have access to robotics hardware
                  </label>
                </div>

                {hasRoboticsHardware && (
                  <div className={styles.formGroup}>
                    <label>Describe your hardware</label>
                    <textarea
                      value={hardwareDescription}
                      onChange={(e) => setHardwareDescription(e.target.value)}
                      rows={3}
                      placeholder="E.g., Jetson Orin Nano, RealSense camera, custom rover..."
                    />
                  </div>
                )}
              </div>
            )}

            {/* Step 4: Learning Preferences */}
            {step === 4 && (
              <div className={styles.formStep}>
                <h2>Learning Goals</h2>
                <div className={styles.formGroup}>
                  <label>What do you want to learn? (select all that apply)</label>
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
                </div>

                <div className={styles.formGroup}>
                  <label>Preferred Content Difficulty</label>
                  <select
                    value={preferredDifficulty}
                    onChange={(e) => setPreferredDifficulty(e.target.value)}
                    required
                  >
                    <option value="">Select...</option>
                    <option value="beginner">Beginner - Step-by-step guidance</option>
                    <option value="intermediate">Intermediate - Balanced approach</option>
                    <option value="advanced">Advanced - Technical deep-dives</option>
                  </select>
                </div>
              </div>
            )}

            {error && <div className={styles.error}>{error}</div>}

            <div className={styles.buttonGroup}>
              {step > 1 && (
                <button
                  type="button"
                  onClick={() => setStep(step - 1)}
                  className={styles.secondaryButton}
                  disabled={loading}
                >
                  Back
                </button>
              )}
              <button type="submit" className={styles.primaryButton} disabled={loading}>
                {loading ? 'Processing...' : step < 4 ? 'Next' : 'Create Account'}
              </button>
            </div>
          </form>

          <p className={styles.authLink}>
            Already have an account? <a href="/signin">Sign in</a>
          </p>
        </div>
      </div>
    </Layout>
  );
}
