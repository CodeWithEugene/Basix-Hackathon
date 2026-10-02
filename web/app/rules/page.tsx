"use client";

import { useAgent } from "@/lib/api";
import type { RuleItem } from "@/lib/types";
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
  ItemTitle,
} from "@/components/ui/item";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

function RuleList({ role }: { role: "community" | "facility" }) {
  const { data, loading } = useAgent<{ pack: string; rules: RuleItem[] }>(
    role,
    "/rules",
  );
  if (loading) return <Skeleton className="h-40 w-full" />;
  return (
    <ItemGroup className="gap-2">
      {(data?.rules ?? []).map((r) => (
        <Item key={`${r.pack}-${r.id}`} variant="outline">
          <ItemContent>
            <ItemTitle className="flex items-center gap-2">
              <span className="font-mono text-sm">{r.id}</span>
              <Badge variant="secondary" className="font-mono text-xs">
                {r.version}
              </Badge>
              <Badge variant="outline" className="font-mono text-xs">
                {r.truth}
              </Badge>
            </ItemTitle>
            <ItemDescription className="font-mono text-xs break-all">
              {r.body}
            </ItemDescription>
          </ItemContent>
        </Item>
      ))}
    </ItemGroup>
  );
}

export default function RulesPage() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Rule Packs</CardTitle>
        <CardDescription>
          The versioned MeTTa rule atoms each agent carries. Thresholds cite WHO
          SMART ANC decision tables, ISSHP, and the WHO/FIGO/ICM 2025 PPH
          definition. Simplified for demonstration; not clinical advice.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="facility">
          <TabsList>
            <TabsTrigger value="facility">Full Pack (Facility)</TabsTrigger>
            <TabsTrigger value="community">Edge Pack (Community)</TabsTrigger>
          </TabsList>
          <TabsContent value="facility" className="mt-4">
            <RuleList role="facility" />
          </TabsContent>
          <TabsContent value="community" className="mt-4">
            <RuleList role="community" />
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
