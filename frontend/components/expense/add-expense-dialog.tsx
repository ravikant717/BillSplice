"use client";

import { useState } from "react";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { createExpense } from "@/services/expense";
import { toast } from "sonner";

interface Props {
  groupId: string;
  onSuccess: () => void;
}

export default function AddExpenseDialog({ groupId, onSuccess }: Props) {
  const [open, setOpen] = useState(false);
  const [isCreating, setIsCreating] = useState(false);

  const [title, setTitle] = useState("");

  const [amount, setAmount] = useState("");

  async function handleCreate() {
    if (isCreating) return;

    const value = Number(amount);

    if (!title.trim() || isNaN(value) || value <= 0) {
      toast.error("Enter a valid amount.");
      return;
    }

    setIsCreating(true);

    try {
      await createExpense(groupId, title, value);
      toast.success("Expense added successfully!");
      setTitle("");
      setAmount("");

      setOpen(false);

      onSuccess();
    } catch (err) {
      console.error(err);
      toast.error("Failed to create expense");
    } finally {
      setIsCreating(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger render={<Button />}>
        <Button>Add Expense</Button>
      </DialogTrigger>

      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Add Expense</DialogTitle>
          <p className="text-sm text-black/60">
            Add a shared cost and keep the group balance up to date.
          </p>
        </DialogHeader>

        <div className="space-y-3">
          <Input
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <Input
            type="number"
            placeholder="Amount"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />
        </div>

        <DialogFooter>
          <Button
            onClick={handleCreate}
            disabled={isCreating}
            className="w-full sm:w-auto"
          >
            {isCreating ? "Creating..." : "Add Expense"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
