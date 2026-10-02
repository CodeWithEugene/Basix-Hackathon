;; ================================================================
;; Mizani evidence layer.
;;
;; Turns provenance-tagged base atoms into evidence, counter-evidence
;; and defeated-evidence items for clinical findings. Every item carries
;; an Omega truth value (stv f c) derived from provenance.
;;
;; Base atoms (written by the agent through the memory log):
;;   (mother M-AMINA (age 27) (gravida 2) (para 1))
;;   (encounter E-17 M-AMINA (site home) (by chp) (ga-weeks 34) (at "..."))
;;   (reading R-31 E-17 sbp 152)
;;   (prov R-31 (repeated yes) (after-treatment none) (device aneroid))
;;   (sign S-11 E-17 severe-headache present (source chp))
;;   (treatment T-2 E-18 nifedipine-oral (at "..."))
;;   (witness E-17 community)
;;   (in-referral REF-1 E-17)
;;   (contested S-11 (by nurse-baraka) (reason "..."))
;;
;; Clinical content (thresholds, sign sets) lives in the rule packs.
;; Requires Omega lib_nal.metta (stv) loaded first.
;; ================================================================

;; ----------------------------------------------------------------
;; Truth values from provenance
;; ----------------------------------------------------------------

;; A reading repeated after rest confirms the measurement (WHO ANC.DT.04).
(= (reading-truth $r)
   (match &self (prov $r (repeated $rep) $at $dev)
     (if (== $rep yes) (stv 1.0 0.9) (stv 1.0 0.6))))

;; Symptoms are self-reported: a little less certain than a measurement.
;; A needs-review sign nobody confirmed is weak (fail safe, still present).
(= (sign-status-truth present) (stv 1.0 0.8))
(= (sign-status-truth needs-review) (stv 1.0 0.5))

;; ----------------------------------------------------------------
;; Guards
;; ----------------------------------------------------------------

;; True when atom id $id was withdrawn by a clinician.
(= (is-contested $id)
   (if (== (collapse (match &self (contested $id $b $r) $id)) ()) no yes))

;; True when any treatment was recorded for encounter $e.
(= (has-treatment $e)
   (if (== (collapse (match &self (treatment $t $e $drug (at $at)) $t)) ()) no yes))

;; ----------------------------------------------------------------
;; Readings -> evidence and counter-evidence (above/below thresholds)
;; ----------------------------------------------------------------

;; Evidence: reading at or above a (threshold <finding> <kind> <min>).
(= (reading-evidence $ref $m $f)
   (match &self (threshold $f $k $t)
     (match &self (in-referral $ref $e)
       (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
         (match &self (reading $r $e $k $val)
           (if (>= $val $t)
             (if (== (is-contested $r) no)
               (evidence $f $r (from $e $site $k $val >= $t) (reading-truth $r))
               (empty))
             (empty)))))))

;; Counter or defeated: reading below a threshold.
;; A below-threshold reading taken after a treatment (for example an
;; antihypertensive) is DEFEATED: it is not evidence the finding is absent.
(= (reading-counter $ref $m $f)
   (match &self (threshold $f $k $t)
     (match &self (in-referral $ref $e)
       (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
         (match &self (reading $r $e $k $val)
           (if (< $val $t)
             (if (== (is-contested $r) no)
               (if (== (has-treatment $e) yes)
                 (defeated $f $r (from $e $site $k $val < $t) (by treated-before-reading))
                 (counter $f $r (from $e $site $k $val < $t) (stv 0.0 0.8)))
               (empty))
             (empty)))))))

;; Evidence for low-threshold findings (for example severe anaemia: Hb < 70).
(= (reading-evidence-low $ref $m $f)
   (match &self (threshold-low $f $k $t)
     (match &self (in-referral $ref $e)
       (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
         (match &self (reading $r $e $k $val)
           (if (< $val $t)
             (if (== (is-contested $r) no)
               (evidence $f $r (from $e $site $k $val < $t) (reading-truth $r))
               (empty))
             (empty)))))))

;; ----------------------------------------------------------------
;; Signs -> evidence and counter-evidence
;; ----------------------------------------------------------------

;; A sign that is present (or needs-review, fail safe) is evidence for the
;; finding of the same name. An explicitly absent sign is counter-evidence.
(= (sign-evidence $ref $m $f)
   (match &self (in-referral $ref $e)
     (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
       (match &self (sign $s $e $f $status (source $src))
         (if (== (is-contested $s) no)
           (if (== $status present)
             (evidence $f $s (from $e $site sign present) (sign-status-truth present))
             (if (== $status needs-review)
               (evidence $f $s (from $e $site sign needs-review) (sign-status-truth needs-review))
               (empty)))
           (empty))))))

(= (sign-counter $ref $m $f)
   (match &self (in-referral $ref $e)
     (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
       (match &self (sign $s $e $f $status (source $src))
         (if (== (is-contested $s) no)
           (if (== $status absent)
             (counter $f $s (from $e $site sign absent) (stv 0.0 0.8))
             (empty))
           (empty))))))

;; ----------------------------------------------------------------
;; Synthesized finding sets (membership atoms live in the packs)
;; ----------------------------------------------------------------

;; severe-symptom: any sign in the pack's severe-sign set, present.
(= (severe-symptom-evidence $ref $m)
   (match &self (severe-sign $f)
     (match &self (in-referral $ref $e)
       (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
         (match &self (sign $s $e $f $status (source $src))
           (if (== (is-contested $s) no)
             (if (== $status present)
               (evidence severe-symptom $s (from $e $site sign $f) (sign-status-truth present))
               (if (== $status needs-review)
                 (evidence severe-symptom $s (from $e $site sign $f) (sign-status-truth needs-review))
                 (empty)))
             (empty)))))))

;; any-danger-sign: any sign in the pack's danger-sign set, present.
(= (danger-sign-evidence $ref $m)
   (match &self (danger-sign $f)
     (match &self (in-referral $ref $e)
       (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
         (match &self (sign $s $e $f $status (source $src))
           (if (== (is-contested $s) no)
             (if (== $status present)
               (evidence any-danger-sign $s (from $e $site sign $f) (sign-status-truth present))
               (if (== $status needs-review)
                 (evidence any-danger-sign $s (from $e $site sign $f) (sign-status-truth needs-review))
                 (empty)))
             (empty)))))))

;; ----------------------------------------------------------------
;; Hypertension confirmation variants (WHO ANC.DT.04 / DT.12)
;; ----------------------------------------------------------------

;; htn-confirmed: an above-threshold reading repeated after rest.
;; htn-unconfirmed: an above-threshold reading not repeated after rest.
(= (htn-variant-evidence $ref $m)
   (match &self (threshold htn $k $t)
     (match &self (in-referral $ref $e)
       (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
         (match &self (reading $r $e $k $val)
           (match &self (prov $r (repeated $rep) $atx $dev)
             (if (>= $val $t)
               (if (== (is-contested $r) no)
                 (if (== $rep yes)
                   (evidence htn-confirmed $r (from $e $site $k $val >= $t) (stv 1.0 0.9))
                   (evidence htn-unconfirmed $r (from $e $site $k $val >= $t) (stv 1.0 0.6)))
                 (empty))
               (empty))))))))

;; Counters apply to both variants (a normal rested repeat lowers
;; confidence that an unconfirmed high reading means hypertension).
(= (htn-variant-counter $ref $m)
   (match &self (threshold htn $k $t)
     (match &self (in-referral $ref $e)
       (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
         (match &self (reading $r $e $k $val)
           (if (< $val $t)
             (if (== (is-contested $r) no)
               (if (== (has-treatment $e) yes)
                 (superpose
                   ((defeated htn-unconfirmed $r (from $e $site $k $val < $t) (by treated-before-reading))
                    (defeated htn-confirmed $r (from $e $site $k $val < $t) (by treated-before-reading))))
                 (superpose
                   ((counter htn-unconfirmed $r (from $e $site $k $val < $t) (stv 0.0 0.8))
                    (counter htn-confirmed $r (from $e $site $k $val < $t) (stv 0.0 0.8)))))
               (empty))
             (empty)))))))

;; ----------------------------------------------------------------
;; abnormal-haemodynamic (WHO/FIGO/ICM 2025 PPH trigger sign):
;; pulse > 100, shock index >= 1, SBP < 100 or DBP < 60.
;; Membership atoms live in the full pack.
;; ----------------------------------------------------------------

(= (haemodynamic-evidence $ref $m)
   (match &self (haemo-member $f)
     (match &self (threshold $f $k $t)
       (match &self (in-referral $ref $e)
         (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
           (match &self (reading $r $e $k $val)
             (if (>= $val $t)
               (if (== (is-contested $r) no)
                 (evidence abnormal-haemodynamic $r (from $e $site $k $val >= $t) (reading-truth $r))
                 (empty))
               (empty))))))))

(= (haemodynamic-low-evidence $ref $m)
   (match &self (haemo-member-low $f)
     (match &self (threshold-low $f $k $t)
       (match &self (in-referral $ref $e)
         (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
           (match &self (reading $r $e $k $val)
             (if (< $val $t)
               (if (== (is-contested $r) no)
                 (evidence abnormal-haemodynamic $r (from $e $site $k $val < $t) (reading-truth $r))
                 (empty))
               (empty))))))))

;; ----------------------------------------------------------------
;; Composite findings decided from literal facts (Jev extracts, MeTTa decides)
;; ----------------------------------------------------------------

;; prom: membranes ruptured, not in labour, gestational age below 37 weeks.
(= (prom-evidence $ref $m)
   (match &self (in-referral $ref $e)
     (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
       (if (and (< $ga 37) (> $ga 0))
         (match &self (sign $sm $e membranes-ruptured present (source $src))
           (if (== (is-contested $sm) no)
             (if (== (collapse (match &self (sign $sl $e in-labour present (source $s2)) $sl)) ())
               (evidence prom $sm (from $e $site sign present) (sign-status-truth present))
               (empty))
             (empty)))
         (empty)))))

;; ----------------------------------------------------------------
;; Gestational-age findings
;; ----------------------------------------------------------------

(= (ga-evidence $ref $m)
   (match &self (in-referral $ref $e)
     (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
       (if (>= $ga 20)
         (evidence late-ga $e (from $e $site ga-weeks $ga) (stv 1.0 0.9))
         (empty)))))

(= (ga-preterm-evidence $ref $m)
   (match &self (in-referral $ref $e)
     (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
       (if (and (< $ga 37) (> $ga 0))
         (evidence preterm-ga $e (from $e $site ga-weeks $ga) (stv 1.0 0.9))
         (empty)))))

(= (postpartum-evidence $ref $m)
   (match &self (in-referral $ref $e)
     (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
       (if (== $ga 0)
         (evidence postpartum $e (from $e $site postpartum) (stv 1.0 0.9))
         (empty)))))

;; ----------------------------------------------------------------
;; Memory findings: search every encounter this agent remembers,
;; not only the referral window. This is what makes a normal BP at
;; 14 weeks change today's answer (ISSHP onset timing).
;; ----------------------------------------------------------------

;; early-normal-bp: BP below 140/90 recorded before 20 weeks.
(= (memory-early-normal $m)
   (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
     (if (< $ga 20)
       (match &self (reading $rs $e sbp $sbp)
         (match &self (reading $rd $e dbp $dbp)
           (if (and (< $sbp 140) (< $dbp 90))
             (if (== (is-contested $rs) no)
               (evidence early-normal-bp $rs (from $e $site ga-weeks $ga) (reading-truth $rs))
               (empty))
             (empty))))
       (empty))))

;; early-high-bp: BP at or above 140/90 recorded before 20 weeks (chronic).
(= (memory-early-high $m)
   (match &self (encounter $e $m (site $site) (by $by) (ga-weeks $ga) (at $at))
     (if (< $ga 20)
       (match &self (reading $rs $e sbp $sbp)
         (match &self (reading $rd $e dbp $dbp)
           (if (or (>= $sbp 140) (>= $dbp 90))
             (if (== (is-contested $rs) no)
               (evidence early-high-bp $rs (from $e $site ga-weeks $ga) (reading-truth $rs))
               (empty))
             (empty))))
       (empty))))

;; ----------------------------------------------------------------
;; One entry point: collect every evidence item for a referral.
;; ----------------------------------------------------------------

(= (collect-evidence $ref $m)
   (superpose (
     (reading-evidence $ref $m $f)
     (reading-counter $ref $m $f)
     (reading-evidence-low $ref $m $f)
     (sign-evidence $ref $m $f)
     (sign-counter $ref $m $f)
     (severe-symptom-evidence $ref $m)
     (danger-sign-evidence $ref $m)
     (htn-variant-evidence $ref $m)
     (htn-variant-counter $ref $m)
     (haemodynamic-evidence $ref $m)
     (haemodynamic-low-evidence $ref $m)
     (prom-evidence $ref $m)
     (ga-evidence $ref $m)
     (ga-preterm-evidence $ref $m)
     (postpartum-evidence $ref $m)
     (memory-early-normal $m)
     (memory-early-high $m)
   )))
