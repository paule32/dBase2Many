;; ---------------------------------------------------------------------------
;; File:   test18.lisp
;; Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
;; All rights reserved
;; ---------------------------------------------------------------------------
(setq counter 5)

(while (> counter 0)
    (println counter)
    (setq counter (- counter 1)))
