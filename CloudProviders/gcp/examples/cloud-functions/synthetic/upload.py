import auth_utils as au
import json
import logging
import requests


def __upload(meta: dict, cfn_url: str, auth_token: str, file_data):
    auth_header = {"Authorization": f'Bearer {auth_token}'}
    json_header = {'content-type': 'application/json'}
    url_resp = requests.post(cfn_url, data=json.dumps(meta), headers={**auth_header, **json_header})

    if url_resp.status_code == 401:
        logging.warning(f'Unauthorized request for a clearfiles signed upload URL: {url_resp}')
        return url_resp, None

    instructions = url_resp.json()
    logging.debug(str(instructions))
    headers = instructions['required_headers']
    upload_resp = requests.put(instructions['signed_url'], data=json.dumps(file_data), headers=headers)
    return upload_resp, instructions['blob_name']


def upload_to_clearfiles(data, meta: dict, configs: dict):

    core_meta = {'organization_id': meta.get('org', 'test'),  # TODO change org
                 'user_id': 'test',
                 'identity_issuer': 'issuer_1',
                 'original_filename': meta['filename']}

    opt_meta = {}
    meta = {**core_meta, **opt_meta}

    upload_url = configs['CLEARFILES_UPLOAD_URL']
    creds_meta = {}
    if 'GCP_TOKEN' in configs:
        creds_meta['storage_format'] = au.CredStoreFormat.DICT
        creds_meta['token'] = configs['GCP_TOKEN']
        logging.debug('Authenticating to GCP with an explicit token, starting with ', configs['GCP_TOKEN'][0:4])
    elif 'SYNTHS_SRVC_ACCT_KEY_FILEPATH' in configs:
        creds_meta['storage_format'] = au.CredStoreFormat.SA_KEY_FILE
        kp = configs['SYNTHS_SRVC_ACCT_KEY_FILEPATH']
        creds_meta['srvc_acct_key_filepath'] = kp
        logging.debug('Authenticating to GCP with service account key file: ', kp)
    elif 'SYNTHS_GCP_SECRET_NAME' in configs:
        creds_meta['storage_format'] = au.CredStoreFormat.GCP_SECRET_MANAGER
        kp = configs['SYNTHS_GCP_SECRET_NAME']
        creds_meta['gcp_secret_name'] = kp
        logging.debug('Authenticating to GCP with creds stored in GCP Secret Manager, key: ', kp)

    return __upload(meta, upload_url, au.fetch_token(upload_url, configs['GCP_PROJECT'], creds_meta), data)
