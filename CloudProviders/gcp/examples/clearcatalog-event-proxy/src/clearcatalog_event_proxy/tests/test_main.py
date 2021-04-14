import main


def test_dispatch(mocker):
    mocker.patch(
        'clearcatalog_event_proxy.event_dispatch.catalog_update_dispatcher',
        return_value=3
    )

    assert main.clearcatalog_event_proxy({'data': ''}, None) == 3
