from dotenv import load_dotenv
import logging
import utils as u
import catalog_observer.event_dispatch as ed
from synthetic.core import synthesize_n_upload

logging.basicConfig(level=logging.DEBUG)


def upload_synthetic_file(request):  # ignore_in_test_coverage
    load_dotenv()
    args = u.parse_request(request)
    dataset = args['dataset']
    num_examples = args['num_examples'] if 'num_examples' in args else None
    return synthesize_n_upload(dataset, num_examples)


def catalog_dataset_update_event_processor(event: dict, context):  # ignore_in_test_coverage
    return ed.catalog_update_dispatcher(event)
