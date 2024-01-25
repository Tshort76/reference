(ns sandbox.goodreads
  (:require [clojure.string :as cs]
            [clojure.java.io :as jio]))


(defn- personal-note? [s]
  (not (or (cs/blank? s) (cs/includes? s "highlight | Location"))))


(defn parse-kindle-highlights [file]
  (let [filename (.getName file)]
    (->> file
         slurp
         cs/split-lines
         (filter personal-note?)
         (reduce (fn [state line]
                   (if (cs/starts-with? line "Note:")
                  ;;  {:highlight X :note Y} 
                  ;;  (conj (pop state) (assoc (peek state) :note (subs line 5)))
                  ;;  (conj state {:highlight line})
                  ;;  (conj (pop state) (vector (peek state) (subs line 5)))
                     (conj (pop state) (str (peek state) "\n\t" (subs line 5)))
                     (conj state line)))
                 [])
         (cs/join "\n\n")
         (spit (str (subs filename 0 (- (count filename) (count "_highlights.txt"))) "_parsed.txt")))))


(comment

  (->> "resources"
       jio/file
       file-seq
       (filter (comp #(cs/ends-with? % "highlights.txt")))
       (map parse-kindle-highlights))

  (parse-kindle-highlights "restless_republic_highlights.txt"))