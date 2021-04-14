import logging
from operator import itemgetter

from toolz import get_in

import clearcatalog_event_proxy.utils as u

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def err_file_display_name(orig_filename: str):
    return orig_filename.replace('.', '_') + "_schema_errors.json"


def update_ui_state(event: dict):

    event_payload = event['payload']
    upload_meta = get_in(['after', 'metadata', 'uploadedObjectMetadata'], event_payload)
    validation_meta = get_in(['after', 'storageEntry', 'dataValidation'], event_payload)
    status = validation_meta['status'] if validation_meta else get_in(['after', 'storageEntry', 'status'],
                                                                      event_payload)

    org, file_id, filename, series, user_id = itemgetter('organization', 'fileid',
                                                         'filename', 'series', 'userid')(upload_meta)

    firestore_path = "/".join(['dataopsui', org, 'users', user_id, 'uploads', file_id])

    firestore_data = {
        "status": status,
        "datasetId": series,
        "filename": filename,
        "fileId": file_id
    }

    if event['type'] == u.CatalogUpdateEventType.FILE_INVALID:
        firestore_data['bucket'] = validation_meta['reportBucket']
        blob_name = validation_meta['reportObject']
        firestore_data['blob'] = blob_name[1:] if blob_name.startswith('/') else blob_name

    elif event['type'] == u.CatalogUpdateEventType.NEW_UPLOAD:
        firestore_data['username'] = upload_meta['username']

    elif event['type'] == u.CatalogUpdateEventType.DATASET_META_ADDED:
        num_rows = get_in(['after', 'metadata', 'recordCount'], event_payload)
        if num_rows:
            firestore_data['recordCount'] = num_rows

    log.info(f'Updating UI state for event of type {event["type"]}')
    wresult = u.write_to_firestore(firestore_data, firestore_path)

    return {"documentPath": firestore_path,
            "result": wresult}
