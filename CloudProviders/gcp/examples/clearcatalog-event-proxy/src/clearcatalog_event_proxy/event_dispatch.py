import json
import logging
from toolz import get_in

from google.cloud import pubsub_v1

import clearcatalog_event_proxy.utils as u
from clearcatalog_event_proxy.update_ui_state import update_ui_state

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def assert_properly_configured():  # ignore_in_test_coverage
    publisher = pubsub_v1.PublisherClient()

    for topic in u.CatalogUpdateEventType:
        if not topic.value.startswith("None"):
            topic_path = publisher.topic_path(u.GCP_PROJECT_ID, topic.value)
            publisher.get_topic({"topic": topic_path})


def publish_event_fn(topic: str):
    def publish_event(event):
        log.info(f'Forwarding an event of type {event["type"]} to topic {topic}')
        return u.publish_message(topic, event['raw_data'], event['attributes'])

    return publish_event


EVENT_HANDLERS = {
    u.CatalogUpdateEventType.FILE_INVALID: [
        publish_event_fn(u.CatalogUpdateEventType.FILE_INVALID.value),
        update_ui_state
    ],

    u.CatalogUpdateEventType.FILE_VALID: [
        publish_event_fn(u.CatalogUpdateEventType.FILE_VALID.value),
        update_ui_state
    ],

    u.CatalogUpdateEventType.NEW_UPLOAD: [
        publish_event_fn(u.CatalogUpdateEventType.NEW_UPLOAD.value),
        update_ui_state
    ],

    u.CatalogUpdateEventType.DATASET_APPENDED: [
        publish_event_fn(u.CatalogUpdateEventType.DATASET_APPENDED.value)
    ],

    u.CatalogUpdateEventType.DATASET_META_ADDED: [
        update_ui_state
    ]
}


def catalog_update_type(evt_payload: dict) -> u.CatalogUpdateEventType:

    validation_state = get_in(['after', 'storageEntry', 'dataValidation', 'status'], evt_payload)
    storage_type = get_in(['after', 'storageEntry', 'type'], evt_payload)
    event_type = None

    log.debug(f"Classifying catalog update event: {evt_payload}")

    if (not evt_payload.get('before')) and storage_type and storage_type.startswith('clearstorage.bucket.fileset'):
        event_type = u.CatalogUpdateEventType.NEW_UPLOAD
    elif (validation_state != 'PENDING' and
          get_in(['before', 'storageEntry', 'dataValidation', 'status'], evt_payload) == 'PENDING'):

        if validation_state == 'VALID':
            event_type = u.CatalogUpdateEventType.FILE_VALID
        elif validation_state == 'INVALID':
            event_type = u.CatalogUpdateEventType.FILE_INVALID

    elif (storage_type and storage_type.startswith('clearstorage.bigquery.table')
          and get_in(['after', 'storageEntry', 'status'], evt_payload) == 'COMPLETE'):

        if get_in(['before', 'storageEntry', 'status'], evt_payload) == 'PENDING':
            event_type = u.CatalogUpdateEventType.DATASET_APPENDED
        elif (not get_in(['before', 'metadata', 'recordCount'], evt_payload)
              and get_in(['after', 'metadata', 'recordCount'], evt_payload)):
            event_type = u.CatalogUpdateEventType.DATASET_META_ADDED

    return event_type


def catalog_update_dispatcher(event: dict):
    assert 'data' in event, 'Event missing message'

    payload = json.loads(u.decode_payload(event['data']))
    event_type = catalog_update_type(payload)

    log.info(f"Dispatching an update event of type: {event_type}")

    params = {
        'raw_data': u.decode_payload(event['data']),
        'attributes': event.get('attributes', {}),
        'type': event_type,
        'payload': payload
    }

    return [fnc(params) for fnc in EVENT_HANDLERS.get(event_type, [])]
