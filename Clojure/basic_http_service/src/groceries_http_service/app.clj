(ns groceries-http-service.app
  (:require [groceries-http-service.handler-v0 :as v0]
            [groceries-http-service.handler-v1 :as v1]
            [groceries-http-service.handler-v2 :as v2]
            [ring.middleware.json :refer [wrap-json-body]]
            [ring.middleware.defaults :refer [wrap-defaults site-defaults]]))

(def app
  (-> v2/app-routes
      (wrap-defaults (assoc-in site-defaults [:security :anti-forgery] false))
      wrap-json-body))