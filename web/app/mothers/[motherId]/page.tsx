"use client";

import { use } from "react";

import { useAgent } from "@/lib/api";
import { motherDisplay } from "@/lib/risk";
import type { MotherMemory } from "@/lib/types";
import { BpChart } from "@/components/mizani/bp-chart";
import { RiskBadge } from "@/components/mizani/risk-badge";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
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
  Item,
  ItemContent,
  ItemDescription,
  ItemGroup,
  ItemMedia,
  ItemTitle,
} from "@/components/ui/item";
import { Skeleton } from "@/components/ui/skeleton";
import { Building2, Home } from "lucide-react";

export default function MotherMemoryPage({
  params,
}: {
  params: Promise<{ motherId: string }>;
}) {
  const { motherId } = use(params);
  const { data, loading } = useAgent<MotherMemory>("facility", `/mothers/${motherId}`);

  if (loading || !data) {
    return <Skeleton className="h-96 w-full" />;
  }

  const encounters = data.encounters
    .slice()
    .sort((a, b) => a.ga_weeks - b.ga_weeks || a.at.localeCompare(b.at));

  return (
    <div className="grid gap-6">
      <div className="flex items-center gap-4">
        <Avatar className="size-12">
          <AvatarFallback>
            {motherDisplay(motherId).slice(0, 2).toUpperCase()}
          </AvatarFallback>
        </Avatar>
        <div>
          <h1 className="text-2xl font-semibold tracking-[-0.015em]">
            {motherDisplay(motherId)}
          </h1>
          <p className="text-sm text-muted-foreground">
            {motherId} · what the facility agent remembers · {data.atom_count} events
          </p>
        </div>
      </div>

      <BpChart encounters={encounters} />

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Encounters</CardTitle>
          <CardDescription>
            Every visit the agent remembers, oldest first.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ItemGroup className="gap-2">
            {encounters.map((e) => {
              const Icon = e.site === "home" ? Home : Building2;
              return (
                <Item key={e.id} variant="outline">
                  <ItemMedia variant="icon">
                    <Icon className="size-4" />
                  </ItemMedia>
                  <ItemContent>
                    <ItemTitle className="flex items-center gap-2">
                      {e.id} · {e.ga_weeks} weeks
                      <Badge variant="secondary" className="font-normal">
                        {e.witness ?? e.site}
                      </Badge>
                    </ItemTitle>
                    <ItemDescription className="font-mono text-xs">
                      {[...e.readings, ...e.signs, ...e.treatments].join("  ·  ") ||
                        "no observations"}
                    </ItemDescription>
                  </ItemContent>
                </Item>
              );
            })}
          </ItemGroup>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Decisions About {motherDisplay(motherId)}</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-2">
          {data.decisions.length === 0 && (
            <p className="text-sm text-muted-foreground">No decisions yet.</p>
          )}
          {data.decisions.map((d) => (
            <div key={d.id} className="flex items-center gap-3 text-sm">
              <RiskBadge level={d.level} />
              <span className="font-mono text-xs text-muted-foreground">
                {d.id} · {d.rule?.id ?? "no rule"} · f {d.truth.f.toFixed(2)} c {d.truth.c.toFixed(2)}
              </span>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Memory Atoms</CardTitle>
          <CardDescription>
            The raw atoms this agent holds about {motherDisplay(motherId)}.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Accordion>
            <AccordionItem value="atoms">
              <AccordionTrigger>Show Atoms</AccordionTrigger>
              <AccordionContent>
                <div className="grid gap-1 font-mono text-xs">
                  {encounters.flatMap((e) =>
                    [e.atom, ...e.readings, ...e.signs, ...e.treatments].map((a, i) => (
                      <p key={`${e.id}-${i}`} className="break-all">
                        {a}
                      </p>
                    )),
                  )}
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </CardContent>
      </Card>
    </div>
  );
}
