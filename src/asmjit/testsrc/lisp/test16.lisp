;; ---------------------------------------------------------------------------
;; File:   test16.lisp
;; Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
;; All rights reserved
;; ---------------------------------------------------------------------------
(setq global-value 100)

(defun increase (value)
    (+ value 10))

(defun run ()
    (println global-value)
    (println (increase global-value)))

(start run)
