import type { Truth } from "@/lib/types";
import { Progress } from "@/components/ui/progress";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

export function TruthMeter({ truth, band }: { truth: Truth; band?: string }) {
  return (
    <div className="grid gap-2">
      <Meter label="Frequency" value={truth.f} hint="How often this holds, by Omega's NAL" />
      <Meter label="Confidence" value={truth.c} hint="How sure Omega's NAL is" />
      {band && (
        <p className="text-xs text-muted-foreground">
          Band: {band === "act" ? "act (f at least 0.6 and c at least 0.5)" : band === "hypothesise" ? "confirm first" : "none"}
        </p>
      )}
    </div>
  );
}

function Meter({ label, value, hint }: { label: string; value: number; hint: string }) {
  return (
    <Tooltip>
      <TooltipTrigger render={<div className="grid gap-1" />}>
        <div className="flex items-center justify-between text-xs">
          <span className="text-muted-foreground">{label}</span>
          <span className="tabular font-medium">{value.toFixed(2)}</span>
        </div>
        <Progress value={Math.round(value * 100)} className="h-1.5" />
      </TooltipTrigger>
      <TooltipContent>{hint}</TooltipContent>
    </Tooltip>
  );
}
