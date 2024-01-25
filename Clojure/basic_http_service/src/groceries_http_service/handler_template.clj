(ns groceries-http-service.handler-template
  (:require [compojure.core :refer [defroutes POST]]
            [compojure.route :as route]
            [clojure.data.json :as json]))

(def app-state (atom {}))

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
