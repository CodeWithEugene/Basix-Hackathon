"use client";

import { useState } from "react";
import { Check, Copy } from "lucide-react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { ScrollArea } from "@/components/ui/scroll-area";

type Node = string | Node[];

function renderNode(node: Node, depth: number): React.ReactNode {
  if (!Array.isArray(node)) {
    const isStv = typeof node === "string" && /^[-\d.]+$/.test(node);
    return (
      <span className={isStv ? "text-primary" : "text-foreground"}>{node} </span>
    );
  }
  const [head, ...rest] = node;
  return (
    <div style={{ marginLeft: depth > 0 ? 14 : 0 }}>
      <Collapsible defaultOpen={depth < 2}>
        <CollapsibleTrigger className="cursor-pointer text-accent-foreground hover:underline">
          ({String(head)}
        </CollapsibleTrigger>
        <CollapsibleContent>
          {rest.map((child, i) => (
            <div key={i}>{renderNode(child, depth + 1)}</div>
          ))}
          <span>)</span>
        </CollapsibleContent>
      </Collapsible>
    </div>
  );
}

export function ProofTree({
  tree,
  raw,
}: {
  tree: unknown;
  raw: string;
}) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(raw);
      setCopied(true);
      toast.success("Proof copied.");
      setTimeout(() => setCopied(false), 1500);
    } catch {
      toast.error("Copy failed.");
    }
  }

  return (
    <div className="grid gap-3">
      <div className="flex items-center justify-between">
        <p className="text-sm text-muted-foreground">
          The verbatim NAL proof term from Omega&apos;s lib_nal on PeTTa.
        </p>
        <Button variant="outline" size="sm" onClick={copy}>
          {copied ? <Check className="size-4" /> : <Copy className="size-4" />}
          Copy Proof
        </Button>
      </div>
      {Array.isArray(tree) && tree.length > 0 ? (
        <div className="rounded-md border p-3 font-mono text-xs leading-5">
          {renderNode(tree as Node, 0)}
        </div>
      ) : (
        <p className="text-sm text-muted-foreground">
          No rule fired, so there is no proof term. The near-miss findings are in
          the Reasoning tab.
        </p>
      )}
      {raw && (
        <ScrollArea className="h-40 rounded-md border bg-muted/50 p-3">
          <pre className="font-mono text-xs whitespace-pre-wrap break-all">{raw}</pre>
        </ScrollArea>
      )}
    </div>
  );
}
