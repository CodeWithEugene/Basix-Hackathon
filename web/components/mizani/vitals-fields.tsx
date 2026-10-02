"use client";

import type { ReadingState } from "@/lib/types";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group";
import {
  NativeSelect,
  NativeSelectOption,
} from "@/components/ui/native-select";
import { Switch } from "@/components/ui/switch";

export interface VitalsValue {
  sbp?: string;
  dbp?: string;
  pulse?: string;
  temp?: string;
  protein?: string;
  repeated: boolean;
  treatment: string;
}

export function VitalsFields({
  value,
  onChange,
  showProtein = false,
  showTreatment = false,
}: {
  value: VitalsValue;
  onChange: (v: VitalsValue) => void;
  showProtein?: boolean;
  showTreatment?: boolean;
}) {
  const set = (k: keyof VitalsValue, v: string | boolean) =>
    onChange({ ...value, [k]: v });

  return (
    <FieldGroup className="gap-4">
      <div className="grid grid-cols-2 gap-3">
        <Field>
          <FieldLabel>Systolic</FieldLabel>
          <InputGroup>
            <InputGroupInput
              inputMode="numeric"
              aria-label="Systolic"
              placeholder="152"
              value={value.sbp ?? ""}
              onChange={(e) => set("sbp", e.target.value)}
              className="text-base md:text-sm"
            />
            <InputGroupAddon align="inline-end">mmHg</InputGroupAddon>
          </InputGroup>
        </Field>
        <Field>
          <FieldLabel>Diastolic</FieldLabel>
          <InputGroup>
            <InputGroupInput
              inputMode="numeric"
              aria-label="Diastolic"
              placeholder="98"
              value={value.dbp ?? ""}
              onChange={(e) => set("dbp", e.target.value)}
              className="text-base md:text-sm"
            />
            <InputGroupAddon align="inline-end">mmHg</InputGroupAddon>
          </InputGroup>
        </Field>
        <Field>
          <FieldLabel>Pulse</FieldLabel>
          <InputGroup>
            <InputGroupInput
              inputMode="numeric"
              aria-label="Pulse"
              placeholder="88"
              value={value.pulse ?? ""}
              onChange={(e) => set("pulse", e.target.value)}
              className="text-base md:text-sm"
            />
            <InputGroupAddon align="inline-end">bpm</InputGroupAddon>
          </InputGroup>
        </Field>
        <Field>
          <FieldLabel>Temperature</FieldLabel>
          <InputGroup>
            <InputGroupInput
              inputMode="decimal"
              aria-label="Temperature"
              placeholder="36.8"
              value={value.temp ?? ""}
              onChange={(e) => set("temp", e.target.value)}
              className="text-base md:text-sm"
            />
            <InputGroupAddon align="inline-end">°C</InputGroupAddon>
          </InputGroup>
        </Field>
        {showProtein && (
          <Field>
            <FieldLabel>Urine Protein</FieldLabel>
            <NativeSelect
              value={value.protein ?? ""}
              onChange={(e) => set("protein", e.target.value)}
            >
              <NativeSelectOption value="">Not done</NativeSelectOption>
              {["0", "1", "2", "3", "4"].map((g) => (
                <NativeSelectOption key={g} value={g}>
                  {g}+
                </NativeSelectOption>
              ))}
            </NativeSelect>
          </Field>
        )}
        {showTreatment && (
          <Field>
            <FieldLabel>Treatment Given</FieldLabel>
            <NativeSelect
              value={value.treatment}
              onChange={(e) => set("treatment", e.target.value)}
            >
              <NativeSelectOption value="none">None</NativeSelectOption>
              <NativeSelectOption value="nifedipine-oral">Nifedipine</NativeSelectOption>
              <NativeSelectOption value="methyldopa">Methyldopa</NativeSelectOption>
              <NativeSelectOption value="magnesium-sulphate">Magnesium Sulphate</NativeSelectOption>
              <NativeSelectOption value="paracetamol">Paracetamol</NativeSelectOption>
              <NativeSelectOption value="other">Other</NativeSelectOption>
            </NativeSelect>
          </Field>
        )}
      </div>
      <Field orientation="horizontal" className="items-center justify-between rounded-md border p-3">
        <div>
          <FieldLabel>Repeated After 15 Minutes Rest</FieldLabel>
          <FieldDescription>
            WHO ANC guidance: repeat a raised reading after 10 to 15 minutes rest.
          </FieldDescription>
        </div>
        <Switch
          checked={value.repeated}
          onCheckedChange={(v) => set("repeated", v)}
          aria-label="Repeated after 15 minutes rest"
        />
      </Field>
    </FieldGroup>
  );
}

export function vitalsToReadings(v: VitalsValue): ReadingState[] {
  const out: ReadingState[] = [];
  const push = (kind: ReadingState["kind"], raw?: string) => {
    if (raw == null || raw === "") return;
    const n = Number(raw);
    if (Number.isFinite(n)) out.push({ kind, value: n, repeated: v.repeated });
  };
  push("sbp", v.sbp);
  push("dbp", v.dbp);
  push("pulse", v.pulse);
  push("temp", v.temp);
  if (v.protein) push("protein", v.protein);
  return out;
}
