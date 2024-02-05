- [Fundamentals](#fundamentals)
  - [Basic Concepts](#basic-concepts)
  - [Basic Syntax](#basic-syntax)
  - [Data Structures](#data-structures)
    - [Hash Maps and Hash Sets](#hash-maps-and-hash-sets)
    - [Lists and Vectors](#lists-and-vectors)
  - [Control Flow](#control-flow)
    - [Threading](#threading)
    - [Predicates](#predicates)
  - [Bindings](#bindings)
  - [Functions](#functions)
    - [Arity overloading](#arity-overloading)
    - [Anonymous Functions](#anonymous-functions)
  - [Destructuring](#destructuring)
    - [Sequences](#sequences)
    - [Hash Maps](#hash-maps)
- [Core Functions](#core-functions)
  - [Sequences](#sequences-1)
    - [Entire Sequence](#entire-sequence)
    - [Individual Elements](#individual-elements)
  - [Functions](#functions-1)
  - [Strings](#strings)
    - [Regex](#regex)
- [Project Infrastructure](#project-infrastructure)
  - [Deps.edn](#depsedn)
  - [Namespaces](#namespaces)
  - [Directory Layout](#directory-layout)
- [Design Patterns](#design-patterns)
  - [Concurrency](#concurrency)
    - [Futures](#futures)
    - [Delays](#delays)
    - [Promises](#promises)
  - [Atoms](#atoms)
  - [Polymorphism](#polymorphism)
    - [Multimethods](#multimethods)
    - [Protocols](#protocols)
- [References and Sources](#references-and-sources)

# Fundamentals
## Basic Concepts
Clojure provides immutable data structures, first-class functions, and a few reusable functions that can be combined to do useful things.
## Basic Syntax
```clojure
(operator operand_1 ... operand_N)
(def <name> <value>)  ; bind a value to a name
"a string" ; must use double quotes for strings 'not a string'
```
## Data Structures
### Hash Maps and Hash Sets
```clojure
;;;;  Hash Map
{}  ; empty hash map
(hash-map :a 1 :b 2)  ; alt syntax
;; GET and GET-IN
(get <map> <key> <default>)
(get {:a 4 :b {:d 4 :f 5}} :h 0) ; -> 0
(get-in {:a 4 :b {:d 4 :f 5}} [:b :d])  ; -> 4
({:a 3 :b {:d 4 :f 5}} :a)  ; -> 3 ... map as a operator

;; Core functions
contains? || keys || vals || assoc || assoc-in || dissoc || merge || merge-with || update || update-in

;;;;  Keywords
;; keywords lookup a key in a function ... useful for threading macros
(:a {:a 3 :b 4}) ; -> 3

;;;;  Hash Sets
#{:a :b :c 4 6}  ; literal syntax
(hash-set 1 1 3 3)  ; -> #{1 3}  ; alt syntax
(set [1 1 3 3])  ; create set from seq
(conj #{:a :b} :c) ; -> #{:a :b :c}
(contains? #{:a :b} :c) ; -> False
(:a #{:a :b}) ; = (get #{:a :b} :a) -> :a
```

### Lists and Vectors
```clojure
;;;;  Lists
;; implemented as linked lists with pointers, so sequential access
(list 1 "two" 3)
;; elements are added to the front of the list (note ' to escape)
(conj '(1 2 3) 0) ; -> (0 1 2 3)

;;;;  Vectors
;; random (index based) access to sequences of data
(get [3 2 1] 0) ; -> 3
(conj [3 2 1] 0) ; -> [3 2 1 0]

;;;;  Strings
"a str"
(str 2) ; -> "2"
```

## Control Flow
```clojure
;;;;  IF ... execute single forms conditionally
(if <condition> <when_true> <when_false=nil>)
(if (= x 3) "Arg was True" "Arg was False")

;;;;  DO ... execute multiple forms, return last form's result
(do <form_1> ... <form_N>)

;;;;  WHEN ... if + do , without an else branch
(when <condition> <form_1> ... <form_N>)

;;;; COND ... match/switch statement
(cond
  (< n 0) "negative"
  (> n 0) "positive"
  :else "zero")

;;;; CASE ... cond but with a single multi-valued predicate
(case mystr
  "" 0
  "hello" (count mystr)
  "default")

;;;;  LOOP ... RECUR
(loop [iteration 0]  ; ~let binding to init vals
  (println (str "Iteration " iteration))
  (if (> iteration 3)          ; check base case
    (println "Goodbye!")
    (recur (inc iteration))))  ; GOTO loop with new set of values

;;;;  REDUCE
;; iteratively apply a function to items from a seq to build up a value
(reduce (fn [state [key val]]
  (assoc state key (inc val)))
  {}  ; initial value for state ... optional
  {:max 100 :min 0})  ; sequence on which to operate
  ; -> {:max 101 :min 1}
```

### Threading
```clojure
;;;; Thread Last ... pass result from form_x as LAST argument to form_(x+1)
(->> [1 2 3] (map inc) (reduce +))  ; -> 9

;;;; Thread First ... pass result from form_x as FIRST argument to form_(x+1)
(-> inc (map [1 2 3]) first)  ; -> 2 ... bad example

;;;;  AS threading ... arbitrary positioning of your argument
(as-> {:a 1 :b 2} m   ; initialize value
  (update m :a + 10)
  (reduce (fn [s [_ v]] (+ s v)) 0 m))


;;;; Conditional threading

;; cond-> | cond->>
(defn divisible-by? [d n] (zero? (mod n d)))
; thread into forms where predicate evaluates to true
(defn fizz-buzz-mini [n]
     (cond-> nil
       (divisible-by? 3 n) (str "Fizz")
       (divisible-by? 5 n) (str "Buzz")
       :always             (or (str n))))

;;  some-> | some->>  ... threads as long as the value isn't nil
(some->> 
  [1 2 3 4]
  (filter #(= 0 (mod % 2)))
  seq  ; basically, use seq to get an empty collection to eval to Falsey
  first)

```

### Predicates
False and nil are falset, everything else (including empty sequences) is truthy
```clojure
;;;; OR ... returns first truthy value or last value
(or false nil :bob) ; -> :bob
(or false nil (= "yes" "no")) ; -> false

;;;;  AND  ... returns first falsey value or last value
(and :john false :mom) ; -> false
(and :john :mom :dad) ; -> :dad
```

## Bindings
```clojure
let fn defn defmacro loop for doseq if-let when-let
if-some when-some

;;;;  LET ... create scoped bindings and DO execution
(let [x (expensive_op 3)]
    (if (> x 3) x (+ x 3)))

(if-let [x (seq (expensive_op 5))]  ; bind a value and conditionally act on it
  (run_an_op_when_truthy x)
  (else_clause_op)
)

(when-let [x (seq (expensive_op 5))]  ; bind a value and operate if truthy ... := in python
  (first_op x)
  (second_op x)
)


;;;;  FOR 
;; prepare a seq of the even values from the first six multiples of three
(for [x [0 1 2 3 4 5]
      :let [y (* x 3)]
      :when (even? y)]
  y)  ; -> (0 6 12)

```

## Functions
```clojure
(defn <function_name>
  "Docstring"
  [param_1 ... param_N]
  <function body ~= do>)
```

### Arity overloading
- Clojure automatically returns the last form evaluated

```clojure
;; multi-arity function definition
(defn add-up
"Add two values"
([op1 op2]  ; double arity
    (+ op1 op2))
([op1]  ; single arity
    (add-up op1 0)))  ; call function with default argument

;; variable arity function definition
(defn greeter
 [name & activities]
    (str "Hi " name ", you are so good at" (clojure.string/join ", " attributes)))
```

### Anonymous Functions
```clojure
;; form 1
(fn [param-list] <function_body>)

;; form 2
#(+ % 1)  ; inc
#(+ %1 %2) ; add with 2 args
(#(str %1 " & " %2) "PB" "J")  ; PB & J
```

## Destructuring
### Sequences
```clojure
(def my-vector [:a :b :c :d])

(let [[a b] my-vector]  ; no need to bind all elements
  (println a b))  ; => :a :b

;; & to bind remaining
(let [[a b & the-rest] my-vector]
  (println a b the-rest))  ; => :a :b (:c :d)

;; Use :as to bind full argument
(let [[a :as all] my-vector]
  (println a all))  ; => :a [:a :b :c :d]

;; Nested vectors and ignoring
(let [[a _ [x y]] [:a :b [:x :y]]]
  (println a x y))  ; -> :a :x :y
```
### Hash Maps
```clojure
(def my-hashmap {:a "A" :b "B" :c "C"})

(let [{a :a} my-hashmap]
  (println a))  ; -> A

;; use :keys as shorthand for {a :a b :b}
(let [{:keys [a b], :as all} my-hashmap]
  (println a b all))  ; => A B {:a A :b B :c C}

;; provide a default mapping with :or clause
(let [{:keys [a b d], :or {d "XXX"}} my-hashmap]
  (println a b d))  ; => A B XXX

;; use :strs inplace of :keys when map keys are strings
(let [{:strs [a]} {"a" "A", "b" "B"}]
  (println a))  ; => A
```

# Core Functions
## Sequences
### Entire Sequence
```clojure
;;;;  MAP and variants
;; apply func to members of a collection or simultaneously to members from a group of collections
(map inc [1 2 3]) ; -> (2 3 4)
(map + [1 2 3] [4 5 6 7]) ; -> (5 7 9) ... stops with shortest list
(mapcat (partial repeat 2) [1 2 3]) ; -> (1 1 2 2 3 3)
(mapv inc [1 2 3]) ; -> [1 2 3]  ; vector

;;;;  TAKE variants
(first [1 2 3]) ; -> 1
(rest [1 2 3]) ; -> (2 3)
(take 2 [1 2 3 4])  ; -> (1 2)  ; take first N items
(drop 2 [1 2 3 4])  ; -> (3 4)  ; drop N items, take rest
(take-while #(< % 5) [1 2 3 4 5 6])  ; -> (1 2 3 4)
(drop-while #(< % 5) [1 2 3 4 5 6])  ; -> (5 6)

;;;;  FILTER and REMOVE
;; return all elements which satisfy a predicate
(filter #(< % 5) [1 2 6 14 4 9])  ; -> (1 2 4)
(remove #(< % 5) [1 2 6 14 4 9])  ; -> (6 14 9) ; complement of filter

;;;;  SOME
;; Return the first item that satisfies the predicate
(some #(> % 6) [1 2 5 5 5 9 3]) ; -> 9

;;;;  SORT
(sort-by count ["aaa" "c" "bb"])  ; => ("c" "bb" "aaa")
(sort-by count ["aaa" "c" "bb"])  ; => ("c" "bb" "aaa")

;;;;  CONCAT
(concat [1 2] [3 4])  ; -> (1 2 3 4)

;;;;  CONJ
(conj [1 2 3] 4)  ; [1 2 3 4]

distinct || flatten || group-by || partition || partition-all || partition-by
split-at || split-with || filter || remove || replace ||
```
### Individual Elements
```clojure
(get-in)
```


## Functions
```clojure
;;;;  COMP ... compose functions into one (last fnc applied first)
(map (comp inc :count) [{:count 0 :name "bob"}, {:count 2 :name "jon"}])

;;;;  APPLY ... explode arguments for arity arguments
(apply max [1 2 3 4 5])

;;;;  MEMOIZE
(def memo-sleepy-identity (memoize sleepy-identity))

;;;;  MISC
identity || constantly || memfn || complement || partial
juxt || every-pred || some-fn

```

## Strings
```clojure
;;;;  core functions
count || get || subs || compare

;;;;  clojure.string functions
join || split || split-lines || replace || replace-first || reverse || index-of || last-index-of || capitalize || lower-case upper-case || trim || trim-newline || triml || trimr || blank? ||starts-with? || ends-with? || includes?

;;;;  clojure.core functions for coercion
parse-boolean || parse-double || parse-long || parse-uuid
```
### Regex
```clojure
#"pattern" || re-find || re-seq || re-matches || re-pattern || re-matcher || re-groups
```

# Project Infrastructure
## Deps.edn
```clojure
{:paths ["src" "resources"]
 :deps {org.clojure/clojure {:mvn/version "1.9.0"}
        ...
        prismatic/plumbing {:mvn/version "0.5.5"}
        environ/environ {:mvn/version "1.2.0"}
        com.taoensso/timbre {:mvn/version "4.10.0"}}
 :aliases
 {:test {:extra-paths ["test"]
         :extra-deps {org.clojure/test.check {:mvn/version "1.0.0"}}}}}
```

## Namespaces
```clojure
(ns sandbox.app
  (:require [clojure.string :as cs]  ; import _ as cs
            [ring.middleware.json :refer [wrap-json-body]]  ; from _ import wrap-json-body
            [compojure.core :refer :all])  ; from _ import *
  (:import (java.io File))   ; import java classes
)

*ns*   ; current namespace
ns-name || ns-aliases || ns-map || ns-interns || ns-publics || ns-refers

```

## Directory Layout
```
.gitignore
deps.edn or project.clj (lein)
README.md
resources
src
  my_package  ;; underscore in directory name, hyphen in namespace
    core.clj  ;; (ns my-package.core)
test
  my_package
    core_test.clj  ;; same name as src package + "_test"
```

# Design Patterns
When you write serial code, you bind together these three events:
- Task definition
- Task execution
- Blocking for the task’s result
## Concurrency
### Futures
Futures are used to **define a task** and place it on another thread without requiring the result immediately.  Requesting a future's result is called dereferencing the future, and you do it with either the `deref` function or the `@` reader macro.  The result of a future is cached, so dereferencing it multiple times does not affect performance.  If you attempt to dereference a future before the task has completed, the thread will block.

```clojure

; return the value 5 if the future doesn’t return within 10 milliseconds
(deref (future (Thread/sleep 1000) 0) 10 5)

(defn long-process [] (Thread/sleep 5000) 5)
(let [f (future (long-process))]
    (while (not (realized? f))  ; use realized? to check if result is ready
      (println "Sleeping")
      (Thread/sleep 1000))
    @f)
```

### Delays
Delays allow you to define a task without having to execute it or require the 
result immediately

### Promises
Promises allow you to express that you expect a result without having to define the task that should produce it or when that task should run. You create promises using `promise`, deliver/assign an expression to them using `deliver`, and then access the value by deferencing.  This can be used to implement a paradigm similar to passing an empty pointer (to pre-allocated space) as a function parameter and expecting the function to produce the side-effect of updating the data at the pointer's referenced address.

```clojure
(def my-promise (promise))
(deliver my-promise (+ 3 5))
@my-promise ; -> 8

; run tasks in parallel, require 1 second of human time (assuming > 3 cores)
(let [my-promise (promise)
        mock-api-call (fn [x] (Thread/sleep 1000) x)]
    (doseq [score [15 10 25]]
      (future (when (> (mock-api-call score) 20)
                (deliver my-promise score))))
    (println "Ladies and Gentlemen, may I have your attention!")
    (println "The winner is:" (deref my-promise 5000 "timed out"))) ;handle case where no value is found
```



## Atoms
## Polymorphism
### Multimethods
```clojure
(defmulti my-multi-fnc dispatcher-fn)  ; (defmulti add :type)
(defmethod my-multi-fnc dispatcher-output-val [params] <fnc_body>)
```

### Protocols
Multimethod with dispatch based on the **first argument's Type**
```clojure
;;;; Define
(defprotocol Psychodynamics
  "Doc string for your protocol"
  (thoughts [x] "thoughts doc string")  ; method signatures
  (feelings [x] [x y] "feelings doc string"))  ; method signature

;;;; Extend
(extend-type java.lang.String Psychodynamics
  (thoughts [x] (str x " thinks, 'Truly, the character defines the data type'")
  (feelings 
    ([x] (str x " is longing for a simpler way of life"))
    ([x y] (str x " is envious of " y "'s simpler way of life")))))

(extend-type java.lang.Object Psychodynamics
(thoughts [x] "Maybe the Internet is just a vector for toxoplasmosis")
(feelings
  ([x] "meh")
  ([x y] (str "meh about " y))))


```
# References and Sources
- https://www.braveclojure.com/clojure-for-the-brave-and-true/ 
- https://clojure.org/api/cheatsheet 
- https://clojure.org/guides/deps_and_cli
- https://clojuredocs.org/