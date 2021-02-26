## Generate a token locally
`gcloud auth print-identity-token | pbcopy`
## Deploy
To deploy, run the following:
`gcloud functions deploy upload_synthetic_file --runtime python38 --trigger-http --service-account data-synthesizer@daas-sandbox-pwasden.iam.gserviceaccount.com`

After the function has been deployed once (user input expected via std in on function creation), you can run the following to redeploy:
`./scripts/deploy_synthetic.py`
## Run
If you are using the Functions Framework, https://github.com/GoogleCloudPlatform/functions-framework-python, you can debug the function by running

`functions-framework --target=upload_synthetic_file --debug`

from the project root directory.  That will bring up a local gunicorn server and serve up your function over HTTP.  You can then use `curl` to invoke your functions.

`curl -X GET -G localhost:8080/upload_synthetic_file -d 'dataset=test'`
### In GCP
`gcloud functions call upload_synthetic_file --data '{"dataset": "test"}'`
 or use the Trigger tab in the GCP console for the Cloud Function.

# TODO
- Different upload organization (not cwan)