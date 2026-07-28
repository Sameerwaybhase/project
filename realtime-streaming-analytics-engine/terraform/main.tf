terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "random_id" "suffix" {
  byte_length = 4
}

# 1. Kinesis Data Stream
resource "aws_kinesis_stream" "order_stream" {
  name             = "order-events-stream"
  shard_count      = 1
  retention_period = 24
}

# 2. DynamoDB Table
resource "aws_dynamodb_table" "live_orders" {
  name         = "LiveOrdersTable"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }
}

# 3. S3 Bucket for Cold Storage
resource "aws_s3_bucket" "cold_storage" {
  bucket        = "cold-orders-data-lake-${random_id.suffix.hex}"
  force_destroy = true
}
