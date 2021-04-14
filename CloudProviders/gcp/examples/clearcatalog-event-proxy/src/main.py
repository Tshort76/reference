import logging
import clearcatalog_event_proxy.event_dispatch as ed

logging.basicConfig(level=logging.INFO)

# ed.assert_properly_configured()


def clearcatalog_event_proxy(event: dict, context):  # ignore_in_test_coverage
    return ed.catalog_update_dispatcher(event)
