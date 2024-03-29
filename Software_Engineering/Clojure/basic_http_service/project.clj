(defproject groceries-http-service "0.1.0-SNAPSHOT"
  :description "A sample HTTP service that stores a list of items."
  :url "http://example.com/FIXME"
  :min-lein-version "2.0.0"
  :dependencies [[org.clojure/clojure "1.10.0"]
                 [compojure "1.6.1"]
                 [ring/ring-defaults "0.3.2"]
                 [org.clojure/data.json "2.2.1"]
                 [ring/ring-json "0.5.1"]
                 [com.taoensso/carmine "3.1.0"]]
  :plugins [[lein-ring "0.12.5"]]
  :ring {:handler groceries-http-service.app/app}
  :profiles
  {:dev {:dependencies [[javax.servlet/servlet-api "2.5"]
                        [ring/ring-mock "0.3.2"]]}})
