import clearcatalog_event_proxy.update_ui_state as uus
from clearcatalog_event_proxy.utils import CatalogUpdateEventType
import importlib.resources as rsrc
import json

mock_events = json.loads(rsrc.read_text('clearcatalog_event_proxy.tests.resources', 'mock_catalog_update_events.json'))


def test_err_file_naming():
    nm = uus.err_file_display_name("sally.csv")
    assert nm.endswith('.json')
    assert nm.startswith('sally')


def test_ui_state_update(mocker):
    mocker.patch(
        'clearcatalog_event_proxy.utils.write_to_firestore',
        side_effect=lambda data, path: {'data': data, 'path': path}
    )

    event = {
        'payload': mock_events['invalid_file_event'],
        'type': CatalogUpdateEventType.FILE_INVALID
    }

    z = uus.update_ui_state(event)
    z_data = z['result']['data']
    assert z_data == {
        'status': 'INVALID',
        'datasetId': 'daas.demo.alpha.positions_file',
        'filename': 'Std Positions.csv',
        'fileId': 'my_fileId_12345',
        'bucket': 'artifacts.daas-sandbox-pwasden.appspot.com',
        "blob": 'example_data/validation_errors.json'
    }
    assert z['result']['path'] == 'dataopsui/test/users/test/uploads/my_fileId_12345'

    event = {
        'payload': mock_events['valid_file_event'],
        'type': CatalogUpdateEventType.FILE_VALID
    }
    z = uus.update_ui_state(event)
    z_data = z['result']['data']
    assert z_data == {
        'status': 'VALID',
        'datasetId': 'daas.demo.alpha.positions_file',
        'filename': 'Std Positions.csv',
        'fileId': 'a_fileId_12345'
    }
    assert z['result']['path'] == 'dataopsui/test_org/users/test_user/uploads/a_fileId_12345'

    event = {
        'payload': mock_events['new_file_event'],
        'type': CatalogUpdateEventType.NEW_UPLOAD
    }
    z = uus.update_ui_state(event)
    z_data = z['result']['data']
    assert z_data == {
        'status': 'PENDING',
        'datasetId': 'daas.demo.alpha.positions_file',
        'filename': 'valid_file.csv',
        'fileId': '5548ecc8-a85f-4676-94d2-a1063ee2c60a',
        'username': 'Sally'
    }
    assert z['result']['path'] == 'dataopsui/test_org/users/test/uploads/5548ecc8-a85f-4676-94d2-a1063ee2c60a'

    event = {
        'payload': mock_events['bq_record_count_event'],
        'type': CatalogUpdateEventType.DATASET_META_ADDED
    }
    z = uus.update_ui_state(event)
    z_data = z['result']['data']
    assert z_data == {
        'status': 'COMPLETE',
        'datasetId': 'daas.demo.alpha.positions_file',
        'filename': 'positions.csv',
        'fileId': '84dff8ec-e299-4cc9-897b-f691d6082606',
        'recordCount': 2707
    }
    assert z['result']['path'] == 'dataopsui/test/users/test_user/uploads/84dff8ec-e299-4cc9-897b-f691d6082606'
