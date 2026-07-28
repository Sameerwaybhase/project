output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "alb_dns_name" {
  description = "The public DNS name of the ALB"
  value       = aws_lb.main.dns_name
}

output "route53_fqdn" {
  description = "Fully Qualified Domain Name resolved by Route 53"
  value       = aws_route53_record.alb_dns.fqdn
}
