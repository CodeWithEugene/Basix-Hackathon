;; ================================================================
;; Mizani edge rule pack (edge-v1): the small pack the community agent
;; carries offline. Sources: WHO SMART ANC decision tables DT.01, DT.04,
;; DT.12, DT.17; Kenya MOH Mother and Child Health Handbook (2020).
;; Simplified for demonstration; not clinical advice.
;; ================================================================

(active-pack edge-v1)
(pack-version edge-v1 v1)

;; ---- thresholds: (threshold <finding> <reading-kind> <min>) ----
(threshold htn sbp 140)                  ;; WHO ANC.DT.17
(threshold htn dbp 90)
(threshold severe-htn sbp 160)           ;; WHO ANC.DT.17 severe hypertension
(threshold severe-htn dbp 110)
(threshold proteinuria protein 2)        ;; WHO ANC.DT.17: proteinuria ++ or more
(threshold fever temp 38)                ;; WHO ANC.DT.01 / DT.04

;; ---- sign sets ----
;; WHO ANC.DT.17 severe symptoms (severe pre-eclampsia features).
(severe-sign severe-headache)
(severe-sign visual-disturbance)
(severe-sign epigastric-pain)
(severe-sign dizziness)
(severe-sign vomiting)

;; WHO ANC.DT.01 danger signs + MCH booklet additions (catch-all set;
;; convulsions, bleeding, fever, rfm, prom, breathing also have own rules).
(danger-sign severe-headache)
(danger-sign visual-disturbance)
(danger-sign severe-abdominal-pain)
(danger-sign unconscious)
(danger-sign looks-very-ill)
(danger-sign vomiting)
(danger-sign swelling-face-hands)

;; ---- rules: (rule <pack> <id> <version> (==> <antecedent> <conc>) <stv>) ----

;; WHO ANC.DT.01: convulsions or heavy bleeding mean emergency referral.
(rule edge-v1 r_danger_bleed v1 (==> vaginal-bleeding emergency-referral) (stv 0.95 0.9))
(rule edge-v1 r_danger_fits v1 (==> convulsions emergency-referral) (stv 0.95 0.9))

;; WHO ANC.DT.17: repeat BP >= 160/110 is severe hypertension, emergency.
(rule edge-v1 r_severe_htn v1 (==> severe-htn emergency-referral) (stv 0.9 0.9))

;; WHO ANC.DT.17: repeat BP >= 140/90 plus any severe symptom, urgent today.
(rule edge-v1 r_htn_symptom v1 (==> (∧ htn severe-symptom) urgent-referral) (stv 0.9 0.9))

;; WHO ANC.DT.01: any other danger sign on its own, urgent today.
(rule edge-v1 r_danger_sign v1 (==> any-danger-sign urgent-referral) (stv 0.9 0.85))

;; WHO ANC.DT.12 + CHP kit gap (no dipstick): confirmed hypertension with no
;; severe symptom needs facility urine testing, urgent today.
(rule edge-v1 r_htn_confirmed v1 (==> htn-confirmed urgent-referral) (stv 0.85 0.85))

;; WHO ANC.DT.01 / MCH booklet: fever, reduced fetal movement, breathing.
(rule edge-v1 r_fever v1 (==> fever urgent-referral) (stv 0.85 0.85))
(rule edge-v1 r_rfm v1 (==> rfm urgent-referral) (stv 0.85 0.85))
(rule edge-v1 r_prom v1 (==> prom urgent-referral) (stv 0.85 0.85))
(rule edge-v1 r_breath v1 (==> breathing-difficulty urgent-referral) (stv 0.85 0.85))

;; WHO ANC.DT.04: a high reading not repeated after rest is unconfirmed;
;; repeat it after 10 to 15 minutes rest before acting.
(rule edge-v1 r_htn_unconfirmed v1 (==> htn-unconfirmed watch-referral) (stv 0.8 0.8))
