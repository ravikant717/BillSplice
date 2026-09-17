import { ReceiptText } from "lucide-react";

export default function Loading() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-5">
      <div className="relative">
        {/* Outer spinning ring */}
        <div className="h-14 w-14 animate-spin rounded-full border-2 border-black/10 border-t-black" />

        {/* BillSplice icon */}
        <div className="absolute inset-0 flex items-center justify-center">
          <ReceiptText className="h-5 w-5 text-black" />
        </div>
      </div>

      <div className="flex flex-col items-center gap-1">
        <p className="text-sm font-medium tracking-tight text-black">
          Loading BillSplice
        </p>

        <p className="text-xs text-black/45">Splitting things up...</p>
      </div>
    </div>
  );
}
