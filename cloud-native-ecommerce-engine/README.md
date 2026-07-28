# Full-Scale Cloud-Native RESTful E-Commerce Engine

Production-ready RESTful backend microservice platform built with **Python, FastAPI, AWS Cognito, PostgreSQL (RDS), Redis Caching, API Gateway, and S3 Presigned Media Uploads**.

## Features
1. **Catalog Management & Redis Caching**: Sub-5ms response time using Cache-Aside strategy.
2. **Presigned S3 Media Uploads**: Secure direct-to-S3 image uploading offloading API servers.
3. **Authentication**: AWS Cognito JWT token authorization.
4. **FastAPI Endpoints**: Production REST endpoints for products, orders, and media upload.

## Repository Layout
* `app/main.py`: FastAPI server router.
* `app/requirements.txt`: Python dependencies.
* `Dockerfile`: Container image configuration.
* `terraform/main.tf`: Infrastructure as Code (IaC) configuration.
* `tests/test_api.py`: Automated Pytest suite.
