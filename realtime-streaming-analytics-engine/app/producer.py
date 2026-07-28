import json
import time
import random
import uuid
import boto3
from datetime import datetime

REGION = "us-east-1"
STREAM_NAME = "order-events-stream"

kinesis = boto3.client("kinesis", region_name=REGION)

def generate_order():
    return {
        "order_id": str(uuid.uuid4()),
        "customer_id": f"CUST-{random.randint(100, 999)}",
        "amount": round(random.uniform(10.0, 500.0), 2),
        "item": random.choice(["Laptop", "Phone", "Headphones", "Monitor", "Keyboard"]),
        "timestamp": datetime.utcnow().isoformat()
    }

def start_producing():
    print(f"Starting event stream producer to Kinesis Stream: {STREAM_NAME}...")
    while True:
        order = generate_order()
        kinesis.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(order),
            PartitionKey=order["customer_id"]
        )
        print(f"Pushed Order: {order['order_id']} | Amount: ${order['amount']}")
        time.sleep(1)

if __name__ == "__main__":
    start_producing()
