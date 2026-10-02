import { Building2, Home } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";

// Renders the raw atoms of one witness's encounters as a readable card.
export function WitnessCard({
  title,
  subtitle,
  atoms,
  memoryAtoms,
  offline,
}: {
  title: string;
  subtitle: string;
  atoms: string[];
  memoryAtoms?: string[];
  offline?: boolean;
}) {
  const Icon = title.toLowerCase().includes("community") ? Home : Building2;
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2 text-base">
            <Icon className="size-4 text-muted-foreground" />
            {title}
          </CardTitle>
          {offline && <Badge variant="outline">Offline</Badge>}
        </div>
        <CardDescription>{subtitle}</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-2">
        {atoms.length === 0 && (
          <p className="text-sm text-muted-foreground">Nothing recorded yet.</p>
        )}
        {atoms.map((a, i) => (
          <AtomLine key={i} atom={a} />
        ))}
        {memoryAtoms && memoryAtoms.length > 0 && (
          <>
            <Separator className="my-2" />
            <p className="text-xs font-medium text-muted-foreground">From Memory</p>
            {memoryAtoms.map((a, i) => (
              <AtomLine key={`m-${i}`} atom={a} muted />
            ))}
          </>
        )}
      </CardContent>
    </Card>
  );
}

function AtomLine({ atom, muted = false }: { atom: string; muted?: boolean }) {
  const kind = atom.startsWith("(reading")
    ? "secondary"
    : atom.startsWith("(sign")
      ? "default"
      : atom.startsWith("(treatment")
        ? "destructive"
        : "outline";
  return (
    <div className="flex items-start gap-2">
      <Badge variant={kind as "secondary"} className="mt-0.5 shrink-0 font-mono text-[10px]">
        {atom.slice(1, atom.indexOf(" "))}
      </Badge>
      <p className={`font-mono text-xs break-all ${muted ? "text-muted-foreground" : ""}`}>
        {atom}
      </p>
    </div>
  );
}
