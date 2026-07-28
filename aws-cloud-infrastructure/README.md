# Automated High-Availability AWS Cloud Infrastructure

Provisioning multi-tier cloud infrastructure using **Terraform** and **AWS CloudFormation**.

## Architecture Highlights
* **VPC**: Multi-AZ layout with 2 Public and 2 Private subnets across distinct Availability Zones.
* **Load Balancer**: Public Application Load Balancer (ALB) handling inbound HTTP traffic.
* **Auto Scaling Group**: EC2 worker instances deployed in private subnets, auto-scaling on 60% CPU threshold.
* **DNS**: Amazon Route 53 Alias record pointing directly to the ALB.

## Project Structure
* `terraform/`: HCL scripts for modular infrastructure deployment.
* `cloudformation/`: AWS CloudFormation template (YAML).
