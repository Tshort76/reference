from enum import Enum


class CatalogUpdateEventType(Enum):
    FILE_INVALID = 'clearcatalog_dataset_updated_fanout_validation_failed'
    NEW_UPLOAD = 'clearcatalog_dataset_updated_fanout_new_file'
    FILE_VALID = 'clearcatalog_dataset_updated_fanout_validation_success'
    MERGED_INTO_DATASET = 'clearcatalog_dataset_updated_fanout_uploaded_to_big_query'
