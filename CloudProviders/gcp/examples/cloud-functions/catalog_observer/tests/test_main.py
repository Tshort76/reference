import main


def test_dispatch(mocker):
    mocker.patch(
        'catalog_observer.event_dispatch.catalog_update_dispatcher',
        return_value=3
    )

    assert main.catalog_dataset_update_event_processor({'data': ''}, None) == 3
