"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { getCurrentUser } from "@/services/auth";
import { useAuthStore } from "@/store/auth";
import Loading from "@/components/common/loading";

export default function AuthGuard({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();

  const user = useAuthStore((state) => state.user);
  const setUser = useAuthStore((state) => state.setUser);

  // initialize loading based on whether we already have a user to avoid
  // calling setState synchronously inside the effect
  const [loading, setLoading] = useState(() => (user ? false : true));

  useEffect(() => {
    async function checkAuth() {
      try {
        const me = await getCurrentUser();

        setUser(me);
      } catch {
        router.replace("/login");
      } finally {
        setLoading(false);
      }
    }

    if (!user) {
      checkAuth();
    }
  }, [user, setUser, router]);

  if (loading) {
    return <Loading />;
  }

  return <>{children}</>;
}