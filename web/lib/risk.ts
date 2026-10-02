import type { RiskLevel } from "./types";

export const LEVEL_LABEL: Record<RiskLevel, string> = {
  normal: "Normal",
  watch: "Watch",
  urgent: "Urgent",
  emergency: "Emergency",
};

export const LEVEL_ORDER: Record<RiskLevel, number> = {
  normal: 0,
  watch: 1,
  urgent: 2,
  emergency: 3,
};

// Badge classes per level. Colour always pairs with an icon and a label.
export const LEVEL_BADGE_CLASS: Record<RiskLevel, string> = {
  normal: "bg-risk-normal-subtle text-risk-normal-subtle-foreground",
  watch: "bg-risk-watch-subtle text-risk-watch-subtle-foreground border border-risk-watch/40",
  urgent: "bg-risk-urgent text-risk-urgent-foreground",
  emergency: "bg-risk-emergency text-risk-emergency-foreground font-semibold",
};

export const LEVEL_CARD_CLASS: Record<RiskLevel, string> = {
  normal: "",
  watch: "",
  urgent: "border-l-4 border-l-risk-urgent",
  emergency: "border-l-4 border-l-risk-emergency",
};

export function premiseLabel(id: string): string {
  const map: Record<string, string> = {
    "htn": "High blood pressure",
    "severe-htn": "Severe high blood pressure",
    "htn-confirmed": "High blood pressure, confirmed by repeat",
    "htn-unconfirmed": "High reading, not repeated",
    "proteinuria": "Urine protein 2+",
    "new-onset": "New onset after 20 weeks",
    "chronic-htn": "Chronic hypertension",
    "severe-symptom": "Severe symptom",
    "severe-headache": "Severe headache",
    "visual-disturbance": "Blurred vision",
    "epigastric-pain": "Epigastric pain",
    "dizziness": "Dizziness",
    "vomiting": "Severe vomiting",
    "any-danger-sign": "Danger sign",
    "vaginal-bleeding": "Vaginal bleeding",
    "convulsions": "Convulsions",
    "fever": "Fever",
    "rfm": "Reduced fetal movement",
    "prom": "Waters broken, preterm",
    "breathing-difficulty": "Difficulty breathing",
    "late-ga": "At or past 20 weeks",
    "preterm-ga": "Before 37 weeks",
    "postpartum": "After birth",
    "early-normal-bp": "Normal BP in memory",
    "si-urgent": "Shock index at or above 0.9",
    "si-emergency": "Shock index at or above 1.4",
    "pph-loss": "Blood loss 300 mL or more",
    "pph-loss-500": "Blood loss 500 mL or more",
    "abnormal-haemodynamic": "Abnormal vitals",
    "severe-anaemia": "Severe anaemia",
    "none": "No rule fired",
  };
  return map[id] ?? id;
}

export function premiseLabelSw(id: string): string {
  const map: Record<string, string> = {
    "htn": "Presha iko juu",
    "severe-htn": "Presha iko juu sana",
    "htn-confirmed": "Presha imethibitishwa",
    "htn-unconfirmed": "Kipimo hakijarudiwa",
    "proteinuria": "Protini kwenye mkojo",
    "new-onset": "Imeanza baada ya wiki 20",
    "chronic-htn": "Presha ya kudumu",
    "severe-symptom": "Dalili kali",
    "severe-headache": "Kichwa kinauma sana",
    "visual-disturbance": "Kuona giza",
    "epigastric-pain": "Maumivu ya tumbo juu",
    "dizziness": "Kizunguzungu",
    "vomiting": "Kutapika sana",
    "any-danger-sign": "Dalili ya hatari",
    "vaginal-bleeding": "Kutokwa na damu",
    "convulsions": "Kifafa",
    "fever": "Homa",
    "rfm": "Mtoto amepunguza kucheza",
    "prom": "Maji yamevunja, mapema",
    "breathing-difficulty": "Kushindwa kupumua",
    "late-ga": "Wiki 20 au zaidi",
    "preterm-ga": "Chini ya wiki 37",
    "postpartum": "Baada ya kujifungua",
    "early-normal-bp": "Presha ya kawaida awali",
    "si-urgent": "Shock index 0.9 au zaidi",
    "si-emergency": "Shock index 1.4 au zaidi",
    "pph-loss": "Damu 300 mL au zaidi",
    "pph-loss-500": "Damu 500 mL au zaidi",
    "abnormal-haemodynamic": "Vitals si vya kawaida",
    "severe-anaemia": "Upungufu mkubwa wa damu",
    "none": "Hakuna kanuni iliyowaka",
  };
  return map[id] ?? id;
}

export function motherDisplay(id: string): string {
  const map: Record<string, string> = {
    "M-AMINA": "Amina",
    "M-WANJIKU": "Wanjiku",
    "M-NAFULA": "Nafula",
  };
  return map[id] ?? id;
}

export function fmtStv(t?: { f: number; c: number } | null): string {
  if (!t) return "unknown";
  return `f ${t.f.toFixed(2)} · c ${t.c.toFixed(2)}`;
}
