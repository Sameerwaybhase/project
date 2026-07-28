# Real-Time Streaming & Analytics Engine

Event-driven real-time data streaming pipeline using **AWS Kinesis Data Streams, AWS Lambda, Amazon DynamoDB, Amazon S3, Amazon Athena, and Streamlit**.

## Features
1. **Producer**: Python script streaming mock order events into AWS Kinesis Data Streams.
2. **Lambda Consumer**: Serverless consumer parsing events, writing hot data to DynamoDB, and archiving to S3.
3. **Athena SQL Queries**: Serverless distributed SQL queries over S3 data lake.
4. **Streamlit UI**: Interactive live dashboard displaying streaming metrics.
5. **Terraform IaC**: Infrastructure provisioning for Kinesis, S3, DynamoDB, and Lambda.

## Repository Layout
* `app/producer.py`: Python event generator streaming order transactions.
* `app/lambda_consumer.py`: Serverless stream record batch consumer.
* `app/dashboard.py`: Streamlit live web visualization app.
* `terraform/main.tf`: Infrastructure as Code (IaC) configuration.
