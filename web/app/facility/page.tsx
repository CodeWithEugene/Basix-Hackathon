"use client";

import { useRouter } from "next/navigation";
import { formatDistanceToNow } from "date-fns";
import { Inbox as InboxIcon } from "lucide-react";

import { useAgent } from "@/lib/api";
import { motherDisplay } from "@/lib/risk";
import type { ReferralListItem } from "@/lib/types";
import { RiskBadge } from "@/components/mizani/risk-badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Empty,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from "@/components/ui/empty";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

export default function FacilityInboxPage() {
  const { data, loading, error } = useAgent<{ referrals: ReferralListItem[] }>(
    "facility",
    "/referrals",
    { pollMs: 2000 },
  );
  const router = useRouter();
  const referrals = data?.referrals ?? [];

  const kpis = {
    today: referrals.length,
    emergency: referrals.filter((r) => r.reconciled_level === "emergency").length,
    urgent: referrals.filter((r) => r.reconciled_level === "urgent").length,
    awaiting: referrals.filter((r) => !r.reconciled_level).length,
  };

  return (
    <div className="grid gap-6">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Kpi title="Incoming Today" value={kpis.today} />
        <Kpi title="Emergency" value={kpis.emergency} tone="emergency" />
        <Kpi title="Urgent" value={kpis.urgent} tone="urgent" />
        <Kpi title="Awaiting Review" value={kpis.awaiting} tone="watch" />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Facility Inbox</CardTitle>
          <CardDescription>
            Mtwapa Health Centre · night shift · Baraka, nurse
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading && <Skeleton className="h-40 w-full" />}
          {error && (
            <Empty>
              <EmptyHeader>
                <EmptyMedia variant="icon">
                  <InboxIcon />
                </EmptyMedia>
                <EmptyTitle>Facility Agent Unreachable</EmptyTitle>
                <EmptyDescription>
                  Start the facility agent and refresh.
                </EmptyDescription>
              </EmptyHeader>
            </Empty>
          )}
          {!loading && !error && referrals.length === 0 && (
            <Empty>
              <EmptyHeader>
                <EmptyMedia variant="icon">
                  <InboxIcon />
                </EmptyMedia>
                <EmptyTitle>No Referrals Yet</EmptyTitle>
                <EmptyDescription>
                  Waiting for the community agent to sync.
                </EmptyDescription>
              </EmptyHeader>
            </Empty>
          )}
          {referrals.length > 0 && (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Mother</TableHead>
                  <TableHead>GA</TableHead>
                  <TableHead>Community Decision</TableHead>
                  <TableHead>Reconciled Decision</TableHead>
                  <TableHead>Changed</TableHead>
                  <TableHead>Arrived</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {referrals.map((r) => (
                  <TableRow
                    key={r.referral_id}
                    className="cursor-pointer"
                    onClick={() => router.push(`/facility/${r.referral_id}`)}
                  >
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Avatar className="size-7">
                          <AvatarFallback className="text-xs">
                            {motherDisplay(r.mother_id).slice(0, 2).toUpperCase()}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="font-medium">{motherDisplay(r.mother_id)}</p>
                          <p className="text-xs text-muted-foreground">{r.mother_id}</p>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="tabular">
                      {r.ga_weeks != null ? `${r.ga_weeks}w` : ""}
                    </TableCell>
                    <TableCell>
                      {r.edge_level ? <RiskBadge level={r.edge_level} /> : "—"}
                    </TableCell>
                    <TableCell>
                      {r.reconciled_level ? (
                        <RiskBadge level={r.reconciled_level} />
                      ) : (
                        <Badge variant="outline">Pending</Badge>
                      )}
                    </TableCell>
                    <TableCell>
                      {r.changed && <Badge variant="secondary">Changed</Badge>}
                    </TableCell>
                    <TableCell>
                      <Tooltip>
                        <TooltipTrigger render={<span className="text-sm text-muted-foreground" />}>
                          {formatDistanceToNow(new Date(r.created_at), { addSuffix: true })}
                        </TooltipTrigger>
                        <TooltipContent>{r.created_at}</TooltipContent>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function Kpi({
  title,
  value,
  tone,
}: {
  title: string;
  value: number;
  tone?: "emergency" | "urgent" | "watch";
}) {
  const cls =
    tone === "emergency"
      ? "text-risk-emergency"
      : tone === "urgent"
        ? "text-risk-urgent"
        : tone === "watch"
          ? "text-risk-watch-subtle-foreground"
          : "";
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardDescription>{title}</CardDescription>
        <CardTitle className={`text-3xl font-medium tabular ${cls}`}>{value}</CardTitle>
      </CardHeader>
    </Card>
  );
}
