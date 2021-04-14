## Deploy

### Sandbox
To deploy, run the following:
`gcloud functions deploy clearcatalog_event_proxy --runtime python38 --trigger-topic clear-catalog-dataset-updated --service-account cleardata-service@daas-sandbox-pwasden.iam.gserviceaccount.com`

### Terraform
Navigate to the `scripts` folder and run the `dev_tf_deploy.sh` script.

#### Plan
`cd scripts; ./dev_tf_deploy.sh`

#### Apply
`cd scripts; ./dev_tf_deploy.sh apply`

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
`pytest -W ignore::DeprecationWarning clearcatalog_event_proxy/tests/test_event_dispatch.py`

### Coverage report
Print coverage report<br>
`pytest -W ignore::DeprecationWarning --cov-config=.coveragerc --cov=. .`

Generate coverage report at html, showing coverage details<br>
`pytest -W ignore::DeprecationWarning --cov-report html --cov-config=.coveragerc --cov=. .`