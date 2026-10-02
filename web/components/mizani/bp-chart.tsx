"use client";

import { useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  ReferenceLine,
  XAxis,
  YAxis,
} from "recharts";

import type { EncounterDetail } from "@/lib/types";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
  type ChartConfig,
} from "@/components/ui/chart";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";

const config = {
  sbp: { label: "Systolic", color: "var(--chart-1)" },
  dbp: { label: "Diastolic", color: "var(--chart-2)" },
} satisfies ChartConfig;

function readingOf(enc: EncounterDetail, kind: "sbp" | "dbp"): number | null {
  for (const r of enc.readings) {
    const parts = r.replace(/[()]/g, "").split(/\s+/);
    // (reading R-01 E-03 sbp 116)
    if (parts[0] === "reading" && parts[3] === kind) {
      return Number(parts[4]);
    }
  }
  return null;
}

export function BpChart({ encounters }: { encounters: EncounterDetail[] }) {
  const [asTable, setAsTable] = useState(false);
  const data = encounters
    .slice()
    .sort((a, b) => a.ga_weeks - b.ga_weeks)
    .map((e) => ({
      label: `${e.ga_weeks}w · ${e.site === "home" ? "home" : "clinic"}`,
      sbp: readingOf(e, "sbp"),
      dbp: readingOf(e, "dbp"),
      witness: e.witness ?? e.site,
    }))
    .filter((d) => d.sbp != null || d.dbp != null);

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-base">BP Over Pregnancy</CardTitle>
            <CardDescription>
              Every reading this agent remembers, by witness.
            </CardDescription>
          </div>
          <Button variant="outline" size="sm" onClick={() => setAsTable(!asTable)}>
            {asTable ? "View As Chart" : "View As Table"}
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {data.length === 0 && (
          <p className="text-sm text-muted-foreground">No readings recorded yet.</p>
        )}
        {data.length > 0 && !asTable && (
          <ChartContainer config={config} className="h-64 w-full">
            <LineChart data={data} margin={{ left: 8, right: 8 }}>
              <CartesianGrid vertical={false} />
              <XAxis dataKey="label" tickLine={false} axisLine={false} />
              <YAxis domain={[40, 180]} tickLine={false} axisLine={false} />
              <ReferenceLine y={140} stroke="var(--risk-urgent)" strokeDasharray="4 4" />
              <ReferenceLine y={90} stroke="var(--risk-watch)" strokeDasharray="4 4" />
              <ChartTooltip content={<ChartTooltipContent />} />
              <ChartLegend content={<ChartLegendContent />} />
              <Line type="monotone" dataKey="sbp" stroke="var(--chart-1)" strokeWidth={2} dot />
              <Line type="monotone" dataKey="dbp" stroke="var(--chart-2)" strokeWidth={2} dot />
            </LineChart>
          </ChartContainer>
        )}
        {data.length > 0 && asTable && (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Visit</TableHead>
                <TableHead>Systolic</TableHead>
                <TableHead>Diastolic</TableHead>
                <TableHead>Witness</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {data.map((d, i) => (
                <TableRow key={i}>
                  <TableCell>{d.label}</TableCell>
                  <TableCell className="tabular">{d.sbp}</TableCell>
                  <TableCell className="tabular">{d.dbp}</TableCell>
                  <TableCell>{d.witness}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
}
