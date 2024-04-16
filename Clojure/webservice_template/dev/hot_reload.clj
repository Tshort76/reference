(ns hot-reload
  (:require [ring.adapter.jetty :refer [run-jetty]]
            [ring.middleware.reload :refer [wrap-reload]]
            [webservice.server :refer [handler]])
  (:gen-class))


(def dev-handler
  (wrap-reload #'handler))

; Start the server with:   clojure -M:dev
(defn -main [& args]
  (run-jetty dev-handler {:port 13000}))