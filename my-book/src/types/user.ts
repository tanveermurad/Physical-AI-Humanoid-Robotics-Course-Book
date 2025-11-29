export interface UserBackground {
  // Software background
  programmingExperience?: 'beginner' | 'intermediate' | 'advanced' | 'expert';
  programmingLanguages?: string[];
  aiMlExperience?: 'none' | 'basic' | 'intermediate' | 'advanced';
  rosExperience?: 'none' | 'basic' | 'intermediate' | 'advanced';

  // Hardware background
  roboticsExperience?: 'none' | 'hobbyist' | 'student' | 'professional';
  hardwareProjects?: string[];
  hasRoboticsHardware?: boolean;
  hardwareDescription?: string;

  // Learning preferences
  learningGoals?: string[];
  preferredDifficulty?: 'beginner' | 'intermediate' | 'advanced';
  onboardingCompleted?: boolean;
}

export interface UserProfile extends UserBackground {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
  updatedAt: string;
}
