variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "domain_name" {
  description = "Existing Route 53 Hosted Zone Domain Name"
  type        = string
  default     = "mycompanydomain.com"
}

variable "record_name" {
  description = "Subdomain prefix for Route 53 record"
  type        = string
  default     = "app"
}
