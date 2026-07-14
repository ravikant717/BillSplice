"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { logout as logoutUser } from "@/services/auth";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "@/store/auth";
import { toast } from "sonner";

export default function Navbar() {
  const router = useRouter();

  async function handleLogout() {
    await logoutUser();
    useAuthStore.getState().logout();
    router.replace("/login");
    toast.success("Logged out successfully");
  }

  return (
    <header className="border-b bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/dashboard" className="text-2xl font-bold">
          💸 BillSplice
        </Link>

        <div className="flex items-center gap-3">
          <Link href="/dashboard">
            <Button variant="ghost">Dashboard</Button>
          </Link>

          <Button variant="destructive" onClick={handleLogout}>
            Logout
          </Button>
        </div>
      </div>
    </header>
  );
}
