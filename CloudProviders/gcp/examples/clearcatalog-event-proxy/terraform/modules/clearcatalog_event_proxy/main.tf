locals {
  zipped_source_object = basename(var.local_source_path)
}

data "google_pubsub_topic" "trigger_topic" {
  name = var.trigger_topic
  project = var.catalog_gcp_project
}


resource "google_storage_bucket" "cloud_storage_artifact_bucket" {
  name = var.cloud_functions_artifact_bucket
  project = var.catalog_gcp_project
  location = var.cloud_storage_location
  uniform_bucket_level_access = true
}


resource "null_resource" "cloud_storage_bucket_with_object" {
  triggers = {
    latest_google_storage_object = local.zipped_source_object
  }

  provisioner "local-exec" {
    command = "gsutil cp ${var.local_source_path} gs://${var.cloud_functions_artifact_bucket}/${local.zipped_source_object}"
  }

  depends_on = [
    google_storage_bucket.cloud_storage_artifact_bucket
  ]
}

resource "google_service_account" "sa" {
  account_id = "clearcatalog-event-proxy"
  project = var.catalog_gcp_project
}

resource "google_pubsub_subscription" "dataset_updated_sub" {
  name = "clearcatalog-event-proxy-dataset-updated-sub"
  topic = data.google_pubsub_topic.trigger_topic.name
  ack_deadline_seconds = 30
  project = var.catalog_gcp_project
}

resource "google_pubsub_subscription_iam_member" "pubsub_subscriber" {
  role = "roles/pubsub.subscriber"
  member = "serviceAccount:${google_service_account.sa.email}"
  project = var.catalog_gcp_project
  subscription = google_pubsub_subscription.dataset_updated_sub.name
}

resource "google_cloudfunctions_function" "clearcatalog_event_proxy" {
  name = "clearcatalog_event_proxy"
  entry_point = "clearcatalog_event_proxy"
  description = "Cloud function that parses raw clearcatalog dataset changes and routes the messages to specific topics"
  project = var.catalog_gcp_project
  region = var.gcp_region
  runtime = "python38"
  available_memory_mb = 128
  source_archive_bucket = var.cloud_functions_artifact_bucket
  source_archive_object = local.zipped_source_object
  environment_variables = var.clearcatalog_event_proxy_environment_variables
  service_account_email = google_service_account.sa.email
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource = "projects/${var.catalog_gcp_project}/topics/${data.google_pubsub_topic.trigger_topic.name}"
  }
  depends_on = [
    null_resource.cloud_storage_bucket_with_object
  ]
}
