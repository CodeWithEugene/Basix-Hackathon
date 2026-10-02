import { ArrowRight } from "lucide-react";

import type { Diff } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import {
  Item,
  ItemContent,
  ItemDescription,
  ItemGroup,
  ItemMedia,
  ItemTitle,
} from "@/components/ui/item";
import { Separator } from "@/components/ui/separator";

const CHANGE_LABEL: Record<string, string> = {
  level_changed: "Level Changed",
  action_changed: "Action Changed",
  premise_added: "Premise Added",
  premise_from_memory: "From Memory",
  premise_defeated: "Premise Defeated",
  premise_revised: "Premise Revised",
  premise_withdrawn: "Premise Withdrawn",
  rule_changed: "Rule Changed",
  truth_changed: "Truth Changed",
};

export function DiffPanel({
  diff,
  swahili = false,
}: {
  diff: Diff | null;
  swahili?: boolean;
}) {
  if (!diff || diff.changes.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">
        {swahili
          ? "Hakuna mabadiliko. Mashahidi wawili wanakubaliana."
          : "No changes. The two witnesses agree."}
      </p>
    );
  }
  return (
    <div className="grid gap-3">
      <div className="flex items-center gap-2 text-sm">
        <Badge variant="outline">Community Said</Badge>
        <ArrowRight className="size-4 text-muted-foreground" />
        <Badge variant="secondary">Reconciled</Badge>
      </div>
      <Separator />
      <ItemGroup className="gap-2">
        {diff.changes.map((c, i) => (
          <Item key={i} variant="outline" size="sm">
            <ItemMedia variant="icon">
              {c.type === "premise_defeated" || c.type === "premise_withdrawn" ? (
                <span className="font-mono text-muted-foreground">−</span>
              ) : (
                <span className="font-mono text-accent-foreground">+</span>
              )}
            </ItemMedia>
            <ItemContent>
              <ItemTitle className="flex items-center gap-2">
                <Badge variant="secondary" className="text-xs">
                  {CHANGE_LABEL[c.type] ?? c.type}
                </Badge>
                {c.before && c.after && c.type !== "rule_changed" && (
                  <span className="font-mono text-xs text-muted-foreground">
                    <span className="line-through">{c.before}</span>
                    <ArrowRight className="inline size-3 mx-1" />
                    <span>{c.after}</span>
                  </span>
                )}
              </ItemTitle>
              <ItemDescription>
                {swahili ? c.reason_sw : c.reason_en}
              </ItemDescription>
            </ItemContent>
          </Item>
        ))}
      </ItemGroup>
    </div>
  );
}
