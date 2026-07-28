output "raw_s3_bucket_name" {
  description = "Name of the raw S3 bucket for data ingestion"
  value       = aws_s3_bucket.raw.id
}

output "clean_s3_bucket_name" {
  description = "Name of the clean output S3 bucket"
  value       = aws_s3_bucket.clean.id
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.pipeline_db.name
}

output "cloudfront_domain_name" {
  description = "Domain name of CloudFront distribution serving clean assets"
  value       = aws_cloudfront_distribution.s3_distribution.domain_name
}
