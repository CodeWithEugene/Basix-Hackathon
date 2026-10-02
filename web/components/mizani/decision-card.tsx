"use client";

import { useState } from "react";

import { LEVEL_CARD_CLASS } from "@/lib/risk";
import type { Decision } from "@/lib/types";
import { RiskBadge } from "@/components/mizani/risk-badge";
import { TruthMeter } from "@/components/mizani/truth-meter";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export function DecisionCard({
  decision,
  size = "default",
  showMeta = true,
}: {
  decision: Decision;
  size?: "default" | "compact";
  showMeta?: boolean;
}) {
  const [tab, setTab] = useState("en");
  const lines = tab === "en" ? decision.explanation_en : decision.explanation_sw;
  return (
    <Card className={LEVEL_CARD_CLASS[decision.level]}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-3">
          <div>
            <CardDescription>
              {decision.agent === "community" ? "Community Decision" : "Reconciled Decision"}
            </CardDescription>
            <CardTitle className="mt-1 flex items-center gap-3">
              <RiskBadge level={decision.level} size={size === "compact" ? "sm" : "lg"} />
            </CardTitle>
          </div>
          {showMeta && decision.rule && (
            <Badge variant="outline" className="font-mono text-xs">
              {decision.rule.id} · {decision.pack}
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="grid gap-4">
        <div>
          <p className="font-medium">{decision.action_en}</p>
          <p className="text-sm text-muted-foreground">{decision.action_sw}</p>
        </div>
        {decision.conclusion !== "none" && (
          <TruthMeter truth={decision.truth} band={decision.band} />
        )}
        {size !== "compact" && lines.length > 0 && (
          <Tabs value={tab} onValueChange={setTab}>
            <TabsList>
              <TabsTrigger value="en">English</TabsTrigger>
              <TabsTrigger value="sw">Kiswahili</TabsTrigger>
            </TabsList>
            <TabsContent value={tab} className="mt-3">
              <ul className="list-disc space-y-1 pl-5 text-sm">
                {lines.map((l, i) => (
                  <li key={i}>{l}</li>
                ))}
              </ul>
            </TabsContent>
          </Tabs>
        )}
      </CardContent>
    </Card>
  );
}
