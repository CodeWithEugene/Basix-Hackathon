"""Explanations in English and Swahili, rendered from the proof JSON.

Templates are filled from the proof, so an explanation can never claim
anything the proof does not contain. No LLM writes clinical text.
"""
from __future__ import annotations

LEVEL_LINES = {
    "emergency": (
        "Emergency. Stabilise and transfer now. Call the senior clinician.",
        "Dharura. Mtulize na umpeleke hospitali sasa. Mwite daktari mkuu.",
    ),
    "urgent": (
        "Urgent. Refer to the facility today.",
        "Haraka. Mpeleke kituo cha afya leo.",
    ),
    "watch": (
        "Watch. Repeat the reading after 15 minutes rest, then reassess.",
        "Angalia. Rudia kipimo baada ya dakika 15 za kupumzika, kisha tathmini tena.",
    ),
    "normal": (
        "Normal. Continue routine antenatal care.",
        "Kawaida. Endelea na kliniki za kawaida za ujauzito.",
    ),
}

FINDING_EN = {
    "htn": "high blood pressure (at or above 140/90)",
    "severe-htn": "severe high blood pressure (at or above 160/110)",
    "htn-confirmed": "high blood pressure confirmed by a repeat after rest",
    "htn-unconfirmed": "a high reading not yet repeated after rest",
    "proteinuria": "protein in the urine",
    "new-onset": "high blood pressure that started after 20 weeks",
    "chronic-htn": "high blood pressure known from before 20 weeks",
    "severe-symptom": "a severe symptom",
    "severe-headache": "a severe headache",
    "visual-disturbance": "blurred vision",
    "epigastric-pain": "pain in the upper abdomen",
    "dizziness": "dizziness",
    "vomiting": "severe vomiting",
    "any-danger-sign": "a danger sign",
    "vaginal-bleeding": "vaginal bleeding",
    "convulsions": "convulsions (fits)",
    "fever": "fever",
    "rfm": "reduced movement of the baby",
    "prom": "waters broken before labour, before 37 weeks",
    "breathing-difficulty": "difficulty breathing",
    "late-ga": "pregnancy at or past 20 weeks",
    "preterm-ga": "pregnancy before 37 weeks",
    "postpartum": "the days after birth",
    "early-normal-bp": "a normal blood pressure from earlier in pregnancy",
    "si-urgent": "a shock index at or above 0.9",
    "si-emergency": "a shock index at or above 1.4",
    "pph-loss": "measured blood loss at or above 300 mL",
    "pph-loss-500": "measured blood loss at or above 500 mL",
    "abnormal-haemodynamic": "an abnormal pulse, pressure or shock index",
    "severe-anaemia": "severe anaemia (Hb below 70 g/L)",
}

FINDING_SW = {
    "htn": "presha iko juu (140/90 au zaidi)",
    "severe-htn": "presha iko juu sana (160/110 au zaidi)",
    "htn-confirmed": "presha imethibitishwa juu baada ya kupimwa tena",
    "htn-unconfirmed": "kipimo cha juu ambacho hakijarudiwa baada ya kupumzika",
    "proteinuria": "protini kwenye mkojo",
    "new-onset": "presha iliyoanza baada ya wiki 20",
    "chronic-htn": "presha iliyokuwepo tangu kabla ya wiki 20",
    "severe-symptom": "dalili kali",
    "severe-headache": "kichwa kinauma sana",
    "visual-disturbance": "kuona giza au kukosa kuona vizuri",
    "epigastric-pain": "maumivu ya juu ya tumbo",
    "dizziness": "kizunguzungu",
    "vomiting": "kutapika sana",
    "any-danger-sign": "dalili ya hatari",
    "vaginal-bleeding": "kutokwa na damu",
    "convulsions": "kifafa (degedege)",
    "fever": "homa",
    "rfm": "mtoto amepunguza kucheza tumboni",
    "prom": "maji yamevunja kabla ya uchungu, kabla ya wiki 37",
    "breathing-difficulty": "kushindwa kupumua",
    "late-ga": "mimba imefikia wiki 20 au zaidi",
    "preterm-ga": "mimba bado chini ya wiki 37",
    "postpartum": "siku za baada ya kujifungua",
    "early-normal-bp": "presha ya kawaida mwanzoni mwa ujauzito",
    "si-urgent": "kimo cha mshtuko (shock index) kimefikia 0.9",
    "si-emergency": "kimo cha mshtuko (shock index) kimefikia 1.4",
    "pph-loss": "kupoteza damu 300 mL au zaidi",
    "pph-loss-500": "kupoteza damu 500 mL au zaidi",
    "abnormal-haemodynamic": "mapigo, presha au kimo cha mshtuko si cha kawaida",
    "severe-anaemia": "upungufu mkubwa wa damu (Hb chini ya 70)",
}


def _src_line_en(src: dict) -> str:
    """One human sentence for an evidence source, parsed from its (from ...) string."""
    f = src.get("from", "")
    parts = f.strip("()").split()
    # shapes: from E-17 home sbp 152 >= 140 | from E-17 home sign present | from E-17 home ga-weeks 14
    if len(parts) >= 6 and parts[0] == "from" and parts[2] in {"home", "facility"}:
        enc, site, kind = parts[1], parts[2], parts[3]
        if kind == "sign":
            return f"reported at the {site} ({enc})"
        if kind == "ga-weeks":
            return f"recorded at {parts[4]} weeks ({enc}, {site})"
        return f"{kind} {parts[4]} at the {site} ({enc})"
    if "derived-from" in f:
        return "derived from the mother's earlier visits"
    return f


def _src_line_sw(src: dict) -> str:
    f = src.get("from", "")
    parts = f.strip("()").split()
    if len(parts) >= 6 and parts[0] == "from" and parts[2] in {"home", "facility"}:
        enc, site, kind = parts[1], parts[2], parts[3]
        site_sw = "nyumbani" if site == "home" else "kituoni"
        if kind == "sign":
            return f"aliripotiwa {site_sw} ({enc})"
        if kind == "ga-weeks":
            return f"ilipimwa katika wiki {parts[4]} ({enc})"
        return f"{kind} {parts[4]} {site_sw} ({enc})"
    if "derived-from" in f:
        return "imetokana na kumbukumbu za mama za hapo awali"
    return f


def explain(decision: dict) -> tuple[list[str], list[str]]:
    """Render the explanation sentences from a decision dict."""
    en: list[str] = []
    sw: list[str] = []

    level_en, level_sw = LEVEL_LINES[decision["level"]]
    en.append(level_en)
    sw.append(level_sw)

    rule = decision.get("rule")
    if rule:
        en.append(f"Rule {rule['id']} ({rule['pack']}) decided this.")
        sw.append(f"Kanuni {rule['id']} ({rule['pack']}) ndiyo imeamua hili.")

    for p in decision.get("premises", []):
        fid = p["id"]
        fen = FINDING_EN.get(fid, fid)
        fsw = FINDING_SW.get(fid, fid)
        status = p["status"]
        if status in {"used", "revised"}:
            if fid == "htn-unconfirmed":
                en.append("The high reading was measured once, not repeated after rest, so Mizani is less sure.")
                sw.append("Kipimo cha juu kilipimwa mara moja tu bila kurudia baada ya kupumzika, kwa hivyo Mizani haina uhakika sana.")
            else:
                en.append(f"The proof uses {fen}.")
                sw.append(f"Ushahidi unaotumiwa: {fsw}.")
            if status == "revised":
                en.append("Two witnesses agree, so confidence rose.")
                sw.append("Mashahidi wawili wanakubaliana, kwa hivyo uhakika umeongezeka.")
            for src in p.get("sources", []):
                if src.get("memory"):
                    en.append(f"This comes from what Mizani remembers: {_src_line_en(src)}.")
                    sw.append(f"Hii inatoka kwa kumbukumbu za Mizani: {_src_line_sw(src)}.")
        elif status == "defeated":
            for src in p.get("sources", []):
                if src.get("kind") == "defeated":
                    en.append(
                        f"A reading for {fen} was set aside because it came after treatment, so it does not show the pressure is normal."
                    )
                    sw.append(
                        f"Kipimo cha {fsw} kimetengwa kwa sababu kilitokea baada ya dawa, kwa hivyo hakionyeshi kuwa presha ni ya kawaida."
                    )
        elif status == "withdrawn":
            for w in p.get("withdrawn", []):
                en.append(f"{fen.capitalize()} was withdrawn by {w['by']}: \"{w['reason']}\".")
                sw.append(f"{fsw} imeondolewa na {w['by']}: \"{w['reason']}\".")
        elif status == "missing":
            en.append(f"No evidence for {fen}.")
            sw.append(f"Hakuna ushahidi wa {fsw}.")

    tv = decision.get("truth") or {}
    if decision["conclusion"] != "none" and tv:
        en.append(f"How sure Mizani is: frequency {tv['f']:.2f}, confidence {tv['c']:.2f} (Omega NAL).")
        sw.append(f"Uhakika wa Mizani: frequency {tv['f']:.2f}, confidence {tv['c']:.2f} (Omega NAL).")

    en.append("Decision support, not diagnosis. A health worker makes the final decision.")
    sw.append("Hu ni msaada wa maamuzi, si uchunguzi wa mgonjwa. Mfanyakazi wa afya ndiye anaamua mwisho.")
    return en, sw
