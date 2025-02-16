#!/bin/bash

# Set AWS Region
AWS_REGION="us-east-1"
LAMBDA_NAME="EkimetricsDataProcessing"

# Package Lambda
zip function.zip lambda_function.py

# Deploy to AWS Lambda
aws lambda update-function-code --function-name $LAMBDA_NAME --zip-file fileb://function.zip --region $AWS_REGION

