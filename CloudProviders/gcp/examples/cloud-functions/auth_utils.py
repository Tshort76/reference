from google.oauth2 import service_account
import google.auth
from google.cloud import secretmanager
import json
from enum import Enum


class CredStoreFormat(Enum):
    GCP_SECRET_MANAGER = 1
    SA_KEY_FILE = 2
    DICT = 3


def get_secret(gcp_project: str, secret_id: str, version: str = 'latest'):  # ignore_in_test_coverage
    # Build the resource name of the secret version.
    sm_client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{gcp_project}/secrets/{secret_id}/versions/{version}"
    response = sm_client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return payload


def fetch_token(target_audience: str, gcp_project: str, creds_meta: dict):  # ignore_in_test_coverage

    creds_form = creds_meta['storage_format']

    if creds_form == CredStoreFormat.DICT:
        return creds_meta['token']

    if creds_form == CredStoreFormat.GCP_SECRET_MANAGER:
        info = json.loads(get_secret(gcp_project=gcp_project,
                                     secret_id=creds_meta['gcp_secret_name'],
                                     version='latest'))

        creds = service_account.IDTokenCredentials.from_service_account_info(info, target_audience=target_audience)
    elif creds_form == CredStoreFormat.SA_KEY_FILE:
        creds = service_account.IDTokenCredentials.from_service_account_file(creds_meta['srvc_acct_key_filepath'],
                                                                             target_audience=target_audience)
    else:
        raise LookupError("No GCP credentials found in the environment!")

    request = google.auth.transport.requests.Request()
    creds.refresh(request)
    return creds.token


def fetch_sa_creds(gcp_project: str, creds_meta: dict):  # ignore_in_test_coverage

    creds_form = creds_meta['storage_format']
    scopes = [u'https://www.googleapis.com/auth/devstorage.read_only']

    if creds_form == CredStoreFormat.GCP_SECRET_MANAGER:
        info = json.loads(get_secret(gcp_project=gcp_project,
                                     secret_id=creds_meta['gcp_secret_name'],
                                     version='latest'))

        creds = service_account.Credentials.from_service_account_info(info, scopes=scopes)
    elif creds_form == CredStoreFormat.SA_KEY_FILE:
        creds = service_account.Credentials.from_service_account_file(creds_meta['srvc_acct_key_filepath'],
                                                                      scopes=scopes)
    else:
        raise LookupError("No GCP credentials found in the environment!")

    request = google.auth.transport.requests.Request()
    creds.refresh(request)
    return creds
