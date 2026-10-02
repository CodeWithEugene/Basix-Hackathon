"use client";

import { useState } from "react";
import { Wifi, WifiOff } from "lucide-react";
import { toast } from "sonner";

import { api, useAgent } from "@/lib/api";
import { motherDisplay } from "@/lib/risk";
import type {
  Decision,
  ExtractResponse,
  Mother,
  SignState,
} from "@/lib/types";
import { DecisionCard } from "@/components/mizani/decision-card";
import { SignToggles } from "@/components/mizani/sign-toggles";
import { VitalsFields, vitalsToReadings, type VitalsValue } from "@/components/mizani/vitals-fields";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
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
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Field, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import { Spinner } from "@/components/ui/spinner";
import { Textarea } from "@/components/ui/textarea";

type OutboxState = { online: boolean; pending: { packet_id: string }[] };

const DEFAULT_NOTE =
  "Mama analalamika kichwa kinauma sana tangu jana, anaona giza kidogo. Miguu imevimba.";

export default function CommunityPage() {
  const outbox = useAgent<OutboxState>("community", "/outbox", { pollMs: 4000 });
  const mothers = useAgent<{ mothers: Mother[] }>("community", "/mothers");
  const online = outbox.data?.online ?? false;

  const [motherId, setMotherId] = useState("M-AMINA");
  const [ga, setGa] = useState("34");
  const [note, setNote] = useState(DEFAULT_NOTE);
  const [signs, setSigns] = useState<SignState[]>([]);
  const [jevMarks, setJevMarks] = useState<Record<string, number>>({});
  const [reviewFlags, setReviewFlags] = useState<string[]>([]);
  const [vitals, setVitals] = useState<VitalsValue>({
    sbp: "152",
    dbp: "98",
    repeated: true,
    treatment: "none",
  });
  const [reading, setReading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [decision, setDecision] = useState<Decision | null>(null);
  const [synced, setSynced] = useState<boolean | null>(null);
  const [registerOpen, setRegisterOpen] = useState(false);

  async function readNote() {
    setReading(true);
    try {
      const res = await api<ExtractResponse>("community", "/visits/extract", {
        method: "POST",
        body: JSON.stringify({ note }),
      });
      if (res.mode === "offline_manual") {
        toast.info("Note reading needs a connection. Tap the signs below.");
        return;
      }
      const next: SignState[] = res.signs.map((s) => ({
        name: s.name,
        status: s.status as SignState["status"],
        source: "jev",
      }));
      setSigns(next);
      setJevMarks(
        Object.fromEntries(
          res.signs
            .filter((s) => s.jev_confidence != null)
            .map((s) => [s.name, s.jev_confidence as number]),
        ),
      );
      setReviewFlags(res.signs.filter((s) => s.status === "needs-review").map((s) => s.name));
      if (res.bp) {
        setVitals((v) => ({
          ...v,
          sbp: String(res.bp!.systolic),
          dbp: String(res.bp!.diastolic),
        }));
      }
      toast.success(`Note read by ${res.model ?? "Jev"}. Confirm the highlighted signs.`);
    } catch {
      toast.info("Note reading needs a connection. Tap the signs below.");
    } finally {
      setReading(false);
    }
  }

  async function submit() {
    setSubmitting(true);
    setSynced(null);
    try {
      const readings = vitalsToReadings(vitals);
      const mother = mothers.data?.mothers.find((m) => m.id === motherId);
      const res = await api<{ decision: Decision; queued: boolean; synced: boolean }>(
        "community",
        "/visits",
        {
          method: "POST",
          body: JSON.stringify({
            mother: mother ?? { id: motherId, age: 27, gravida: 2, para: 1 },
            ga_weeks: Number(ga) || 0,
            note,
            signs: signs.map((s) => ({
              ...s,
              status: s.status === "needs-review" ? "present" : s.status,
            })),
            readings,
          }),
        },
      );
      setDecision(res.decision);
      setSynced(res.synced);
      outbox.reload();
      if (res.decision.level === "emergency") {
        toast.error("Emergency. Stabilise and transfer now.");
      }
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "The visit could not be recorded.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-12">
      <div className="grid gap-4 lg:col-span-7">
        <Alert variant={online ? "default" : "destructive"}>
          {online ? <Wifi className="size-4" /> : <WifiOff className="size-4" />}
          <AlertTitle>{online ? "Online" : "Offline"}</AlertTitle>
          <AlertDescription>
            {online
              ? "Referrals sync to Mtwapa Health Centre."
              : "Decisions run on this device's rule pack (edge-v1)."}
          </AlertDescription>
        </Alert>

        <Card>
          <CardHeader>
            <CardTitle>Community Visit</CardTitle>
            <CardDescription>
              Zawadi, CHP · Kilifi County · eCHIS phone
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-5">
            <div className="grid grid-cols-2 gap-3">
              <Field>
                <FieldLabel>Mother</FieldLabel>
                <div className="flex gap-2">
                  <Select value={motherId} onValueChange={(v) => setMotherId(v ?? motherId)}>
                    <SelectTrigger>
                      <SelectValue placeholder="Pick a mother" />
                    </SelectTrigger>
                    <SelectContent>
                      {(mothers.data?.mothers ?? []).map((m) => (
                        <SelectItem key={m.id} value={m.id}>
                          {motherDisplay(m.id)} · {m.age}y · G{m.gravida}P{m.para}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Button variant="outline" onClick={() => setRegisterOpen(true)}>
                    Register
                  </Button>
                </div>
              </Field>
              <Field>
                <FieldLabel>Gestational Age (weeks)</FieldLabel>
                <Input
                  inputMode="numeric"
                  aria-label="Gestational age in weeks"
                  value={ga}
                  onChange={(e) => setGa(e.target.value)}
                  className="text-base md:text-sm"
                />
              </Field>
            </div>

            <Field>
              <FieldLabel>Visit Note</FieldLabel>
              <Textarea
                rows={3}
                value={note}
                onChange={(e) => setNote(e.target.value)}
                placeholder="Andika maelezo kwa Kiswahili, Kiingereza au Sheng"
              />
              <div className="flex items-center gap-2 pt-1">
                <Button
                  variant="outline"
                  onClick={readNote}
                  disabled={reading || !online || !note.trim()}
                >
                  {reading ? <Spinner /> : null}
                  Read Note
                </Button>
                {!online && (
                  <p className="text-xs text-muted-foreground">
                    Note reading needs a connection. Tap the signs below.
                  </p>
                )}
              </div>
            </Field>

            <div>
              <p className="mb-2 text-sm font-medium">Danger Signs</p>
              <SignToggles
                signs={signs}
                onChange={setSigns}
                jevMarks={jevMarks}
                reviewFlags={reviewFlags}
              />
            </div>

            <div>
              <p className="mb-2 text-sm font-medium">Vitals</p>
              <VitalsFields value={vitals} onChange={setVitals} />
            </div>

            <Button
              size="lg"
              className="h-11 w-full"
              onClick={submit}
              disabled={submitting}
            >
              {submitting ? <Spinner /> : null}
              Get Decision
            </Button>
          </CardContent>
        </Card>
      </div>

      <div className="lg:col-span-5">
        <div className="lg:sticky lg:top-6 grid gap-3">
          {!decision && !submitting && (
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Decision</CardTitle>
                <CardDescription>
                  The community agent&apos;s decision appears here, with its proof.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Skeleton className="h-32 w-full" />
              </CardContent>
            </Card>
          )}
          {submitting && (
            <Card>
              <CardContent className="flex items-center gap-3 py-8">
                <Spinner />
                <p className="text-sm text-muted-foreground">
                  Omega is reasoning over the visit...
                </p>
              </CardContent>
            </Card>
          )}
          {decision && (
            <>
              <DecisionCard decision={decision} />
              <div className="flex items-center gap-2">
                {synced ? (
                  <Badge className="bg-risk-normal-subtle text-risk-normal-subtle-foreground">
                    Synced to Mtwapa Health Centre
                  </Badge>
                ) : (
                  <Badge variant="outline">
                    Queued, will sync when connection returns
                  </Badge>
                )}
              </div>
            </>
          )}
        </div>
      </div>

      <RegisterMotherDialog
        open={registerOpen}
        onClose={() => setRegisterOpen(false)}
        onRegistered={(m) => {
          setMotherId(m.id);
          mothers.reload();
          setRegisterOpen(false);
        }}
      />
    </div>
  );
}

function RegisterMotherDialog({
  open,
  onClose,
  onRegistered,
}: {
  open: boolean;
  onClose: () => void;
  onRegistered: (m: Mother) => void;
}) {
  const [id, setId] = useState("M-NEEMA");
  const [age, setAge] = useState("26");
  const [gravida, setGravida] = useState("1");
  const [para, setPara] = useState("0");
  return (
    <Dialog open={open} onOpenChange={(o) => !o && onClose()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Register Mother</DialogTitle>
        </DialogHeader>
        <div className="grid gap-3">
          <Field>
            <FieldLabel>Mother Id (synthetic)</FieldLabel>
            <Input value={id} onChange={(e) => setId(e.target.value)} />
          </Field>
          <div className="grid grid-cols-3 gap-3">
            <Field>
              <FieldLabel>Age</FieldLabel>
              <Input inputMode="numeric" value={age} onChange={(e) => setAge(e.target.value)} />
            </Field>
            <Field>
              <FieldLabel>Gravida</FieldLabel>
              <Input inputMode="numeric" value={gravida} onChange={(e) => setGravida(e.target.value)} />
            </Field>
            <Field>
              <FieldLabel>Para</FieldLabel>
              <Input inputMode="numeric" value={para} onChange={(e) => setPara(e.target.value)} />
            </Field>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button
            onClick={() =>
              onRegistered({
                id,
                age: Number(age) || 0,
                gravida: Number(gravida) || 0,
                para: Number(para) || 0,
                ga_weeks: null,
              })
            }
          >
            Register
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
