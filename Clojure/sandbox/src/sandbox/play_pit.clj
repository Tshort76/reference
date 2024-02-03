(ns sandbox.play-pit
  (:require [clojure.string :as cs]))

;; Given an unsorted integer array, find all pairs with the given sum in it.


(comment

  (let [my-promise (promise)
        mock-api-call (fn [x] (Thread/sleep 1000) x)]
    (doseq [score [15 10 18]]
      (future (when (> (mock-api-call score) 20)
                (deliver my-promise score))))
    (println "Ladies and Gentlemen, may I have your attention!")
    (println
     (if-let [r (deref my-promise 5000 nil)]
       (str "The winner is " r)
       "Nevermind, sorry for the interruption")))


  (defn long-process [] (Thread/sleep 5000) 5)
  (let [f (future (long-process))]
    (while (not (realized? f))
      (println "Sleeping")
      (Thread/sleep 1000))
    @f)




  (->> [8 7 2 5 3 1] sort)


  {:input '([8 7 2 5 3 1] 10)
   :out ['(8 2) '(7 3)]})

;;  ctrl + alt + .  :: slurp Forward