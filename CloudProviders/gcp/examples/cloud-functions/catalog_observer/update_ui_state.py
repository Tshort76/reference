import logging
from operator import itemgetter
from catalog_observer.utils import CatalogUpdateEventType

import utils as u

log = logging.getLogger(__name__)


def err_file_display_name(orig_filename: str):
    return orig_filename.replace('.', '_') + "_schema_errors.json"


def update_ui_state(event: dict):

    event_payload = event['payload']
    upload_meta = u.get_in(event_payload, ['after', 'metadata', 'uploaded_object_metadata'])
    validation_meta = u.get_in(event_payload, ['after', 'storage_entry', 'data_validation'])

    org, file_id, filename, series, user_id = itemgetter('organization', 'file_id',
                                                         'filename', 'series', 'user_id')(upload_meta)

    firestore_path = "/".join(['dataopsui', org, 'users', user_id, 'uploads', file_id])

    firestore_data = {
        "status": validation_meta['status'],
        "dataset_id": series,
        "filename": filename,
        "file_id": file_id
    }

    if event['type'] == CatalogUpdateEventType.FILE_INVALID:
        firestore_data['bucket'] = validation_meta['report_bucket']
        blob_name = validation_meta['report_object']
        firestore_data['blob'] = blob_name[1:] if blob_name.startswith('/') else blob_name

    elif event['type'] == CatalogUpdateEventType.NEW_UPLOAD:
        firestore_data['created_by'] = upload_meta['user_email']

    log.info(f'Updating UI state for event of type {event["type"]}')
    wresult = u.write_to_firestore(firestore_data,
                                   firestore_path,
                                   update_record=False)

    return {"document_path": firestore_path,
            "result": wresult}
