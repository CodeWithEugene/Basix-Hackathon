import Link from "next/link";
import {
  ArrowRight,
  GitMerge,
  MemoryStick,
  Scale,
  WifiOff,
} from "lucide-react";

import { AgentHealthBadge } from "@/components/mizani/agent-health";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const CARDS = [
  {
    icon: WifiOff,
    title: "Decides Offline",
    body: "The community agent runs Omega with a small MeTTa rule pack, no network needed, and queues the referral.",
  },
  {
    icon: MemoryStick,
    title: "Remembers The Mother",
    body: "The facility agent holds her earlier visits, so a normal BP at 14 weeks makes today's hypertension new onset.",
  },
  {
    icon: GitMerge,
    title: "Shows Its Working",
    body: "Every premise carries a source and an Omega NAL truth value, and the nurse can contest any of them.",
  },
];

const STEPS = [
  "The CHP records the visit, offline, in Swahili, English or Sheng.",
  "The community agent decides with the edge rule pack and queues the referral.",
  "When the network returns, the facility agent reconciles both witnesses with memory.",
  "The nurse sees the proof, the diff, and can contest any premise.",
];

export default function WelcomePage() {
  return (
    <div className="mx-auto grid max-w-4xl gap-10 py-8">
      <div className="grid gap-4">
        <p className="text-sm font-medium text-muted-foreground">
          Omega Agent Without Borders
        </p>
        <h1 className="text-5xl font-light tracking-[-0.025em] md:text-6xl">
          Two Witnesses, One Referral
        </h1>
        <p className="max-w-2xl text-lg text-muted-foreground">
          Mizani weighs what the community health promoter saw against what the
          clinic sees, with Omega&apos;s own reasoning, and shows its working in
          English and Swahili.
        </p>
        <div className="flex flex-wrap items-center gap-3 pt-2">
          <Button render={<Link href="/community" />} size="lg">
            Start Community Visit
          </Button>
          <Button render={<Link href="/facility" />} variant="ghost" size="lg">
            Open Facility Inbox
            <ArrowRight className="size-4" />
          </Button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {CARDS.map((c) => (
          <Card key={c.title}>
            <CardHeader>
              <c.icon className="size-5 text-primary" />
              <CardTitle className="text-sm font-medium">{c.title}</CardTitle>
              <CardDescription>{c.body}</CardDescription>
            </CardHeader>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <Scale className="size-4" />
            How It Works
          </CardTitle>
        </CardHeader>
        <ol className="grid gap-3 px-6 pb-6">
          {STEPS.map((s, i) => (
            <li key={i} className="flex gap-3 text-sm">
              <span className="flex size-6 shrink-0 items-center justify-center rounded-full bg-secondary text-xs font-medium">
                {i + 1}
              </span>
              <span className="text-muted-foreground">{s}</span>
            </li>
          ))}
        </ol>
      </Card>

      <div className="flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
        <AgentHealthBadge role="community" />
        <AgentHealthBadge role="facility" />
        <span>Decision support, not diagnosis. Synthetic data only.</span>
      </div>
    </div>
  );
}
