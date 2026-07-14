"use client";

import { useState } from "react";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { joinGroup } from "@/services/group";
import { toast } from "sonner";

interface Props {
  onSuccess: () => void;
}

export default function JoinGroupDialog({ onSuccess }: Props) {
  const [open, setOpen] = useState(false);

  const [inviteCode, setInviteCode] = useState("");

  async function handleJoin() {
    if (!inviteCode.trim()) {
      toast.error("Enter an invite code.");
      return;
    }

    try {
      await joinGroup(inviteCode.toUpperCase());

      toast.success("Joined group successfully!");

      setInviteCode("");
      setOpen(false);

      onSuccess();
    } catch (err) {
      console.error(err);

      toast.error("Invalid invite code");
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline">Join Group</Button>
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>Join Group</DialogTitle>
        </DialogHeader>

        <Input
          placeholder="Invite Code"
          value={inviteCode}
          onChange={(e) => setInviteCode(e.target.value.toUpperCase())}
        />

        <Button onClick={handleJoin}>Join</Button>
      </DialogContent>
    </Dialog>
  );
}
