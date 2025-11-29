/**
 * Extended database schema for user profiles and background information
 */

export const userProfileSchema = {
  user: {
    fields: {
      // Better Auth will handle these automatically:
      // id, email, name, emailVerified, image, createdAt, updatedAt
    }
  },

  // Custom table for user background and preferences
  userProfile: {
    tableName: "user_profile",
    fields: {
      id: {
        type: "string",
        primaryKey: true,
      },
      userId: {
        type: "string",
        references: {
          model: "user",
          field: "id",
        },
        unique: true,
      },
      // Software background
      programmingExperience: {
        type: "string", // beginner, intermediate, advanced, expert
        required: false,
      },
      programmingLanguages: {
        type: "string", // JSON array stored as string
        required: false,
      },
      aiMlExperience: {
        type: "string", // none, basic, intermediate, advanced
        required: false,
      },
      rosExperience: {
        type: "string", // none, basic, intermediate, advanced
        required: false,
      },

      // Hardware background
      roboticsExperience: {
        type: "string", // none, hobbyist, student, professional
        required: false,
      },
      hardwareProjects: {
        type: "string", // JSON array stored as string
        required: false,
      },
      hasRoboticsHardware: {
        type: "boolean",
        required: false,
      },
      hardwareDescription: {
        type: "string",
        required: false,
      },

      // Learning preferences
      learningGoals: {
        type: "string", // JSON array stored as string
        required: false,
      },
      preferredDifficulty: {
        type: "string", // beginner, intermediate, advanced
        required: false,
      },

      // Profile completion
      onboardingCompleted: {
        type: "boolean",
        default: false,
      },

      createdAt: {
        type: "date",
      },
      updatedAt: {
        type: "date",
      },
    },
  },
};
