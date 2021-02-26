import json
import logging
import utils as u
from catalog_observer.utils import CatalogUpdateEventType
from catalog_observer.update_ui_state import update_ui_state

log = logging.getLogger(__name__)


def publish_event_fn(topic: str):
    def publish_event(event):
        log.info(f'Forwarding an event of type {event["type"]} to topic {topic}')
        return u.publish_message(topic, event['raw_data'], event['attributes'])

    return publish_event


EVENT_HANDLERS = {
    CatalogUpdateEventType.FILE_INVALID: [
        publish_event_fn(CatalogUpdateEventType.FILE_INVALID.value),
        update_ui_state
    ],

    CatalogUpdateEventType.FILE_VALID: [
        publish_event_fn(CatalogUpdateEventType.FILE_VALID.value),
        update_ui_state
    ],

    CatalogUpdateEventType.NEW_UPLOAD: [
        publish_event_fn(CatalogUpdateEventType.NEW_UPLOAD.value),
        update_ui_state
    ],

    CatalogUpdateEventType.MERGED_INTO_DATASET: [
        publish_event_fn(CatalogUpdateEventType.MERGED_INTO_DATASET.value)
    ]
}


def catalog_update_type(evt_payload: dict) -> CatalogUpdateEventType:

    validation_state = u.get_in(evt_payload, ['after', 'storage_entry', 'data_validation', 'status'])
    storage_type = u.get_in(evt_payload, ['after', 'storage_entry', '_type'])
    event_type = None

    log.debug(f"Classifying catalog update event: {evt_payload}")

    if (not evt_payload.get('before')) and storage_type and storage_type.startswith('clearstorage.bucket.fileset'):
        event_type = CatalogUpdateEventType.NEW_UPLOAD
    elif (validation_state != 'PENDING' and
          u.get_in(evt_payload, ['before', 'storage_entry', 'data_validation', 'status']) == 'PENDING'):
        if validation_state == 'VALID':
            event_type = CatalogUpdateEventType.FILE_VALID
        elif validation_state == 'INVALID':
            event_type = CatalogUpdateEventType.FILE_INVALID

    return event_type


def catalog_update_dispatcher(event: dict):
    assert 'data' in event, 'Event missing message'

    payload = json.loads(u.decode_payload(event['data']))
    event_type = catalog_update_type(payload)

    print(f"Dispatching an update event of type: {event_type}")

    params = {
        'raw_data': u.decode_payload(event['data']),
        'attributes': event.get('attributes', {}),
        'type': event_type,
        'payload': payload
    }

    return [fnc(params) for fnc in EVENT_HANDLERS.get(event_type, [])]
