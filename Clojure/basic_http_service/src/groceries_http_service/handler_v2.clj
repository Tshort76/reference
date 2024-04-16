(ns groceries-http-service.handler-v2
  (:require [compojure.core :refer :all]
            [compojure.route :as route]
            [clojure.data.json :as json]
            [taoensso.carmine :as car :refer (wcar)]))


(def redis-conn {:pool {} :spec {:host "127.0.0.1" :port 6379}})
(defmacro wcar* [& body] `(car/wcar redis-conn ~@body))


(defn add [item]
  {item (wcar* (car/incr item))})


(defn del [item]
  (let [cnt (wcar* (car/decr item))]
    (when (<= cnt 0) (wcar* (car/del item)))
    {item (max cnt 0)}))


(defn items-list []
  (let [keyz (second (wcar* (car/scan 0 :count 1000)))]
    (zipmap keyz (wcar* (apply car/mget keyz)))))


(defn std-resp [{:strs [action parameters]}]
  {:status 200
   :body (json/write-str
          (case action
            "item.add" (add (get parameters "item"))
            "item.remove" (del (get parameters "item"))
            "item.list" (items-list)
            {}))
   :headers {"Content-Type" "application/json"}})


(defroutes app-routes
  (POST "/" req (std-resp (get-in req [:body "result"])))
  (route/not-found "Not Found"))
