import boto3
import json

# Create a Lambda client with the LocalStack endpoint
lambda_client = boto3.client(
    'lambda',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    endpoint_url='http://localhost:4566'
)

# Create a CloudWatch Logs client with the LocalStack endpoint
logs_client = boto3.client(
    'logs',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    endpoint_url='http://localhost:4566'
)

# Define the payload
payload = {
    "key": "value"  # Replace with your actual input data
}

# Invoke the Lambda function
response = lambda_client.invoke(
    FunctionName='my_lambda',
    InvocationType='RequestResponse',
    Payload=json.dumps(payload)
)

# Read the response
response_payload = response['Payload'].read().decode('utf-8')
print("Response: ", response_payload)

# Fetch the log group name (assuming it's /aws/lambda/my_lambda)
log_group_name = '/aws/lambda/my_lambda'

# Retrieve the log streams
log_streams = logs_client.describe_log_streams(
    logGroupName=log_group_name,
    orderBy='LastEventTime',
    descending=True,
    limit=1  # Get the latest log stream
)

if 'logStreams' in log_streams and len(log_streams['logStreams']) > 0:
    log_stream_name = log_streams['logStreams'][0]['logStreamName']

    # Get the log events from the latest log stream
    log_events = logs_client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        startFromHead=True
    )

    print("\nLogs:")
    for event in log_events['events']:
        print(event['message'])

else:
    print("No log streams found for the Lambda function.")

