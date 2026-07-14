"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import SessionRedirect from "@/components/auth/session-redirect";
import { register, getCurrentUser } from "@/services/auth";
import { useAuthStore } from "@/store/auth";
import { toast } from "sonner";

export default function SignUpPage() {
  const router = useRouter();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  async function handleRegister() {
    try {
      await register({ name, email, password });

      const user = await getCurrentUser();

      useAuthStore.getState().setUser(user);

      toast.success("Welcome aboard!");

      router.push("/dashboard");
    } catch (err) {
      console.error(err);
      toast.error("Could not create account");
    }
  }

  return (
    <SessionRedirect redirectIfAuthedTo="/dashboard">
      <div className="flex min-h-screen items-center justify-center">
        <div className="w-80 space-y-4">
          <input
            className="w-full border p-2"
            placeholder="Name"
            onChange={(e) => setName(e.target.value)}
          />

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
            onClick={handleRegister}
            className="w-full rounded bg-black p-2 text-white"
          >
            Register
          </button>
        </div>
      </div>
    </SessionRedirect>
  );
}
