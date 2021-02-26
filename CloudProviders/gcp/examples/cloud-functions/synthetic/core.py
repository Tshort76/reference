from datetime import datetime
import os
import synthetic.upload as su
import synthetic.synthesize as ss
import yaml


dataset_to_schema_file = {
    'position': 'resources/position_schema.yaml',
    'transaction': 'resources/transaction_schema.yaml',
    'test': 'resources/test_schema.yaml'
}

default_configs = {
    'GCP_PROJECT': 'daas-sandbox-pwasden',
    'CLEARFILES_UPLOAD_URL': 'https://us-central1-daas-sandbox-pwasden.cloudfunctions.net/clearfiles_upload_url',
    'GCP_SECRET_MANAGER_NAME': 'data-synthesizer-sa-key'
}


def configs():
    env_configs = {k: os.environ[k] for k in ('GCP_TOKEN',
                                             'SYNTHS_SRVC_ACCT_KEY_FILEPATH', 
                                             'SYNTHS_GCP_SECRET_NAME',
                                             'CLEARFILES_UPLOAD_URL',
                                             'GCP_PROJECT') if k in os.environ}

    return {**default_configs, **env_configs}


def gen_schema(dataset: str):

    base_schema_file = 'resources/core_fields_defs.yaml'
    properties_file = dataset_to_schema_file[dataset]

    with open(properties_file) as file:
        schema = yaml.full_load(file)

    if 'definitions' not in schema:
        with open(base_schema_file) as file:
            schema.update(yaml.full_load(file))

    return schema


def __synth_help(dataset: str, n):
    schema = gen_schema(dataset)
    return ss.generate_examples(dataset, schema, n)


def synthesize_n_upload(dataset: str, num_examples: int):

    synthetic_data = __synth_help(dataset, num_examples)
    filename = "synthetic_" + dataset + "_" + str(datetime.now())[:10] + ".json"

    resp, blob = su.upload_to_clearfiles(synthetic_data, filename, configs())

    return blob
