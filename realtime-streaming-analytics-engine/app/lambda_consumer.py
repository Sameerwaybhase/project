import json
import base64
import os
import boto3

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

TABLE_NAME = os.environ.get("DYNAMODB_TABLE", "LiveOrdersTable")
BUCKET_NAME = os.environ.get("S3_BUCKET", "cold-orders-data-lake")

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    
    for record in event.get("Records", []):
        payload_bytes = base64.b64decode(record["kinesis"]["data"])
        data = json.loads(payload_bytes.decode("utf-8"))
        
        # 1. Hot Write to DynamoDB
        table.put_item(Item=data)
        
        # 2. Cold Write to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=f"raw/{data['order_id']}.json",
            Body=json.dumps(data)
        )
        
    return {"statusCode": 200, "body": "Processed batch successfully."}
