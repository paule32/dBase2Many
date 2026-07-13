;; ---------------------------------------------------------------------------
;; File:   test13.lisp
;; Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
;; All rights reserved
;; ---------------------------------------------------------------------------
(defun fibonacci (n)
    (if n
        (if (- n 1)
            (+ (fibonacci (- n 1))
               (fibonacci (- n 2)))
            1)
        0))

(println (fibonacci 10))
