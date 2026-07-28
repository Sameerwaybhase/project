# Serverless Event-Driven Data Processing Pipeline

An event-driven data processing pipeline built on AWS using **Lambda, S3, DynamoDB, CloudFront, Python (Boto3), and CloudWatch**.

## Architecture Overview
1. **Raw S3 Bucket**: Stores raw incoming JSON objects.
2. **S3 Event Notification**: Triggers an AWS Lambda function on `s3:ObjectCreated:*`.
3. **AWS Lambda (Python 3.11)**: Reads the file, enriches data schema, indexes record into DynamoDB, and archives transformed file in Clean S3 Bucket.
4. **DynamoDB**: Key-Value NoSQL database for fast querying.
5. **Clean S3 Bucket + CloudFront CDN**: Delivers clean assets globally with low latency via Origin Access Control (OAC).
6. **CloudWatch**: Logs all Lambda execution logs and raises metrics/alarms on failure.

## Repository Layout
* `src/lambda_function.py`: Core Python data ETL handler.
* `terraform/`: Infrastructure as Code (HCL) to provision all AWS resources.
