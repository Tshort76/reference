variable "catalog_gcp_project" {
  type = string
}
variable "gcp_region" {
  type = string
}
variable "cloud_storage_location" {
  type = string
}
variable "cloud_functions_artifact_bucket" {
  type = string
}
variable "local_source_path" {
  type = string
}
variable "clearcatalog_event_proxy_environment_variables" {
  type = map(string)
}
variable "trigger_topic" {
  type = string
}

variable "data_ops_gcp_project" {
  type = string
}