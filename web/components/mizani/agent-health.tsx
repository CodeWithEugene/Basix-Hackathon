"use client";

import { useAgent } from "@/lib/api";
import type { Health } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

function Dot({ ok }: { ok: boolean }) {
  return (
    <span
      className={`inline-block size-2 rounded-full ${ok ? "bg-risk-normal" : "bg-risk-emergency"}`}
      aria-hidden
    />
  );
}

export function AgentHealth() {
  const comm = useAgent<Health>("community", "/health", { pollMs: 5000 });
  const fac = useAgent<Health>("facility", "/health", { pollMs: 5000 });

  return (
    <div className="flex flex-col gap-1.5 text-xs">
      <HealthRow
        label="Community"
        health={comm.data}
        unreachable={!!comm.error}
      />
      <HealthRow
        label="Facility"
        health={fac.data}
        unreachable={!!fac.error}
      />
    </div>
  );
}

function HealthRow({
  label,
  health,
  unreachable,
}: {
  label: string;
  health?: Health;
  unreachable: boolean;
}) {
  if (unreachable) {
    return (
      <Tooltip>
        <TooltipTrigger render={<div className="flex items-center gap-2 text-muted-foreground" />}>
          <Dot ok={false} />
          <span>{label}: Unreachable</span>
        </TooltipTrigger>
        <TooltipContent>The {label.toLowerCase()} agent is not responding.</TooltipContent>
      </Tooltip>
    );
  }
  return (
    <Tooltip>
      <TooltipTrigger render={<div className="flex items-center gap-2 text-muted-foreground" />}>
        <Dot ok={!!health} />
        <span>
          {label}
          {health ? ` · ${health.pack}` : ""}
        </span>
      </TooltipTrigger>
      {health && (
        <TooltipContent className="font-mono text-xs">
          <div>omega {health.omega_commit}</div>
          <div>petta {health.petta} · swipl {health.swipl}</div>
          <div>{health.events} events · {health.decisions} decisions</div>
        </TooltipContent>
      )}
    </Tooltip>
  );
}

export function AgentHealthBadge({ role }: { role: "community" | "facility" }) {
  const { data, error } = useAgent<Health>(role, "/health", { pollMs: 5000 });
  if (error) {
    return <Badge variant="outline">Unreachable</Badge>;
  }
  if (!data) return null;
  return (
    <Badge variant="secondary" className="font-mono">
      {data.pack} · omega {data.omega_commit}
    </Badge>
  );
}
