# Automated CI/CD Deployment Workflow to AWS EKS

Containerized Python Flask Microservice with automated Continuous Integration & Continuous Deployment (CI/CD) pipelines using **Docker, Amazon ECR, Jenkins, GitHub Actions, AWS EKS, and Kubernetes YAML**.

## Architecture Highlights
1. **Python Flask App**: Production-ready microservice with health check endpoints and unit tests.
2. **Containerization**: Multi-stage lightweight Docker build based on `python:3.11-slim`.
3. **Registry**: Image pushing and vulnerability scanning on **Amazon ECR**.
4. **CI/CD Orchestration**: Dual deployment option via **Jenkinsfile** and **GitHub Actions Workflow** (`deploy.yml`).
5. **Orchestration**: Zero-downtime rolling deployment on **AWS EKS** using Kubernetes manifests.

## Repository Layout
* `app/`: Python Flask source code, requirements, Dockerfile, and pytest tests.
* `k8s/`: Declarative Kubernetes manifests (`deployment.yaml`, `service.yaml`).
* `.github/workflows/deploy.yml`: GitHub Actions automated CI/CD pipeline.
* `Jenkinsfile`: Jenkins declarative automated CI/CD pipeline.
