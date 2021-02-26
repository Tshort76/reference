import catalog_observer.update_ui_state as uus
import auth_utils as au
from catalog_observer.utils import CatalogUpdateEventType
import importlib.resources as rsrc
import json

mock_events = json.loads(rsrc.read_text('catalog_observer.resources', 'mock_catalog_update_events.json'))


def test_cred_local_fetch(mocker):
    mocker.patch('auth_utils.fetch_sa_creds', side_effect=lambda x, y: y)
    mocker.patch.dict('os.environ', {'CLEARDATA_SERVICE_ACCT_KEY_FILEPATH': 'a_file_path'})

    assert uus.__fetch_creds() == {'storage_format': au.CredStoreFormat.SA_KEY_FILE,
                                   'srvc_acct_key_filepath': "a_file_path"}


def test_cred_sm_fetch(mocker):
    mocker.patch('auth_utils.fetch_sa_creds', side_effect=lambda x, y: y)
    mocker.patch.dict('os.environ', {'GCP_SECRET_MANAGER_NAME': 'gcp_secret'})

    assert uus.__fetch_creds() == {'storage_format': au.CredStoreFormat.GCP_SECRET_MANAGER,
                                   'gcp_secret_name': "gcp_secret"}


def test_err_file_naming():
    nm = uus.err_file_display_name("sally.csv")
    assert nm.endswith('.json')
    assert nm.startswith('sally')


def test_ui_state_update(mocker):
    mocker.patch(
        'utils.write_to_firestore',
        side_effect=lambda data, path, update_record: {'data': data, 'path': path}
    )

    event = {
        'payload': mock_events['invalid_file_event'],
        'type': CatalogUpdateEventType.FILE_INVALID
    }

    z = uus.update_ui_state(event)
    z_data = z['result']['data']
    assert z_data == {
        'status': 'INVALID',
        'dataset_id': 'daas.demo.alpha.positions_file',
        'filename': 'Std Positions.csv',
        'file_id': 'my_file_id_12345',
        'bucket': 'artifacts.daas-sandbox-pwasden.appspot.com',
        "blob": 'example_data/validation_errors.json'
    }
    assert z['result']['path'] == 'dataopsui/test/users/test/uploads/my_file_id_12345'

    event = {
        'payload': mock_events['valid_file_event'],
        'type': CatalogUpdateEventType.FILE_VALID
    }
    z = uus.update_ui_state(event)
    z_data = z['result']['data']
    assert z_data == {
        'status': 'VALID',
        'dataset_id': 'daas.demo.alpha.positions_file',
        'filename': 'Std Positions.csv',
        'file_id': 'a_file_id_12345'
    }
    assert z['result']['path'] == 'dataopsui/test_org/users/test_user/uploads/a_file_id_12345'

    event = {
        'payload': mock_events['new_file_event'],
        'type': CatalogUpdateEventType.NEW_UPLOAD
    }
    z = uus.update_ui_state(event)
    z_data = z['result']['data']
    assert z_data == {
        'status': 'PENDING',
        'dataset_id': 'daas.demo.alpha.positions_file',
        'filename': 'valid_file.csv',
        'file_id': '5548ecc8-a85f-4676-94d2-a1063ee2c60a',
        'created_by': 'tester@daas.clearwateranalytics.com'
    }
    assert z['result']['path'] == 'dataopsui/test_org/users/test/uploads/5548ecc8-a85f-4676-94d2-a1063ee2c60a'
