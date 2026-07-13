;; ---------------------------------------------------------------------------
;; File:   test12.lisp
;; Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
;; All rights reserved
;; ---------------------------------------------------------------------------
(defun factorial (n)
    (if n
        (* n (factorial (- n 1)))
        1))

(println (factorial 5))
