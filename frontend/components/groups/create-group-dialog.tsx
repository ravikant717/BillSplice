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

import { createGroup } from "@/services/group";
import { toast } from "sonner";

interface Props {
  onSuccess: () => void;
}

export default function CreateGroupDialog({ onSuccess }: Props) {
  const [name, setName] = useState("");
  const [isCreating, setIsCreating] = useState(false);
  const [open, setOpen] = useState(false);

  async function handleCreate() {
    if (!name.trim() || isCreating) return;

    setIsCreating(true);

    try {
      await createGroup(name);

      toast.success("Group created successfully!");

      setOpen(false);
      setName("");

      onSuccess();
    } catch (err) {
      console.error(err);

      toast.error("Failed to create group");
    } finally {
      setIsCreating(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger render={<Button />}>
        <Button>Create Group</Button>
      </DialogTrigger>

      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Create Group</DialogTitle>
          <p className="text-sm text-black/60">
            Create a new shared space for expenses and balances.
          </p>
        </DialogHeader>

        <div className="space-y-3">
          <Input
            placeholder="Group Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>

        <DialogFooter>
          <Button
            onClick={handleCreate}
            disabled={isCreating}
            className="w-full sm:w-auto"
          >
            {isCreating ? "Creating..." : "Create Group"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
