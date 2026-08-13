"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";

export function AuthGate() {
  const router = useRouter();
  const { token, user } = useAuth();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  useEffect(() => {
    if (mounted && token && user) {
      router.replace(`/${user.role}/dashboard`);
    }
  }, [mounted, token, user, router]);
  return null;
}
