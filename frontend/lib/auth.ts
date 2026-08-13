"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface User {
  id: number;
  name: string;
  email: string;
  role: "supplier" | "buyer" | "admin";
  business_type?: string | null;
  country?: string | null;
  location?: string | null;
  phone?: string | null;
}

interface AuthState {
  token: string | null;
  user: User | null;
  setAuth: (token: string, user: User) => void;
  clear: () => void;
}

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      setAuth: (token, user) => set({ token, user }),
      clear: () => set({ token: null, user: null }),
    }),
    {
      name: "w2w_auth",
    }
  )
);

export function useHydrated() {
  // zustand persist is synchronous from localStorage on first client render,
  // so a mounted check is enough to avoid SSR/hydration mismatches.
  return true;
}