(ns webservice.handler
  (:require [compojure.core :refer [routes GET]]
            [compojure.route :as cr]))

(def app-routes
  (routes
   (GET "/hello" [] "Hello World")
   (GET "/echo/:arg-str" [arg-str] arg-str)
   (cr/not-found "Not Found")))
