import boto3
lambda_client = boto3.client('lambda', region_name = 'us-east-2')
with open('PetBot.zip', 'rb') as f:
  zipped_code = f.read()
lambda_client.update_function_code(
  FunctionName='PetBotFunction',
  ZipFile=zipped_code,
)