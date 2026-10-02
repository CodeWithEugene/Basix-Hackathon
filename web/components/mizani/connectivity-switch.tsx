"use client";

import { Wifi, WifiOff } from "lucide-react";
import { toast } from "sonner";

import { api, useAgent } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

type OutboxState = { online: boolean; pending: unknown[] };

export function ConnectivitySwitch({
  online,
  onToggle,
}: {
  online?: boolean;
  onToggle?: (online: boolean) => void;
}) {
  const { data, reload } = useAgent<OutboxState>("community", "/outbox", {
    pollMs: 4000,
  });
  const value = online ?? data?.online ?? false;

  async function toggle(next: boolean) {
    try {
      const res = await api<{ synced: string[]; pending: number }>(
        "community",
        "/connectivity",
        { method: "POST", body: JSON.stringify({ online: next }) },
      );
      onToggle?.(next);
      reload();
      if (next) {
        if (res.synced.length > 0) {
          toast.success("Referral synced to Mtwapa Health Centre.");
        } else {
          toast.info("Back online.");
        }
      } else {
        toast.info("Offline. Decisions run on this device's rule pack.");
      }
    } catch {
      toast.error("Could not reach the community agent.");
    }
  }

  return (
    <Tooltip>
      <TooltipTrigger
        render={
          <div className="flex items-center gap-2" />
        }
      >
        {value ? (
          <Wifi className="size-4 text-risk-normal" />
        ) : (
          <WifiOff className="size-4 text-risk-watch-subtle-foreground" />
        )}
        <Switch
          checked={value}
          onCheckedChange={toggle}
          aria-label="Connectivity"
        />
        <Badge variant={value ? "secondary" : "outline"}>
          {value ? "Online" : "Offline"}
        </Badge>
      </TooltipTrigger>
      <TooltipContent>
        {value
          ? "Referrals sync to the facility agent."
          : "The community agent decides offline and queues referrals."}
      </TooltipContent>
    </Tooltip>
  );
}
