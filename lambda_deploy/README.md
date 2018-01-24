# For Lambda Deployment

This is slightly tricky. A good outline can be found here: https://codeburst.io/aws-lambda-functions-made-easy-1fae0feeab27

Another good resource: https://github.com/agentreno/lambda-packaging-example

Mostly I 'stole' scripts from there which deal with setting up and deploying your lambda function.

Steps:

Set up the aws command line tool. https://aws.amazon.com/cli/

Get all your AWS stuff configured (Keys, secrets, etc). See: http://boto3.readthedocs.io/en/latest/guide/configuration.html

Set up the virtual environment.

Create a role that will be used to deploy this.
python iamstuff.py

Zip up your code (including necessary stuff from the virtualenv).
. zip_for_lambda.sh

Deploy.
python simple_lambda_create.py

Schedule the job to run hourly (or other cycle).