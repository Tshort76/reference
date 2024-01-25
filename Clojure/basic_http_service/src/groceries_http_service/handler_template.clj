(ns groceries-http-service.handler-v0
  (:require [compojure.core :refer :all]
            [compojure.route :as route]
            [clojure.data.json :as json]))

(defn std-resp [{:strs [action parameters]}]
  {:status 200
   :body (json/write-str
          (cond
            (= action "item.add") (let [itm (get parameters "item")]
                                    (swap! app-state conj itm)
                                    {"item" itm})
            (= action "item.remove") @app-state
            (= action "item.list") @app-state))
   :headers {"Content-Type" "application/json"}})


(defroutes app-routes
  (POST "/" req (std-resp (get-in req [:body "result"])))
  (route/not-found "Not Found"))
