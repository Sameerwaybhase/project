provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "kb_documents" {
  bucket        = "enterprise-kb-docs-bucket-2026"
  force_destroy = true
}

resource "aws_opensearchserverless_collection" "vector_db" {
  name = "kb-vector-store"
  type = "VECTORSEARCH"
}
