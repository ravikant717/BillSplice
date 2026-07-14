"use client";

import { ReactNode, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import Loading from "@/components/common/loading";
import { getCurrentUser } from "@/services/auth";
import { useAuthStore } from "@/store/auth";

interface Props {
  children?: ReactNode;
  redirectIfAuthedTo: string;
  redirectIfUnauthedTo?: string;
}

export default function SessionRedirect({
  children,
  redirectIfAuthedTo,
  redirectIfUnauthedTo,
}: Props) {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);
  const setUser = useAuthStore((state) => state.setUser);

  const [checking, setChecking] = useState(true);

  useEffect(() => {
    async function resolveSession() {
      if (user) {
        router.replace(redirectIfAuthedTo);
        return;
      }

      try {
        const me = await getCurrentUser();

        setUser(me);
        router.replace(redirectIfAuthedTo);
      } catch {
        if (redirectIfUnauthedTo) {
          router.replace(redirectIfUnauthedTo);
        }
      } finally {
        setChecking(false);
      }
    }

    resolveSession();
  }, [redirectIfAuthedTo, redirectIfUnauthedTo, router, setUser, user]);

  if (checking) {
    return <Loading />;
  }

  return <>{children}</>;
}
