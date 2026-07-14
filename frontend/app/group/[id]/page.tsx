"use client";
import EmptyState from "@/components/common/empty-state";
import { HandCoins, Receipt, Users, Wallet, ReceiptText } from "lucide-react";
import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import { Expense } from "@/types/expense";
import { getExpenses } from "@/services/expense";
import { getGroupDetails } from "@/services/group";
import { GroupDetail } from "@/types/group-detail";
import { Balance } from "@/types/balance";
import { getBalances } from "@/services/balance";
import { Settlement } from "@/types/settlement";
import { getSettlements } from "@/services/settlement";
import { Trash2 } from "lucide-react";
import { deleteExpense } from "@/services/expense";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import AddExpenseDialog from "@/components/expense/add-expense-dialog";
import Navbar from "@/components/layout/navbar";
import AuthGuard from "@/components/auth/auth-guard";
import Loading from "@/components/common/loading";
import { settle } from "@/services/settlement";
import { useAuthStore } from "@/store/auth";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
export default function GroupPage() {
  const params = useParams();
  const user = useAuthStore((state) => state.user);
  const [group, setGroup] = useState<GroupDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [balances, setBalances] = useState<Balance[]>([]);
  const [settlements, setSettlements] = useState<Settlement[]>([]);
  const myBalance =
    balances.find((balance) => balance.user === user?.name)?.balance ?? 0;
  const loadGroup = useCallback(async () => {
    try {
      const data = await getGroupDetails(params.id as string);
      setGroup(data);

      const expenseData = await getExpenses(params.id as string);
      setExpenses(expenseData);

      const balanceData = await getBalances(params.id as string);
      setBalances(balanceData);

      const settlementData = await getSettlements(params.id as string);
      setSettlements(settlementData);
    } finally {
      setLoading(false);
    }
  }, [params.id]);

  useEffect(() => {
    loadGroup();
  }, [loadGroup]);

  if (loading) return <Loading />;

  const totalExpense = expenses.reduce(
    (sum, expense) => sum + expense.amount,
    0,
  );

  async function handleDeleteExpense(expenseId: string) {
    const ok = confirm("Delete this expense?");

    if (!ok) return;

    try {
      await deleteExpense(expenseId);
      toast.success("Expense deleted");
      loadGroup();
    } catch (err) {
      console.error(err);

      toast.error("Failed to delete expense");
    }
  }
  async function handleSettle(toUserId: string, amount: number) {
    if (!group) return;
    try {
      await settle(group.id, toUserId, amount);

      toast.success("Settlement recorded");

      loadGroup();
    } catch (err) {
      console.error(err);

      toast.error("Failed to settle");
    }
  }
  return (
    <AuthGuard>
      <Navbar />
      <main className="mx-auto flex min-h-screen max-w-6xl flex-col gap-6 px-4 py-8 sm:px-6 lg:px-8">
        <section className="rounded-none border border-black/10 bg-white p-6 shadow-[0_1px_0_0_rgba(0,0,0,0.04)] sm:p-8">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="space-y-4">
              <div className="inline-flex items-center gap-2 rounded-none border border-black/10 px-3 py-1 text-[11px] uppercase tracking-[0.25em] text-black/60">
                Group overview
              </div>

              <div className="space-y-2">
                <h1 className="text-4xl font-semibold tracking-tight text-black sm:text-5xl">
                  {group?.name}
                </h1>
                <p className="max-w-2xl text-sm leading-6 text-black/60">
                  Keep track of shared spending, balances, and settlements in
                  one place.
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-3">
                <div className="rounded-none border border-black/10 bg-black px-3 py-2 text-xs font-medium tracking-wide text-white">
                  Invite code: {group?.invite_code}
                </div>
                <div className="rounded-none border border-black/10 px-3 py-2 text-xs text-black/60">
                  Members: {group?.members.length}
                </div>
              </div>
            </div>

            {group ? <AddExpenseDialog groupId={group.id} onSuccess={loadGroup} /> : null}
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardContent className="flex items-center justify-between p-4">
              <div>
                <p className="text-[11px] uppercase tracking-[0.2em] text-black/50">
                  Members
                </p>
                <p className="mt-2 text-2xl font-semibold text-black">
                  {group?.members.length}
                </p>
              </div>
              <Users className="h-5 w-5 text-black" />
            </CardContent>
          </Card>

          <Card>
            <CardContent className="flex items-center justify-between p-4">
              <div>
                <p className="text-[11px] uppercase tracking-[0.2em] text-black/50">
                  Expenses
                </p>
                <p className="mt-2 text-2xl font-semibold text-black">
                  {expenses.length}
                </p>
              </div>
              <ReceiptText className="h-5 w-5 text-black" />
            </CardContent>
          </Card>

          <Card>
            <CardContent className="flex items-center justify-between p-4">
              <div>
                <p className="text-[11px] uppercase tracking-[0.2em] text-black/50">
                  Total spent
                </p>
                <p className="mt-2 text-2xl font-semibold text-black">
                  ₹{totalExpense}
                </p>
              </div>
              <Wallet className="h-5 w-5 text-black" />
            </CardContent>
          </Card>

          <Card>
            <CardContent className="flex items-center justify-between p-4">
              <div>
                <p className="text-[11px] uppercase tracking-[0.2em] text-black/50">
                  My Net balance
                </p>
                <p className="mt-2 text-2xl font-semibold text-black">
                  {myBalance >= 0
                    ? `+ ₹${myBalance}`
                    : `- ₹${Math.abs(myBalance)}`}
                </p>
              </div>
              <HandCoins className="h-5 w-5 text-black" />
            </CardContent>
          </Card>
        </section>

        <section className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between gap-4">
              <div>
                <CardTitle>Expenses</CardTitle>
                <p className="mt-1 text-xs text-black/50">
                  New expenses are listed at the top of the activity feed.
                </p>
              </div>
              <span className="rounded-none border border-black/10 px-3 py-1 text-[11px] uppercase tracking-[0.2em] text-black/50">
                {expenses.length} items
              </span>
            </CardHeader>

            <CardContent>
              {expenses.length === 0 ? (
                <EmptyState
                  icon={<Receipt />}
                  title="No expenses yet"
                  description="Add your first expense to get started."
                />
              ) : (
                <div className="space-y-3">
                  {expenses.map((expense) => (
                    <div
                      key={expense.id}
                      className="flex items-center justify-between gap-4 border border-black/10 bg-white p-4"
                    >
                      <div className="min-w-0">
                        <h3 className="truncate font-medium text-black">
                          {expense.title}
                        </h3>
                        <p className="mt-1 text-xs text-black/45">
                          Shared expense
                        </p>
                      </div>

                      <div className="flex items-center gap-2">
                        <span className="whitespace-nowrap font-semibold text-black">
                          ₹{expense.amount}
                        </span>

                        {expense.paid_by === user?.id && (
                          <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => handleDeleteExpense(expense.id)}
                          >
                            <Trash2 className="h-4 w-4 text-black/70" />
                          </Button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>

          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Members</CardTitle>
                <p className="mt-1 text-xs text-black/50">
                  Everyone currently in the group.
                </p>
              </CardHeader>

              <CardContent>
                <ul className="space-y-3">
                  {group?.members.map((member) => (
                    <li
                      key={member}
                      className="flex items-center justify-between border border-black/10 p-3"
                    >
                      <span className="font-medium text-black">{member}</span>
                      <span className="text-[11px] uppercase tracking-[0.2em] text-black/35">
                        member
                      </span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Balances</CardTitle>
                <p className="mt-1 text-xs text-black/50">
                  Positive amounts mean the user should receive money.
                </p>
              </CardHeader>

              <CardContent>
                {balances.length === 0 ? (
                  <EmptyState
                    icon={<Wallet />}
                    title="No balances"
                    description="Balances will appear after expenses are added."
                  />
                ) : (
                  <div className="space-y-3">
                    {balances.map((balance) => (
                      <div
                        key={balance.user}
                        className="flex items-center justify-between border border-black/10 p-4"
                      >
                        <span className="font-medium text-black">
                          {balance.user}
                        </span>

                        <span className="font-semibold text-black">
                          {balance.balance >= 0
                            ? `+ ₹${balance.balance}`
                            : `- ₹${Math.abs(balance.balance)}`}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Suggested Settlements</CardTitle>
                <p className="mt-1 text-xs text-black/50">
                  Suggested transfers to settle the group.
                </p>
              </CardHeader>

              <CardContent>
                {settlements.length === 0 ? (
                  <EmptyState
                    icon={<HandCoins />}
                    title="No settlements"
                    description="Everyone is settled up for now."
                  />
                ) : (
                  <div className="space-y-3">
                    {settlements.map((settlement, index) => (
                      <div
                        key={index}
                        className="flex items-center justify-between gap-4 border border-black/10 p-4"
                      >
                        <div className="flex min-w-0 items-center gap-2 text-sm">
                          <span className="truncate font-medium text-black">
                            {settlement.from_user}
                          </span>

                          <span className="text-black/40">→</span>

                          <span className="truncate font-medium text-black">
                            {settlement.to_user}
                          </span>
                        </div>

                        <div className="flex items-center gap-3">
                          <span className="font-semibold text-black">
                            ₹{settlement.amount}
                          </span>

                          {settlement.from_user_id === user?.id && (
                            <Button
                              size="sm"
                              onClick={() =>
                                handleSettle(
                                  settlement.to_user_id,
                                  settlement.amount,
                                )
                              }
                            >
                              Settle
                            </Button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </section>
      </main>
    </AuthGuard>
  );
}
