;; ================================================================
;; Mizani full rule pack (full-v1): everything in the edge pack plus the
;; facility-only rules that need the mother's memory and facility tests.
;; Sources: WHO SMART ANC DT.01/04/12/17/25; ISSHP onset timing;
;; shock index literature (El Ayadi 2016; Nathan 2015, 2019; CRADLE VSA);
;; WHO/FIGO/ICM 2025 postpartum haemorrhage definition; WHO 2024 Hb cut-offs.
;; Simplified for demonstration; not clinical advice.
;; ================================================================

(active-pack full-v1)
(pack-version full-v1 v1)

;; ---- thresholds (as edge, plus facility kinds) ----
(threshold htn sbp 140)
(threshold htn dbp 90)
(threshold severe-htn sbp 160)
(threshold severe-htn dbp 110)
(threshold proteinuria protein 2)
(threshold fever temp 38)
(threshold si-urgent si 0.9)             ;; shock index: refer (El Ayadi 2016)
(threshold si-emergency si 1.4)          ;; shock index: urgent transfer
(threshold pph-loss blood-loss 300)      ;; WHO/FIGO/ICM 2025 PPH (with signs)
(threshold pph-loss-500 blood-loss 500)  ;; WHO/FIGO/ICM 2025 PPH (alone)
(threshold-low severe-anaemia hb 70)     ;; WHO 2024 severe band, g/L

;; abnormal-haemodynamic members (WHO/FIGO/ICM 2025: pulse > 100,
;; shock index > 1, SBP < 100, DBP < 60; >= encodes > within float tolerance)
(threshold abnormal-pulse pulse 100)
(threshold pph-si si 1.0)
(threshold-low pph-low-sbp sbp 100)
(threshold-low pph-low-dbp dbp 60)
(haemo-member abnormal-pulse)
(haemo-member pph-si)
(haemo-member-low pph-low-sbp)
(haemo-member-low pph-low-dbp)

;; ---- sign sets (as edge) ----
(severe-sign severe-headache)
(severe-sign visual-disturbance)
(severe-sign epigastric-pain)
(severe-sign dizziness)
(severe-sign vomiting)

(danger-sign severe-headache)
(danger-sign visual-disturbance)
(danger-sign severe-abdominal-pain)
(danger-sign unconscious)
(danger-sign looks-very-ill)
(danger-sign vomiting)
(danger-sign swelling-face-hands)

;; ---- edge-equivalent rules ----
(rule full-v1 r_danger_bleed v1 (==> vaginal-bleeding emergency-referral) (stv 0.95 0.9))
(rule full-v1 r_danger_fits v1 (==> convulsions emergency-referral) (stv 0.95 0.9))
(rule full-v1 r_severe_htn v1 (==> severe-htn emergency-referral) (stv 0.9 0.9))
(rule full-v1 r_htn_symptom v1 (==> (∧ htn severe-symptom) urgent-referral) (stv 0.9 0.9))
(rule full-v1 r_danger_sign v1 (==> any-danger-sign urgent-referral) (stv 0.9 0.85))
(rule full-v1 r_htn_confirmed v1 (==> htn-confirmed urgent-referral) (stv 0.85 0.85))
(rule full-v1 r_fever v1 (==> fever urgent-referral) (stv 0.85 0.85))
(rule full-v1 r_rfm v1 (==> rfm urgent-referral) (stv 0.85 0.85))
(rule full-v1 r_prom v1 (==> prom urgent-referral) (stv 0.85 0.85))
(rule full-v1 r_breath v1 (==> breathing-difficulty urgent-referral) (stv 0.85 0.85))
(rule full-v1 r_htn_unconfirmed v1 (==> htn-unconfirmed watch-referral) (stv 0.8 0.8))

;; ---- facility rules: onset timing, pre-eclampsia, shock index, PPH ----

;; Pre-eclampsia (WHO ANC.DT.17; ISSHP): new-onset hypertension plus
;; proteinuria >= 2+. new-onset is derived from memory (see reason.metta).
(rule full-v1 r_pe v1 (==> (∧ new-onset proteinuria) pre-eclampsia) (stv 0.95 0.9))

;; Pre-eclampsia with severe features: new onset plus proteinuria plus a
;; severe symptom, or new onset plus proteinuria plus severe hypertension.
(rule full-v1 r_pe_severe_symp v1
  (==> (∧ new-onset (∧ proteinuria severe-symptom)) pre-eclampsia-severe) (stv 0.95 0.9))
(rule full-v1 r_pe_severe_bp v1
  (==> (∧ new-onset (∧ proteinuria severe-htn)) pre-eclampsia-severe) (stv 0.95 0.9))

;; Shock index (pulse / systolic), computed per reading by the host.
(rule full-v1 r_shock v1 (==> si-urgent urgent-referral) (stv 0.85 0.85))
(rule full-v1 r_shock_high v1 (==> si-emergency emergency-referral) (stv 0.9 0.9))

;; Postpartum haemorrhage (WHO/FIGO/ICM 2025): >= 300 mL with an abnormal
;; haemodynamic sign (abnormal-haemodynamic synthesized by the host), or
;; >= 500 mL regardless. Postpartum encounters carry ga-weeks 0.
(rule full-v1 r_pph v1
  (==> (∧ postpartum (∧ pph-loss abnormal-haemodynamic)) emergency-referral) (stv 0.95 0.9))
(rule full-v1 r_pph_500 v1
  (==> (∧ postpartum pph-loss-500) emergency-referral) (stv 0.95 0.9))

;; Severe anaemia (WHO 2024: Hb < 70 g/L).
(rule full-v1 r_anaemia_severe v1 (==> severe-anaemia urgent-referral) (stv 0.85 0.85))
