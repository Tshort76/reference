import base64
import datetime as dt
from google.cloud import firestore
from google.cloud import pubsub_v1
import logging
import os
from enum import Enum


class CatalogUpdateEventType(Enum):
    FILE_INVALID = 'clearcatalog_dataset_updated_fanout_validation_failed'
    NEW_UPLOAD = 'clearcatalog_dataset_updated_fanout_new_file'
    FILE_VALID = 'clearcatalog_dataset_updated_fanout_validation_success'
    DATASET_APPENDED = 'clearcatalog_dataset_updated_fanout_uploaded_to_big_query'
    DATASET_META_ADDED = 'None_0'


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

GCP_PROJECT_ID = os.getenv('GCP_PROJECT', "daas-sandbox-pwasden")


def decode_payload(b_str: bytes) -> str:
    """Decodes a base64 encoded, utf-8 encoded byte string

    Args:
        b_str (bytes): A base64 encoding of a utf-8 encoded byte string

    Returns:
        str: The decoded string
    """

    b_str = b_str.encode("utf-8") if type(b_str) == str else b_str
    missing_padding = len(b_str) % 4
    if missing_padding:
        b_str += b'=' * (4 - missing_padding)
    return base64.b64decode(b_str).decode("utf-8")


def encode_payload(payload: str) -> bytes:
    "Ensures consistent encoding and therefore simple decoding"
    return payload.encode("utf-8")


def write_to_firestore(data: dict, write_path: str, update_record: bool = True):  # ignore_in_test_coverage

    db = firestore.Client(project=GCP_PROJECT_ID)
    sep_idx = write_path.rindex('/')
    coll = write_path[:sep_idx]
    doc_id = write_path[sep_idx+1:]

    data['createTime'] = dt.datetime.now()

    log.info(f"Writing document with id: {doc_id} to firestore collection at: {coll}")

    return db.collection(coll).document(doc_id).set(data, merge=update_record)


def publish_message(topic: str, payload, attributes: dict = {}):  # ignore_in_test_coverage
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(GCP_PROJECT_ID, topic)
    message = encode_payload(payload) if type(payload) == str else payload
    attrs = attributes or {}

    return publisher.publish(topic_path, message, **attrs).result(5)  # wait for <= 5 seconds
