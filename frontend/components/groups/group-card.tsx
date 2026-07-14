"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ChevronRight, Copy } from "lucide-react";
import { Group } from "@/types/group";
import { useRouter } from "next/navigation";
import { toast } from "sonner";

interface Props {
  group: Group;
}

export default function GroupCard({ group }: Props) {
  const router = useRouter();

  async function copyCode(e: React.MouseEvent<HTMLButtonElement>) {
    e.stopPropagation();

    await navigator.clipboard.writeText(group.invite_code);

    toast.success("Invite code copied!");
  }

  return (
    <Card
      className="cursor-pointer border border-black/10 transition-all duration-200 hover:-translate-y-0.5 hover:border-black/25 hover:shadow-[0_16px_40px_rgba(0,0,0,0.08)]"
      onClick={() => router.push(`/group/${group.id}`)}
    >
      <CardContent className="p-5 sm:p-6">
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0">
            <h2 className="truncate text-lg font-semibold text-black sm:text-xl">
              {group.name}
            </h2>

            <p className="mt-4 text-xs uppercase tracking-[0.2em] text-black/45">
              Invite code
            </p>

            <div className="mt-2 flex items-center gap-2">
              <code className="rounded-none border border-black/10 bg-black px-3 py-1.5 text-xs font-mono tracking-[0.2em] text-white">
                {group.invite_code}
              </code>

              <Button size="icon-sm" variant="outline" onClick={copyCode}>
                <Copy className="h-4 w-4" />
              </Button>
            </div>
          </div>

          <ChevronRight className="h-5 w-5 shrink-0 text-black/35" />
        </div>
      </CardContent>
    </Card>
  );
}
