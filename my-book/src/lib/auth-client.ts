import { createAuthClient } from "better-auth/react";

const getBaseURL = () => {
  if (typeof window === 'undefined') {
    return "http://localhost:3001";
  }
  return process.env.BETTER_AUTH_URL || "http://localhost:3001";
};

export const authClient = createAuthClient({
  baseURL: getBaseURL(),
});

export const {
  signIn,
  signUp,
  signOut,
  useSession
} = authClient;
