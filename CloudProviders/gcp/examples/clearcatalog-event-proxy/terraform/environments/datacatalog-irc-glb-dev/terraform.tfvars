data_ops_gcp_project = "proven-burro-26ae"
catalog_gcp_project = "clean-poodle-2be2"
gcp_region = "us-west2"
trigger_topic = "clear-catalog-dataset-update"

cloud_storage_location = "US"
cloud_functions_artifact_bucket = "tf-artifacts-clean-poodle-2be2-clearcatalog-event-proxy"
clearcatalog_event_proxy_environment_variables = {
  LOGGING_LEVEL_ROOT = "ERROR"
  LOGGING_LEVEL_COM_CLEARWATERANALYTICS = "DEBUG"
}
