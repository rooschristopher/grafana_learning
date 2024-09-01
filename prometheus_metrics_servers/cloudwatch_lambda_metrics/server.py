import boto3
import time
from prometheus_client import start_http_server, Gauge

# Define Prometheus metrics
log_entry_count = Gauge('lambda_log_entry_count', 'Number of new log entries in CloudWatch for Lambda function')

# CloudWatch Logs client for LocalStack
logs_client = boto3.client(
    'logs',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    endpoint_url='http://localstack:4566'
)

# Initialize the timestamp of the last processed log event
last_processed_timestamp = 0

# Function to scrape CloudWatch logs and update the Prometheus metric
def scrape_logs():
    global last_processed_timestamp

    log_group_name = '/aws/lambda/my_lambda'  # Replace with your log group name

    # Describe log streams
    log_streams = logs_client.describe_log_streams(
        logGroupName=log_group_name,
        orderBy='LastEventTime',
        descending=True,
        limit=1  # Get the latest log stream
    )

    if 'logStreams' in log_streams and len(log_streams['logStreams']) > 0:
        log_stream_name = log_streams['logStreams'][0]['logStreamName']

        # Get log events
        log_events = logs_client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            startTime=last_processed_timestamp + 1,  # Fetch logs after the last processed timestamp
            startFromHead=True
        )

        # Update the Prometheus metric with the count of new log events
        new_log_count = len(log_events['events'])
        log_entry_count.set(new_log_count)

        # Update the last processed timestamp if there are new logs
        if new_log_count > 0:
            last_processed_timestamp = log_events['events'][-1]['timestamp']

    else:
        log_entry_count.set(0)  # No logs found, set count to 0

if __name__ == '__main__':
    # Start the Prometheus metrics server
    start_http_server(8000)

    while True:
        scrape_logs()
        time.sleep(10)