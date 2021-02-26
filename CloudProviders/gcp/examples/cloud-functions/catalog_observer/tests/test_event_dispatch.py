import base64
import catalog_observer.event_dispatch as ed
import importlib.resources as rsrc
import json


mock_events = json.loads(rsrc.read_text('catalog_observer.resources', 'mock_catalog_update_events.json'))


def test_file_update_type():
    assert ed.catalog_update_type(mock_events['new_file_event']) == ed.CatalogUpdateEventType.NEW_UPLOAD
    assert ed.catalog_update_type(mock_events['new_bq_table_event']) is None
    assert ed.catalog_update_type(mock_events['invalid_file_event']) == ed.CatalogUpdateEventType.FILE_INVALID
    assert ed.catalog_update_type(mock_events['valid_file_event']) == ed.CatalogUpdateEventType.FILE_VALID


def test_catalog_update_dispatcher(mocker):
    mocker.patch('catalog_observer.event_dispatch.catalog_update_type', return_value='a')
    mocker.patch.dict('catalog_observer.event_dispatch.EVENT_HANDLERS', {'a': [lambda x: 1, lambda x: 2]})
    msg = {'data': base64.b64encode('{"name": "Ralph"}'.encode("utf-8"))}

    assert ed.catalog_update_dispatcher(msg) == [1, 2]


def test_publish_event_fn(mocker):
    mocker.patch('utils.publish_message', side_effect=lambda x, y, z: [x, y, z])
    msg = {'raw_data': "Message", 'attributes': "Attributes", 'type': 'Dummy'}

    assert ed.publish_event_fn('A')(msg) == ['A', 'Message', 'Attributes']
    assert ed.publish_event_fn('B')(msg) == ['B', 'Message', 'Attributes']
    assert ed.publish_event_fn('C')({'raw_data': "M", 'attributes': "A", 'type': 'a'}) == ['C', 'M', 'A']
