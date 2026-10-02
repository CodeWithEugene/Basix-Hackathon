;; ================================================================
;; Mizani reason layer.
;;
;; Fires the active rule pack as NAL deduction chains through Omega's
;; own lib_nal.metta (|-nal), producing proof terms with truth values.
;; Derives cross-visit findings (new-onset hypertension) from reconciled
;; evidence and the agent's memory of the mother.
;;
;; The host (Python) stages ephemeral atoms before firing:
;;   (reconciled <mother> <finding> (stv f c))   revised truth per finding
;;   (evidence-mem <finding> <src> <from> <tv>)  memory evidence for onset
;; These are cleared with (clear-ephemeral) between runs and are never
;; written to the persistent memory log.
;; ================================================================

;; ----------------------------------------------------------------
;; Ephemeral staging
;; ----------------------------------------------------------------

(= (clear-ephemeral)
   (progn
     (collapse (match &self (reconciled $m $f $tv) (remove-atom &self (reconciled $m $f $tv))))
     (collapse (match &self (evidence-mem $a $b $c $d) (remove-atom &self (evidence-mem $a $b $c $d))))
     ()))

;; The revised truth the host computed for finding $f of mother $m
;; (revision itself is folded by the host through |-nal calls).
(= (finding-truth $m $f)
   (match &self (reconciled $m $f $tv) $tv))

;; ----------------------------------------------------------------
;; Rule firing as NAL deduction chains
;;
;; A rule atom is (rule <pack> <id> <version> (==> <antecedent> <conc>) <stv>).
;; The antecedent is a finding symbol or a nested conjunction
;; (∧ a (∧ b c)). Each elimination step is one |-nal deduction:
;;   premise, (==> (∧ premise rest) conc)  |-  (==> rest conc)
;;   premise, (==> premise conc)          |-  conc
;; ----------------------------------------------------------------

(= (eliminate $m (==> (∧ $p $rest) $c) $tv $n)
   (let* (($ptv (finding-truth $m $p))
          (((==> $rest $c) $tv2) (|-nal ($p $ptv) ((==> (∧ $p $rest) $c) $tv)))
          (($fc $ftv $tail) (eliminate $m (==> $rest $c) $tv2 (+ $n 1))))
     ($fc $ftv (step $n (premise $p $ptv) (derived (==> $rest $c) $tv2) $tail))))

(= (eliminate $m (==> $p $c) $tv $n)
   (let* (($ptv (finding-truth $m $p))
          (($c $tv2) (|-nal ($p $ptv) ((==> $p $c) $tv))))
     ($c $tv2 (step $n (premise $p $ptv) (derived $c $tv2) (done)))))

;; Fire one rule by id. Returns a proof term or nothing.
(= (fire-rule $m $id)
   (match &self (rule $pack $id $ver (==> $ante $conc) $rtv)
     (let ($fc $ftv $steps) (eliminate $m (==> $ante $conc) $rtv 1)
       (conclusion $fc $ftv (because (rule $pack $id $ver) $steps)))))

;; Fire every rule of the active pack. Packs assert (active-pack <pack>).
(= (fire-all $m)
   (match &self (active-pack $pack)
     (match &self (rule $pack $id $ver $body $rtv)
       (fire-rule $m $id))))

;; ----------------------------------------------------------------
;; Why / why-not: which premises of a rule are present, missing, or weak
;; ----------------------------------------------------------------

(= (presence $m $f)
   (if (== (collapse (match &self (reconciled $m $f $tv) $tv)) ()) missing present))

;; Structural guard: succeeds when $x is a conjunction.
(= (is-conj $x)
   (if (== (collapse (let (∧ $a $b) $x ok)) ()) no yes))

(= (checks $m (∧ $a $b))
   (check $a (presence $m $a) (checks $m $b)))
(= (checks $m $a)
   (if (== (is-conj $a) no)
     (check $a (presence $m $a) (done))
     (empty)))

(= (why $m $id)
   (match &self (rule $pack $id $ver (==> $ante $conc) $rtv)
     (rule-status $pack $id $ver $conc (checks $m $ante))))

;; ----------------------------------------------------------------
;; Cross-visit derivations (ISSHP onset timing)
;;
;; new-onset: hypertension holds now (reconciled htn in Omega's act band),
;; the mother is at or past 20 weeks, and memory holds a normal BP from
;; before 20 weeks. This is what turns today's high BP into pre-eclampsia
;; territory instead of chronic hypertension.
;; ----------------------------------------------------------------

(= (derive-findings $ref $m)
   (superpose (
     (onset-derivation $ref $m)
     (chronic-derivation $ref $m)
   )))

(= (onset-derivation $ref $m)
   (match &self (reconciled $m htn (stv $fh $ch))
     (if (and (>= $fh 0.6) (>= $ch 0.5))
       (match &self (reconciled $m late-ga $tg)
         (match &self (evidence-mem early-normal-bp $src $from $tv)
           (evidence new-onset $src (derived-from memory $from) (stv 1.0 0.9))))
       (empty))))

(= (chronic-derivation $ref $m)
   (match &self (reconciled $m htn (stv $fh $ch))
     (if (and (>= $fh 0.6) (>= $ch 0.5))
       (match &self (evidence-mem early-high-bp $src $from $tv)
         (evidence chronic-htn $src (derived-from memory $from) (stv 1.0 0.9)))
       (empty))))

;; ----------------------------------------------------------------
;; Governed self-modification: replace a rule atom, return the diff.
;; The host logs both the remove and the add to the memory event log,
;; so every rule change is auditable and replayable.
;; ----------------------------------------------------------------

(= (update-rule $id $newver $newbody $newtv)
   (match &self (rule $p $id $ver $body $tv)
     (let $_ (remove-atom &self (rule $p $id $ver $body $tv))
       (let $_2 (add-atom &self (rule $p $id $newver $newbody $newtv))
         (rule-diff (old (rule $p $id $ver $body $tv))
                    (new (rule $p $id $newver $newbody $newtv)))))))
