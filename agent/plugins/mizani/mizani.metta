;; ================================================================
;; Mizani as an Omega plugin.
;;
;; The same evidence/reason files load in the Mizani FastAPI host and as
;; a drop-in Omega plugin: after (loadOmegaPlugin), Omega's (getSkills)
;; lists the skills below and Omega's own `metta` skill can call them.
;; Requires Omega's lib_nal.metta and src/skills.metta loaded first.
;; ================================================================

;; assess: fire the active pack for a mother whose reconciled findings the
;; host has staged; returns the list of conclusion proof terms.
(= (assess $m)
   (collapse (fire-all $m)))

(= (loadOmegaPlugin)
   (progn
     (add-skill assess    "Decide referral for a mother from staged evidence; returns NAL proof terms" (mother))
     (add-skill fire-rule "Fire one rule by id for a mother; returns its NAL proof term" (mother rule_id))
     (add-skill why       "Explain which premises of a rule are present or missing" (mother rule_id))
     (add-skill update-rule "Replace a rule with a new version, returns old/new diff" (rule_id version body truth))
     ()))
