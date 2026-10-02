;; ================================================================
;; Mizani shims: small helpers shared by the evidence and reason layers.
;; Omega's lib_nal.metta must be loaded before this file.
;; ================================================================

;; min/max exist in PeTTa's stdlib (lib_nal.metta uses them); these
;; definitions are only a safety net for runtimes that lack them.
(= (mizani-min $a $b) (if (< $a $b) $a $b))
(= (mizani-max $a $b) (if (> $a $b) $a $b))

;; Empty-collapsed-match test: true when no atom matches $pattern via $pred
;; Usage style: (no-match (contested $id $b $r) $id)
(= (none ($query)) (== (collapse $query) ()))
