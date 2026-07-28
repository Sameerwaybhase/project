import json
import os
import logging
import urllib.parse
import boto3
import uuid
from datetime import datetime

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS SDK clients
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Retrieve environment variables
TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME')
CLEAN_BUCKET = os.environ.get('CLEAN_S3_BUCKET_NAME')


def lambda_handler(event, context):
    logger.info(f"Received Event: {json.dumps(event)}")

    try:
        # 1. Extract bucket and object key from event
        record = event['Records'][0]
        src_bucket = record['s3']['bucket']['name']
        src_key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')

        logger.info(f"Processing object '{src_key}' from bucket '{src_bucket}'")

        # 2. Fetch object content from S3
        response = s3_client.get_object(Bucket=src_bucket, Key=src_key)
        raw_content = response['Body'].read().decode('utf-8')
        payload = json.loads(raw_content)

        # 3. Transform and Enrich Payload
        payload['record_id'] = str(uuid.uuid4())
        payload['processed_at'] = datetime.utcnow().isoformat()
        payload['source_file'] = f"s3://{src_bucket}/{src_key}"
        payload['status'] = "PROCESSED"

        # 4. Index Item into DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item=payload)
        logger.info(f"Successfully written record {payload['record_id']} to DynamoDB table {TABLE_NAME}")

        # 5. Save Clean Transformed File to Clean S3 Bucket
        clean_key = f"processed/{payload['record_id']}.json"
        s3_client.put_object(
            Bucket=CLEAN_BUCKET,
            Key=clean_key,
            Body=json.dumps(payload, indent=2),
            ContentType='application/json'
        )
        logger.info(f"Transformed asset saved to s3://{CLEAN_BUCKET}/{clean_key}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Pipeline execution completed successfully.',
                'record_id': payload['record_id']
            })
        }

    except Exception as e:
        logger.error(f"Error processing pipeline event: {str(e)}", exc_info=True)
        raise e
