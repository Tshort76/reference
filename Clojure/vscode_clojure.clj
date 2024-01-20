;;;; namespaces
;; Load namespace and requirements - Ctrl+Alt+C Enter




;;;; Clojure Code Editing

;; Alt+Enter to evaluate the 'top level' form
;; Ctrl+Enter evaluates the 'current' form
;; Ctrl+Shift+Enter evaluates the enclosing form
;; EXPAND : Shift+Alt -> or <-
;; SLURP : Ctrl+Shift+Alt  -> or <-
  

  (def colt-express
    {:name "Colt Express"
     :categories ["Family"
                  "Strategy"]
     :play-time 40
     :ratings {:pez 5.0
               :kat 5.0
               :wiw 5.0
               :vig 3.0
               :rex 5.0
               :lun 4.0}})


    (defn average [coll]
      (/ (apply + coll) (count coll)))

;; To see the result at each step in the thread, use Ctrl+Alt+Enter after each form.
(->> colt-express
     :ratings
     vals
     average)



;; == The Calva Debugger ==   https://calva.io/debugger/
;; VSCode command: *Instrument Current Top Level Form for Debugging*
;; This will cause the debugger to stop at the first breakable point in the instrumented function
;; To un-instrument the function, just evaluate it the normal way (top level evaluation).
(defn bar
  [n]
  (cond (> n 40) (+ n 20)
        (> n 20) (- (first n) 20)
        :else 0))



(bar 2)  ; works
(bar 24) ; throws, what's going on?