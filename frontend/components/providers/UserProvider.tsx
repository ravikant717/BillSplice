"use client";

import { useEffect, useState } from "react";
import Loading from "@/components/common/loading";
import { getCurrentUser } from "@/services/auth";
import { useAuthStore } from "@/store/auth";

export default function UserProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const setUser = useAuthStore((state) => state.setUser);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadUser() {
      try {
        const user = await getCurrentUser();
        setUser(user);
      } finally {
        setLoading(false);
      }
    }

    loadUser();
  }, [setUser]);

  if (loading) {
    return <Loading />;
  }

  return <>{children}</>;
}
