import { Card, CardContent } from "@/components/ui/card";

export default function GroupCardSkeleton() {
  return (
    <Card className="border border-black/10">
      <CardContent className="p-5 sm:p-6">
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0 flex-1">
            {/* Group name */}
            <div className="h-6 w-40 animate-pulse bg-black/10" />

            {/* Invite code label */}
            <div className="mt-4 h-3 w-20 animate-pulse bg-black/10" />

            {/* Invite code */}
            <div className="mt-2 flex items-center gap-2">
              <div className="h-8 w-28 animate-pulse bg-black/10" />

              <div className="h-8 w-8 animate-pulse border border-black/10 bg-black/5" />
            </div>
          </div>

          {/* Arrow */}
          <div className="h-5 w-5 animate-pulse bg-black/10" />
        </div>
      </CardContent>
    </Card>
  );
}
