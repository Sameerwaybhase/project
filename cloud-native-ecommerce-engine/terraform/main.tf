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

resource "aws_s3_bucket" "media_bucket" {
  bucket        = "ecommerce-product-media-bucket-2026"
  force_destroy = true
}

resource "aws_cognito_user_pool" "pool" {
  name = "ecommerce-user-pool"
}
