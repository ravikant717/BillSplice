"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import SessionRedirect from "@/components/auth/session-redirect";
import { login, getCurrentUser } from "@/services/auth";
import { useAuthStore } from "@/store/auth";
import { toast } from "sonner";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  async function handleLogin() {
    try {
      await login(email, password);

      const user = await getCurrentUser();

      useAuthStore.getState().setUser(user);

      toast.success("Welcome back!");

      router.push("/dashboard");
    } catch (err) {
      console.error(err);
      toast.error("Invalid email or password");
    }
  }

  return (
    <SessionRedirect redirectIfAuthedTo="/dashboard">
      <div className="flex min-h-screen items-center justify-center">
        <div className="w-80 space-y-4">
          <input
            className="w-full border p-2"
            placeholder="Email"
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            type="password"
            className="w-full border p-2"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            onClick={handleLogin}
            className="w-full rounded bg-black p-2 text-white"
          >
            Login
          </button>
        </div>
      </div>
    </SessionRedirect>
  );
}
