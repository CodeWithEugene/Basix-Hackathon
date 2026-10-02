;; Shims required only when running on hyperon (pip) instead of PeTTa.
;; lib_nal.metta calls min/max, which exist in PeTTa's stdlib but not in
;; hyperon's. On PeTTa these definitions are unused; harmless if loaded.
(= (min $a $b) (if (< $a $b) $a $b))
(= (max $a $b) (if (> $a $b) $a $b))
