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
Data types are immutable
### Hash Maps and Hash Sets
```clojure
;; Hash Map
{}  ; empty hash map
(hash-map :a 1 :b 2)  ; alt syntax
;; GET and GET-IN
(get <map> <key> <default>)
(get {:a 4 :b {:d 4 :f 5}} :h 0) ; -> 0
(get-in {:a 4 :b {:d 4 :f 5}} [:b :d])  ; -> 4
({:a 3 :b {:d 4 :f 5}} :a)  ; -> 3 ... map as a operator

;; Keywords
;; keywords lookup a key in a function ... useful for threading macros
(:a {:a 3 :b 4}) ; -> 3

;; Hash Sets
#{:a :b :c 4 6}  ; literal syntax
(hash-set 1 1 3 3)  ; -> #{1 3}  ; alt syntax
(set [1 1 3 3])  ; create set from seq
(conj #{:a :b} :c) ; -> #{:a :b :c}
(contains? #{:a :b} :c) ; -> False
(:a #{:a :b}) ; = (get #{:a :b} :a) -> :a
```

### Lists and Vectors
```clojure
;; Lists
;; implemented as linked lists with pointers, so sequential access
(list 1 "two" 3)
;; elements are added to the front of the list (note ' to escape)
(conj '(1 2 3) 0) ; -> (0 1 2 3)

;; Vectors
;; random (index based) access to sequences of data
(get [3 2 1] 0) ; -> 3
(conj [3 2 1] 0) ; -> [3 2 1 0]
```

### Strings
```clojure
"a str"  ; Must use Double Quotes

;; core functions
count || get || subs || compare

;; clojure.string functions
join || split || split-lines || replace || replace-first || reverse || index-of || last-index-of || capitalize || lower-case upper-case || trim || trim-newline || triml || trimr || blank? ||starts-with? || ends-with? || includes?

;; clojure.core functions for coercion
parse-boolean || parse-double || parse-long || parse-uuid

;; Regex
#"pattern" || re-find || re-seq || re-matches || re-pattern || re-matcher || re-groups
```


## Control Flow
```clojure
;; IF ... execute single forms conditionally
(if <condition> <when_true> <when_false=nil>)
(if (= x 3) "Arg was True" "Arg was False")

;; DO ... execute multiple forms, return last form's result
(do <form_1> ... <form_N>)

;; WHEN ... if + do , without an else branch
(when <condition> <form_1> ... <form_N>)

;; BOOLEAN expressions
; false and nil are falsey, everything else is truthy

;; OR ... returns first truthy value or last value
(or false nil :bob) ; -> :bob
(or false nil (= "yes" "no")) ; -> false

;; AND  ... returns first falsey value or last value
(and :john false :mom) ; -> false
(and :john :mom :dad) ; -> :dad

;; LET ... create scoped bindings and DO execution
(let [x (expensive_op 3)]
    (if (> x 3) x (+ x 3)))

;; LOOP ... RECUR
(loop [iteration 0]  ; ~let binding to init vals
  (println (str "Iteration " iteration))
  (if (> iteration 3)          ; check base case
    (println "Goodbye!")
    (recur (inc iteration))))  ; GOTO loop with new set of values


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

# Reference Sheet
## Predicates
zero? pos? neg? even? odd? number? rational? integer? ratio? decimal? float? double? int? nat-int? neg-int? pos-int? NaN? infinite?
## Random
rand rand-int
```