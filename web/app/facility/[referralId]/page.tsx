"use client";

import { use, useState } from "react";
import { useRouter } from "next/navigation";
import { Siren } from "lucide-react";
import { toast } from "sonner";

import { api, useAgent } from "@/lib/api";
import { motherDisplay } from "@/lib/risk";
import type { Referral, ReadingState } from "@/lib/types";
import { DiffPanel } from "@/components/mizani/diff-panel";
import { PremiseList } from "@/components/mizani/premise-list";
import { ProofTree } from "@/components/mizani/proof-tree";
import { RiskBadge } from "@/components/mizani/risk-badge";
import { VitalsFields, vitalsToReadings, type VitalsValue } from "@/components/mizani/vitals-fields";
import { WitnessCard } from "@/components/mizani/witness-card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function ReconciliationPage({
  params,
}: {
  params: Promise<{ referralId: string }>;
}) {
  const { referralId } = use(params);
  const { data: referral, error, loading, reload } = useAgent<Referral>(
    "facility",
    `/referrals/${referralId}`,
    { pollMs: 3000 },
  );
  const router = useRouter();
  const [acknowledged, setAcknowledged] = useState(false);

  async function contest(premiseId: string, reason: string, by: string, sourceId?: string) {
    try {
      const updated = await api<Referral>(
        "facility",
        `/referrals/${referralId}/contest`,
        { method: "POST", body: JSON.stringify({ premise_id: premiseId, reason, by, source_id: sourceId }) },
      );
      const level = updated.reconciled?.level ?? "normal";
      toast.success(`Recomputed. Decision stayed ${level === "urgent" ? "Urgent" : level}.`);
      reload();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Contest failed.");
      throw e;
    }
  }

  if (loading) {
    return <Skeleton className="h-96 w-full" />;
  }
  if (error || !referral) {
    return (
      <Alert variant="destructive">
        <AlertTitle>Referral Not Found</AlertTitle>
        <AlertDescription>
          {error?.message ?? "This referral does not exist."}{" "}
          <Button variant="outline" size="sm" onClick={() => router.push("/facility")}>
            Back To Inbox
          </Button>
        </AlertDescription>
      </Alert>
    );
  }

  const reconciled = referral.reconciled;
  const isEmergency = reconciled?.level === "emergency";
  const communityAtoms = referral.encounters.community;
  const facilityAtoms = referral.encounters.facility;
  const memoryAtoms = facilityAtoms.filter(() => false); // memory shown below from /mothers

  return (
    <div className="grid gap-4">
      <div className="flex flex-wrap items-center gap-3">
        <h1 className="text-2xl font-semibold tracking-[-0.015em]">
          {motherDisplay(referral.mother_id)}
        </h1>
        <span className="text-sm text-muted-foreground">
          {referral.mother.age}y · G{referral.mother.gravida}P{referral.mother.para} ·{" "}
          {referral.referral_id}
        </span>
        {reconciled && <RiskBadge level={reconciled.level} size="lg" />}
      </div>

      {isEmergency && !acknowledged && (
        <Alert variant="destructive">
          <Siren className="size-4" />
          <AlertTitle>Emergency</AlertTitle>
          <AlertDescription className="flex items-center justify-between gap-3">
            <span>
              {reconciled!.action_en} {reconciled!.action_sw}
            </span>
            <AlertDialog>
              <AlertDialogTrigger
                render={<Button variant="outline" size="sm" />}
              >
                Acknowledge
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Acknowledge This Emergency?</AlertDialogTitle>
                  <AlertDialogDescription>
                    You confirm you have seen the reconciled decision and its
                    proof, and you are acting per protocol. This is recorded.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogAction onClick={() => setAcknowledged(true)}>
                    Acknowledge
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </AlertDescription>
        </Alert>
      )}

      <ResizablePanelGroup orientation="horizontal" className="hidden md:flex">
        <ResizablePanel defaultSize={50}>
          <div className="grid gap-4 pr-2">
            <WitnessCard
              title="Community Witness"
              subtitle="Zawadi, CHP · at the home · offline when recorded"
              atoms={communityAtoms}
              offline
            />
            <WitnessCard
              title="Facility Witness"
              subtitle="Baraka, nurse · Mtwapa Health Centre"
              atoms={facilityAtoms}
              memoryAtoms={memoryAtoms}
            />
            <AddReadingSheet referralId={referralId} onDone={reload} />
          </div>
        </ResizablePanel>
        <ResizableHandle withHandle />
        <ResizablePanel defaultSize={50}>
          <div className="pl-2">
            <DecisionPanel referral={referral} onContest={contest} />
          </div>
        </ResizablePanel>
      </ResizablePanelGroup>

      <div className="grid gap-4 md:hidden">
        <Tabs defaultValue="community">
          <TabsList className="w-full">
            <TabsTrigger value="community">Community</TabsTrigger>
            <TabsTrigger value="facility">Facility</TabsTrigger>
            <TabsTrigger value="decision">Decision</TabsTrigger>
          </TabsList>
          <TabsContent value="community" className="mt-3">
            <WitnessCard
              title="Community Witness"
              subtitle="Zawadi, CHP · at the home · offline when recorded"
              atoms={communityAtoms}
              offline
            />
          </TabsContent>
          <TabsContent value="facility" className="mt-3">
            <WitnessCard
              title="Facility Witness"
              subtitle="Baraka, nurse · Mtwapa Health Centre"
              atoms={facilityAtoms}
            />
            <div className="mt-3">
              <AddReadingSheet referralId={referralId} onDone={reload} />
            </div>
          </TabsContent>
          <TabsContent value="decision" className="mt-3">
            <DecisionPanel referral={referral} onContest={contest} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}

function DecisionPanel({
  referral,
  onContest,
}: {
  referral: Referral;
  onContest: (premiseId: string, reason: string, by: string, sourceId?: string) => Promise<void>;
}) {
  const reconciled = referral.reconciled;
  if (!reconciled) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base">Reconciled Decision</CardTitle>
          <CardDescription>
            Add the arrival readings to reconcile the two witnesses.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Skeleton className="h-32 w-full" />
        </CardContent>
      </Card>
    );
  }
  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <div>
            <CardDescription>Reconciled Decision</CardDescription>
            <CardTitle className="mt-1 flex items-center gap-2 text-base">
              <RiskBadge level={reconciled.level} />
              {reconciled.rule && (
                <span className="font-mono text-xs text-muted-foreground">
                  {reconciled.rule.id} · {reconciled.pack}
                </span>
              )}
            </CardTitle>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="reasoning">
          <TabsList>
            <TabsTrigger value="reasoning">Reasoning</TabsTrigger>
            <TabsTrigger value="proof">Proof</TabsTrigger>
            <TabsTrigger value="changes">Changes</TabsTrigger>
            <TabsTrigger value="sw">Kiswahili</TabsTrigger>
          </TabsList>
          <TabsContent value="reasoning" className="mt-4 grid gap-4">
            <div>
              <p className="font-medium">{reconciled.action_en}</p>
              <p className="text-sm text-muted-foreground">{reconciled.action_sw}</p>
            </div>
            <PremiseList
              premises={reconciled.premises}
              canContest
              onContest={onContest}
            />
          </TabsContent>
          <TabsContent value="proof" className="mt-4">
            <ProofTree tree={reconciled.proof_tree} raw={reconciled.proof_raw} />
          </TabsContent>
          <TabsContent value="changes" className="mt-4">
            <DiffPanel diff={referral.diff} />
          </TabsContent>
          <TabsContent value="sw" className="mt-4">
            <ul className="list-disc space-y-1 pl-5 text-sm">
              {reconciled.explanation_sw.map((l, i) => (
                <li key={i}>{l}</li>
              ))}
            </ul>
            {referral.diff && (
              <div className="mt-4">
                <DiffPanel diff={referral.diff} swahili />
              </div>
            )}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}

function AddReadingSheet({
  referralId,
  onDone,
}: {
  referralId: string;
  onDone: () => void;
}) {
  const [open, setOpen] = useState(false);
  const [vitals, setVitals] = useState<VitalsValue>({
    repeated: true,
    treatment: "none",
    sbp: "138",
    dbp: "88",
    protein: "2",
  });
  const [busy, setBusy] = useState(false);

  async function save() {
    setBusy(true);
    try {
      const readings: ReadingState[] = vitalsToReadings(vitals);
      await api("facility", "/encounters", {
        method: "POST",
        body: JSON.stringify({
          referral_id: referralId,
          readings,
          treatment: vitals.treatment === "none" ? null : vitals.treatment,
        }),
      });
      toast.success("Facility readings recorded and reconciled.");
      setOpen(false);
      onDone();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Could not record readings.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger render={<Button variant="outline" className="w-full" />}>
        Add Facility Reading
      </SheetTrigger>
      <SheetContent className="overflow-y-auto">
        <SheetHeader>
          <SheetTitle>Add Facility Reading</SheetTitle>
          <SheetDescription>
            Arrival readings, the repeat after rest, dipstick, and any treatment
            given on the way. The reconciliation recomputes immediately.
          </SheetDescription>
        </SheetHeader>
        <div className="grid gap-4 p-4">
          <VitalsFields
            value={vitals}
            onChange={setVitals}
            showProtein
            showTreatment
          />
          <Button onClick={save} disabled={busy}>
            Save And Reconcile
          </Button>
        </div>
      </SheetContent>
    </Sheet>
  );
}
