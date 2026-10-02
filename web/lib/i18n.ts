// Bilingual UI strings. Clinical sentences are rendered by the agent from
// the proof; these are interface chrome only. Swahili strings follow Kenya
// MOH community usage where known; flagged for native review.
export const SIGN_LABELS: Record<string, { en: string; sw: string }> = {
  "severe-headache": { en: "Severe headache", sw: "Kichwa kinauma sana" },
  "visual-disturbance": { en: "Blurred vision or darkness", sw: "Kuona giza au kukosa kuona vizuri" },
  "convulsions": { en: "Convulsions (fits)", sw: "Kifafa (degedege)" },
  "vaginal-bleeding": { en: "Vaginal bleeding", sw: "Kutokwa na damu" },
  "fever": { en: "Fever", sw: "Homa" },
  "severe-abdominal-pain": { en: "Severe abdominal pain", sw: "Tumbo linauma sana" },
  "rfm": { en: "Baby moving less or stopped", sw: "Mtoto amepunguza au ameacha kucheza" },
  "swelling-face-hands": { en: "Swelling of face or hands", sw: "Uso na mikono imevimba" },
  "breathing-difficulty": { en: "Difficulty breathing", sw: "Kushindwa kupumua" },
  "membranes-ruptured": { en: "Waters have broken", sw: "Maji yamevunja" },
  "in-labour": { en: "In labour now", sw: "Yuko kwenye uchungu" },
  "epigastric-pain": { en: "Pain in the upper abdomen", sw: "Maumivu ya juu ya tumbo" },
  "dizziness": { en: "Dizziness", sw: "Kizunguzungu" },
  "vomiting": { en: "Severe vomiting", sw: "Kutapika sana" },
  "unconscious": { en: "Unconscious", sw: "Hajui kichochote" },
  "looks-very-ill": { en: "Looks very ill", sw: "Anaonekana mgonjwa sana" },
};

export const DANGER_SIGNS = [
  "severe-headache",
  "visual-disturbance",
  "convulsions",
  "vaginal-bleeding",
  "fever",
  "severe-abdominal-pain",
  "rfm",
  "swelling-face-hands",
  "breathing-difficulty",
  "membranes-ruptured",
] as const;

export const UI = {
  disclaimerStrip: {
    en: "Demo with synthetic data. Decision support, not diagnosis.",
    sw: "Onyesho la data bandia. Hu ni msaada wa maamuzi, si uchunguzi.",
  },
  offline: {
    en: "Offline. Decisions run on this device's rule pack.",
    sw: "Hakuna mtandao. Maamuzi yanafanyika kwenye kifaa hiki.",
  },
  online: {
    en: "Online. Referrals sync to Mtwapa Health Centre.",
    sw: "Mtandao upo. Rufaa zinatumwa kwa Kituo cha Afya cha Mtwapa.",
  },
};
