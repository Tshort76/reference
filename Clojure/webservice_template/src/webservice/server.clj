(ns webservice.server
  (:require [ring.adapter.jetty :refer [run-jetty]]
            [webservice.handler :as h]
            [ring.middleware.json :refer [wrap-json-body]]
            [ring.middleware.defaults :refer [wrap-defaults site-defaults]])
  (:gen-class))


(def handler (-> h/app-routes
                 (wrap-defaults (assoc-in site-defaults [:security :anti-forgery] false))
                 wrap-json-body))


;; Start with:   clojure -M -m webservice.server
(defn -main [& args]
  (run-jetty handler {:port 3000 :join? false}))