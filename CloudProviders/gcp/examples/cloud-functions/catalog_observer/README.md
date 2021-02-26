## Deploy
To deploy, run the following:
`gcloud functions deploy catalog_dataset_update_event_processor --runtime python38 --trigger-topic clearcatalog_dataset_updated --service-account cleardata-service@daas-sandbox-pwasden.iam.gserviceaccount.com`

## Tests
Be sure to install `pytest`, `pytest-cov`, and `pytest-mock`.

A [.coveragerc file](https://coverage.readthedocs.io/en/latest/config.html) is included at the project root to configure the coverage report.  Currently, the system is configured to exclude test modules and trivial files from the coverage report, as well as branches/forms that contain a # ignore_in_test_coverage comment on the opening line.

e.g. 
```python
if DEBUG:  # ignore_in_test_coverage
    print("This line and the IF condition will not count towards percent coverage")
```

Then you can use the following for testing (assuming that you are at the project root):

### Run all tests
`pytest -W ignore::DeprecationWarning`

### Run tests in a specific module
`pytest -W ignore::DeprecationWarning catalog_observer/tests/event_dispatch_test.py`

### Coverage report
Print coverage report<br>
`pytest -W ignore::DeprecationWarning --cov-config=.coveragerc --cov=. .`

Generate coverage report at html, showing coverage details<br>
`pytest -W ignore::DeprecationWarning --cov-report html --cov-config=.coveragerc --cov=. .`