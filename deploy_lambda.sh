#!/bin/bash

# Set AWS Region
AWS_REGION="us-east-1"
LAMBDA_NAME="EkimetricsDataProcessing"

# Package Lambda
rm -rf package
mkdir package
pip install boto3 pandas numpy -t package/
cp lambda_function.py package/
cd package && zip -r ../function.zip .

# Deploy to AWS Lambda
aws lambda update-function-code --function-name $LAMBDA_NAME --zip-file fileb://function.zip --region $AWS_REGION

