;; ---------------------------------------------------------------------------
;; File:   test14.lisp
;; Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
;; All rights reserved
;; ---------------------------------------------------------------------------
(defun add (a b)
    (+ a b))

(defun run ()
    (println "LISP-Programm startet")
    (println (add 20 22)))

(start run)
