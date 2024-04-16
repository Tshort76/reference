(ns groceries-http-service.handler-v1
  (:require [compojure.core :refer :all]
            [compojure.route :as route]
            [clojure.data.json :as json]))


(def app-state (atom {}))


(defn add [item]
  (swap! app-state update item #(inc (or % 0)))
  (select-keys @app-state [item]))


(defn del [item]
  (let [state (swap! app-state update item #(dec (or % 1)))
        item-cnt (get state item)]
    (when (zero? item-cnt) (swap! app-state dissoc item))  ; clean up the list so that it doesn't have a bunch of 0 items
    {item item-cnt}))


(defn std-resp [{:strs [action parameters]}]
  {:status 200
   :body (json/write-str
          (case action
            "item.add" (add (get parameters "item"))
            "item.remove" (del (get parameters "item"))
            "item.list" @app-state
            {}))
   :headers {"Content-Type" "application/json"}})


(defroutes app-routes
  (POST "/" req (std-resp (get-in req [:body "result"])))
  (route/not-found "Not Found"))
