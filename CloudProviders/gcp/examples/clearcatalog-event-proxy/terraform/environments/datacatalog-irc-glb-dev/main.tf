module "clearcatalog_event_proxy" {
  source = "../../modules/clearcatalog_event_proxy/"
  catalog_gcp_project = var.catalog_gcp_project
  gcp_region = var.gcp_region
  cloud_storage_location = var.cloud_storage_location
  cloud_functions_artifact_bucket = var.cloud_functions_artifact_bucket
  local_source_path = var.local_source_path
  clearcatalog_event_proxy_environment_variables = merge(var.clearcatalog_event_proxy_environment_variables, {"GCP_PROJECT": var.data_ops_gcp_project})
  trigger_topic = var.trigger_topic
  data_ops_gcp_project = var.data_ops_gcp_project
}

provider "google" {
  credentials = var.gcp_auth_file
  impersonate_service_account = var.shared_vpc_service_account
  project = var.catalog_gcp_project
  region = var.gcp_region
}

provider "google-beta" {
  credentials = var.gcp_auth_file
  impersonate_service_account = var.shared_vpc_service_account
  project = var.catalog_gcp_project
  region = var.gcp_region
}

#######
# Backend
#######
terraform {
  backend "gcs" {
    bucket = "tf-state-daas-proven-burro-26ae"
    prefix = "terraform/clearcatalog_event_proxy/dev/clearcatalog_event_proxy"
  }
}

#######
# Variables
#######
variable "gcp_auth_file" {
  type = string
  default = null
}
variable "shared_vpc_service_account" {
  type = string
  default = null
}
variable "catalog_gcp_project" {
  type = string
  default = null
}

variable "data_ops_gcp_project" {
  type = string
  default = null
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