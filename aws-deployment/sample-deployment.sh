#!/bin/bash

# Step 1: Updating homebrew (for mac)
echo "Updating homebrew"
brew update

# Step 2: Installing AWS cli
echo "Installing AWS cli"
brew install awscli

# Step 3: Verifying the installation
echo "Verfifying the installation"
aws --version

# AmazonEC2ContainerRegistryFullAccess
# AmazonEC2FullAccess

# Step 4: Configuring access to AWS
echo "Configuring AWS access"
aws configure

# Step 5: Running the docker container in the background
echo "Running the docker container in the background"
docker-compose up -d

# Step 6: Tagging the docker image as per aws requirements
echo "Tagging the docker image as per aws requirements"
docker tag siddmirjank2696/loan-approval:latest <account_id>.dkr.ecr.<region>.amazonaws.com/siddmirjank2696/loan-approval:latest

# Step 7: Creating am AWS ECR Repository
echo "Creating am AWS ECR Repository"
aws ecr create-repository --repository-name siddmirjank2696/loan-approval

# Step 8: Authenticating docker to ECR
echo "Authenticating docker to ECR"
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account_id>.dkr.ecr.<region>.amazonaws.com

# Step 9: Pushing the docker image to AWS ECR
echo "Pushing the docker image to AWS ECR"
docker push <account_id>.dkr.ecr.<region>.amazonaws.com/siddmirjank2696/loan-approval:latest

# Step 10: Creating an AWS ECS cluster
echo "Creating an AWS ECS cluster"
aws ecs create-cluster --cluster-name my-cluster

# Step 11: Registring the task definition
echo "Registering the task definition"
aws ecs register-task-definition --cli-input-json file://aws-deployment/task-definition.json

# Step 12: Creating a service
aws ecs create-service \
  --cluster my-cluster \
  --service-name my-service \
  --task-definition my-task \
  --desired-count 1 \
  --launch-type EC2

# Step 13: Verifying the application status
echo "Verifying the application status"
aws ecs describe-tasks --cluster my-cluster --tasks <task_id>

