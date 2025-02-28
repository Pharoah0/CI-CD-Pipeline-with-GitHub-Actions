#!/bin/bash
set -e

# Configuration parameters (update these as needed)
AWS_REGION="us-east-1"
LAMBDA_NAME="DataTransformationLambda"
S3_BUCKET="my_s3_bucket"
# Replace with your account ID and the latest layer version
LAYER_ARN="arn:aws:lambda:us-east-1:<ACCOUNT_ID>:layer:PandasNumpyLayer:<LAYER_VERSION>"

echo "Packaging Lambda function code..."

# Remove any existing package folder and create a new one.
rm -rf package
mkdir package

# Copy the lambda function code from the lambda folder.
cp lambda/lambda_function.py package/

# Create the deployment package (function.zip) from the package directory.
cd package && zip -r ../function.zip . && cd ..

echo "Deployment package created. Uploading and updating Lambda function..."

# Deploy the new function code.
aws lambda update-function-code --function-name $LAMBDA_NAME --zip-file fileb://function.zip --region $AWS_REGION

# Update the Lambda function configuration.
aws lambda update-function-configuration \
  --function-name $LAMBDA_NAME \
  --memory-size 1024 \
  --timeout 300 \
  --ephemeral-storage Size=512 \
  --environment "Variables={S3_BUCKET_NAME=$S3_BUCKET}" \
  --layers $LAYER_ARN \
  --region $AWS_REGION

echo "Lambda function $LAMBDA_NAME updated successfully."
