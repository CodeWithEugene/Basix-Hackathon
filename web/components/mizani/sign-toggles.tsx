"use client";

import { DANGER_SIGNS, SIGN_LABELS, UI } from "@/lib/i18n";
import type { SignState } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";

const OPTIONS = [
  { value: "present", label: "Present" },
  { value: "absent", label: "Absent" },
  { value: "not-mentioned", label: "Not Asked" },
] as const;

export function SignToggles({
  signs,
  onChange,
  jevMarks = {},
  reviewFlags = [],
}: {
  signs: SignState[];
  onChange: (signs: SignState[]) => void;
  jevMarks?: Record<string, number>;
  reviewFlags?: string[];
}) {
  function setStatus(name: string, status: SignState["status"]) {
    const rest = signs.filter((s) => s.name !== name);
    onChange([...rest, { name, status, source: "chp" }]);
  }

  return (
    <FieldGroup className="gap-4">
      {DANGER_SIGNS.map((name) => {
        const current = signs.find((s) => s.name === name);
        const value = current?.status ?? "not-mentioned";
        const jevConf = jevMarks[name];
        const needsReview = reviewFlags.includes(name) || value === "needs-review";
        return (
          <Field
            key={name}
            orientation="horizontal"
            className="items-start justify-between"
            data-sign={name}
          >
            <div className="grid gap-1">
              <FieldLabel className="flex items-center gap-2">
                {SIGN_LABELS[name]?.en ?? name}
                {jevConf != null && (
                  <Badge variant="outline" className="font-normal">
                    Jev {jevConf.toFixed(2)}
                  </Badge>
                )}
                {needsReview && (
                  <Badge className="bg-risk-watch-subtle text-risk-watch-subtle-foreground border border-risk-watch/40">
                    Please Confirm
                  </Badge>
                )}
                {current?.source === "chp" && value !== "not-mentioned" && (
                  <Badge variant="secondary" className="font-normal">
                    Entered By CHP
                  </Badge>
                )}
              </FieldLabel>
              <FieldDescription>{SIGN_LABELS[name]?.sw}</FieldDescription>
            </div>
            <ToggleGroup
              value={[value]}
              onValueChange={(v) => {
                const next = (v as string[])[0];
                if (next) setStatus(name, next as SignState["status"]);
              }}
              className={needsReview ? "rounded-md ring-2 ring-risk-watch/60" : ""}
            >
              {OPTIONS.map((o) => (
                <ToggleGroupItem key={o.value} value={o.value} aria-label={o.label}>
                  {o.label}
                </ToggleGroupItem>
              ))}
            </ToggleGroup>
          </Field>
        );
      })}
    </FieldGroup>
  );
}

export const disclaimerStrip = UI.disclaimerStrip;
