import boto3
iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda', region_name = 'us-east-2')
env_variables = dict() # Environment Variables
with open('PetBot.zip', 'rb') as f:
  zipped_code = f.read()
role = iam_client.get_role(RoleName='LambdaBasicExecution')
lambda_client.create_function(
  FunctionName='PetBotFunction',
  Runtime='python3.6',
  Role=role['Role']['Arn'],
  Handler='petbot.handler',
  Code=dict(ZipFile=zipped_code),
  Timeout=300, # Maximum allowable timeout
  Environment=dict(Variables=env_variables),
)