"use client";

import { useState } from "react";
import { Download } from "lucide-react";

import { useAgent } from "@/lib/api";
import type { LogEvent } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  InputGroup,
  InputGroupInput,
} from "@/components/ui/input-group";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

function LogTable({ role }: { role: "community" | "facility" }) {
  const { data, loading } = useAgent<{ events: LogEvent[] }>(
    role,
    "/memory/log?limit=500",
    { pollMs: 4000 },
  );
  const [filter, setFilter] = useState("");
  const events = (data?.events ?? []).filter(
    (e) => !filter || e.atom.toLowerCase().includes(filter.toLowerCase()),
  );

  return (
    <div className="grid gap-3">
      <div className="flex items-center justify-between gap-3">
        <InputGroup className="max-w-sm">
          <InputGroupInput
            placeholder="Filter atoms, for example contested"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          />
        </InputGroup>
        <Button
          variant="outline"
          size="sm"
          render={<a href={`/api/${role}/memory/export`} download={`${role}.metta`} />}
        >
          <Download className="size-4" />
          Download Memory
        </Button>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-16">N</TableHead>
            <TableHead>Time</TableHead>
            <TableHead>Op</TableHead>
            <TableHead>Atom</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {loading && (
            <TableRow>
              <TableCell colSpan={4}>Loading...</TableCell>
            </TableRow>
          )}
          {events.map((e) => (
            <TableRow key={e.n}>
              <TableCell className="tabular text-muted-foreground">{e.n}</TableCell>
              <TableCell className="text-xs text-muted-foreground">{e.ts}</TableCell>
              <TableCell>
                <Badge variant={e.op === "add" ? "secondary" : "outline"}>
                  {e.op === "add" ? "Add" : "Remove"}
                </Badge>
              </TableCell>
              <TableCell>
                <Tooltip>
                  <TooltipTrigger
                    render={
                      <span className="block max-w-md truncate font-mono text-xs" />
                    }
                  >
                    {e.atom}
                  </TooltipTrigger>
                  <TooltipContent className="max-w-lg">
                    <p className="font-mono text-xs break-all">{e.atom}</p>
                  </TooltipContent>
                </Tooltip>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

export default function AuditPage() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Audit Log</CardTitle>
        <CardDescription>
          The append-only atom log of each agent. Every mutation is here:
          readings, signs, syncs, contests, decisions.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="facility">
          <TabsList>
            <TabsTrigger value="community">Community Agent</TabsTrigger>
            <TabsTrigger value="facility">Facility Agent</TabsTrigger>
          </TabsList>
          <TabsContent value="community" className="mt-4">
            <LogTable role="community" />
          </TabsContent>
          <TabsContent value="facility" className="mt-4">
            <LogTable role="facility" />
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
