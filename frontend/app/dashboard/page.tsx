"use client";
import { Users, Receipt, Sparkles, ArrowRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useEffect, useState } from "react";
import CreateGroupDialog from "@/components/groups/create-group-dialog";
import { getGroups } from "@/services/group";
import { Group } from "@/types/group";
import { useAuthStore } from "@/store/auth";
import JoinGroupDialog from "@/components/groups/join-group-dialog";
import GroupCard from "@/components/groups/group-card";
import Navbar from "@/components/layout/navbar";
import AuthGuard from "@/components/auth/auth-guard";
import EmptyState from "@/components/common/empty-state";
import { Button } from "@/components/ui/button";
import { getOverallBalance } from "@/services/dashboard";
export default function Dashboard() {
  const user = useAuthStore((state) => state.user);
  const [overallBalance, setOverallBalance] = useState(0);
  const [groups, setGroups] = useState<Group[]>([]);
  const hour = new Date().getHours();

  const greeting =
    hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";
  useEffect(() => {
    loadGroups();
  }, []);
  async function loadGroups() {
    const data = await getGroups();

    setGroups(data);

    const balance = await getOverallBalance();

    setOverallBalance(balance);
  }

  return (
    <AuthGuard>
      <Navbar />
      <main className="mx-auto flex min-h-screen max-w-6xl flex-col gap-6 px-4 py-8 sm:px-6 lg:px-8">
        <section className="rounded-none border border-black/10 bg-white p-6 shadow-[0_1px_0_0_rgba(0,0,0,0.04)] sm:p-8">
          <div className="flex flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
            <div className="space-y-5">
              <div className="inline-flex items-center gap-2 rounded-none border border-black/10 px-3 py-1 text-[11px] uppercase tracking-[0.25em] text-black/55">
                Dashboard
              </div>

              <div className="space-y-3">
                <h1 className="max-w-3xl text-4xl font-semibold tracking-tight text-black sm:text-5xl">
                  {greeting},{" "}
                  <span className="text-black/70">{user?.name}</span>.
                </h1>
                <p className="max-w-2xl text-sm leading-6 text-black/60 sm:text-base">
                  Keep your shared costs, invite codes, and balances in one
                  calm, monochrome workspace.
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-3 text-sm text-black/55">
                <span className="inline-flex items-center gap-2 rounded-none border border-black/10 px-3 py-2">
                  <Sparkles className="h-4 w-4" />
                  Split expenses cleanly
                </span>
                <span className="rounded-none border border-black/10 px-3 py-2">
                  {groups.length} group{groups.length === 1 ? "" : "s"} tracked
                </span>
              </div>
            </div>

            <div className="grid gap-3 sm:grid-cols-2 lg:w-[22rem]">
              <Card>
                <CardContent className="flex items-center justify-between p-4">
                  <div>
                    <p className="text-[11px] uppercase tracking-[0.2em] text-black/45">
                      Total groups
                    </p>
                    <p className="mt-2 text-3xl font-semibold text-black">
                      {groups.length}
                    </p>
                  </div>
                  <Users className="h-5 w-5 text-black" />
                </CardContent>
              </Card>

              <Card>
                <CardContent className="flex items-center justify-between p-4">
                  <div>
                    <p className="text-[11px] uppercase tracking-[0.2em] text-black/45">
                      {overallBalance >= 0 ? "You are owed" : "You owe"}
                    </p>

                    <p
                      className={`mt-2 text-3xl font-semibold ${
                        overallBalance >= 0 ? "text-green-600" : "text-red-600"
                      }`}
                    >
                      ₹{Math.abs(overallBalance).toFixed(2)}
                    </p>

                    <Receipt
                      className={`h-5 w-5 ${
                        overallBalance >= 0 ? "text-green-600" : "text-red-600"
                      }`}
                    />
                  </div>
                  <Receipt className="h-5 w-5 text-black" />
                </CardContent>
              </Card>
            </div>
          </div>

          <div className="mt-6 flex flex-col gap-3 border-t border-black/10 pt-6 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.25em] text-black/45">
                Quick actions
              </p>
              <p className="mt-1 text-sm text-black/55">
                Start a new group or join an existing one.
              </p>
            </div>

            <div className="flex flex-wrap gap-3">
              <CreateGroupDialog onSuccess={loadGroups} />
              <JoinGroupDialog onSuccess={loadGroups} />
            </div>
          </div>
        </section>

        <section className="grid gap-4 lg:grid-cols-[1fr_18rem] lg:items-start">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between gap-4">
              <div>
                <CardTitle>Your Groups</CardTitle>
                <p className="mt-1 text-xs text-black/50">
                  Open a group to review expenses, balances, and settlements.
                </p>
              </div>

              <span className="rounded-none border border-black/10 px-3 py-1 text-[11px] uppercase tracking-[0.2em] text-black/50">
                {groups.length} total
              </span>
            </CardHeader>

            <CardContent>
              {groups.length === 0 ? (
                <EmptyState
                  icon={<ArrowRight />}
                  title="No groups yet"
                  description="Create a group to start splitting shared expenses."
                />
              ) : (
                <div className="space-y-4">
                  {groups.map((group) => (
                    <GroupCard key={group.id} group={group} />
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>At a glance</CardTitle>
              <p className="mt-1 text-xs text-black/50">
                A simple snapshot of where things stand.
              </p>
            </CardHeader>

            <CardContent className="space-y-3">
              <div className="flex items-center justify-between border border-black/10 p-3">
                <span className="text-sm text-black/60">Groups</span>
                <span className="font-semibold text-black">
                  {groups.length}
                </span>
              </div>

              <div className="flex items-center justify-between border border-black/10 p-3">
                <span className="text-sm text-black/60">Ready to split</span>
                <span className="font-semibold text-black">Yes</span>
              </div>

              <div className="flex items-center justify-between border border-black/10 p-3">
                <span className="text-sm text-black/60">Theme</span>
                <span className="font-semibold text-black">Mono</span>
              </div>
            </CardContent>
          </Card>
        </section>
      </main>
    </AuthGuard>
  );
}
