;; ---------------------------------------------------------------------------
;; File:   test17.lisp
;; Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
;; All rights reserved
;; ---------------------------------------------------------------------------
(setq start-value 5)

(defun factorial (n)
    (if n
        (* n (factorial (- n 1)))
        1))

(defun countdown (n)
    (while n
           (println n)
           (setq n (- n 1)))
    0)

(defun run ()
    (println "Countdown:")
    (countdown start-value)

    (println "Fakultaet:")
    (println (factorial start-value))

    0)

(start run)
