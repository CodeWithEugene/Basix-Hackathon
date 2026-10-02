"use client";

import { useState } from "react";
import { Ban, CircleCheck, CircleDashed, GitMerge, Undo2 } from "lucide-react";

import { premiseLabel } from "@/lib/risk";
import type { Premise } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { Input } from "@/components/ui/input";
import {
  Item,
  ItemActions,
  ItemContent,
  ItemDescription,
  ItemGroup,
  ItemMedia,
  ItemTitle,
} from "@/components/ui/item";
import {
  NativeSelect,
  NativeSelectOption,
} from "@/components/ui/native-select";
import { Textarea } from "@/components/ui/textarea";

const STATUS_ICON: Record<string, typeof CircleCheck> = {
  used: CircleCheck,
  revised: GitMerge,
  defeated: Ban,
  withdrawn: Undo2,
  missing: CircleDashed,
  "below-threshold": CircleDashed,
};

const STATUS_CLASS: Record<string, string> = {
  used: "text-risk-normal",
  revised: "text-primary",
  defeated: "text-muted-foreground",
  withdrawn: "text-risk-watch-subtle-foreground",
  missing: "text-muted-foreground",
  "below-threshold": "text-risk-watch-subtle-foreground",
};

export function PremiseList({
  premises,
  onContest,
  canContest = false,
}: {
  premises: Premise[];
  onContest?: (premiseId: string, reason: string, by: string, sourceId?: string) => Promise<void>;
  canContest?: boolean;
}) {
  const [contesting, setContesting] = useState<Premise | null>(null);

  return (
    <>
      <ItemGroup className="gap-2">
        {premises.map((p, i) => {
          const Icon = STATUS_ICON[p.status] ?? CircleDashed;
          return (
            <Item key={`${p.id}-${i}`} variant="outline" className="items-start">
              <ItemMedia variant="icon" className={STATUS_CLASS[p.status]}>
                <Icon className="size-4" />
              </ItemMedia>
              <ItemContent>
                <ItemTitle>
                  {premiseLabel(p.id)}
                  {p.truth && (
                    <span className="ml-2 font-mono text-xs text-muted-foreground tabular">
                      f {p.truth.f.toFixed(2)} · c {p.truth.c.toFixed(2)}
                    </span>
                  )}
                </ItemTitle>
                <ItemDescription className="flex flex-wrap items-center gap-1.5">
                  <Badge variant="outline" className="capitalize">
                    {p.status}
                  </Badge>
                  {p.sources.slice(0, 3).map((s, j) => (
                    <HoverCard key={j}>
                      <HoverCardTrigger
                        render={<Badge variant="secondary" className="font-normal" />}
                      >
                        {s.id}
                      </HoverCardTrigger>
                      <HoverCardContent className="w-96">
                        <p className="font-mono text-xs break-all">{s.from}</p>
                        {s.tv && (
                          <p className="mt-1 font-mono text-xs text-muted-foreground">
                            (stv {s.tv.f} {s.tv.c})
                          </p>
                        )}
                        {s.by && (
                          <p className="mt-1 text-xs text-muted-foreground">
                            defeated by: {s.by}
                          </p>
                        )}
                      </HoverCardContent>
                    </HoverCard>
                  ))}
                  {p.withdrawn.map((w, j) => (
                    <span key={j} className="text-xs text-muted-foreground">
                      withdrawn by {w.by}: &quot;{w.reason}&quot;
                    </span>
                  ))}
                </ItemDescription>
              </ItemContent>
              {canContest && (p.status === "used" || p.status === "revised") && (
                <ItemActions>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setContesting(p)}
                  >
                    Contest
                  </Button>
                </ItemActions>
              )}
            </Item>
          );
        })}
      </ItemGroup>
      <ContestDialog
        key={contesting?.id ?? "none"}
        premise={contesting}
        onClose={() => setContesting(null)}
        onSubmit={async (reason, by, sourceId) => {
          if (contesting && onContest) {
            await onContest(contesting.id, reason, by, sourceId);
          }
          setContesting(null);
        }}
      />
    </>
  );
}

function ContestDialog({
  premise,
  onClose,
  onSubmit,
}: {
  premise: Premise | null;
  onClose: () => void;
  onSubmit: (reason: string, by: string, sourceId?: string) => Promise<void>;
}) {
  const evidence = (premise?.sources ?? []).filter((s) => s.kind === "evidence");
  const [sourceId, setSourceId] = useState<string>(evidence[0]?.id ?? "");
  const [reason, setReason] = useState("");
  const [by, setBy] = useState("nurse-baraka");
  const [busy, setBusy] = useState(false);

  return (
    <Dialog open={!!premise} onOpenChange={(open) => !open && onClose()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Contest This Premise</DialogTitle>
          <DialogDescription>
            {premise ? premiseLabel(premise.id) : ""} will be withdrawn and the
            decision will recompute without it. Your name and reason are recorded.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-3">
          {evidence.length > 1 && (
            <NativeSelect
              value={sourceId}
              onChange={(e) => setSourceId(e.target.value)}
              aria-label="Observation to withdraw"
            >
              {evidence.map((s) => (
                <NativeSelectOption key={s.id} value={s.id}>
                  {s.id} · {s.from}
                </NativeSelectOption>
              ))}
            </NativeSelect>
          )}
          <Textarea
            placeholder="Reason, for example: headache resolved after paracetamol"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            rows={3}
          />
          <Input
            value={by}
            onChange={(e) => setBy(e.target.value)}
            aria-label="Your name"
          />
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button
            disabled={!reason.trim() || !by.trim() || busy}
            onClick={async () => {
              setBusy(true);
              try {
                await onSubmit(
                  reason.trim(),
                  by.trim(),
                  evidence.length > 1 ? sourceId : undefined,
                );
                setReason("");
              } finally {
                setBusy(false);
              }
            }}
          >
            Withdraw Premise
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
