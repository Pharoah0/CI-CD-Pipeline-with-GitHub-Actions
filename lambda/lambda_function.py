import boto3
import os
import sys
import io
import zipfile

S3_BUCKET = os.getenv("S3_BUCKET_NAME", "pe-ekimetrics-ad-campaign-data")
DEPENDENCY_KEY = "dependencies.zip"
DOWNLOAD_PATH = "/tmp/dependencies.zip"
EXTRACT_PATH = "/tmp/python"

s3 = boto3.client("s3")

def download_dependencies():
    """Download and extract dependencies from S3 if not already extracted."""
    if not os.path.exists(EXTRACT_PATH):
        s3 = boto3.client("s3")
        s3.download_file(S3_BUCKET, DEPENDENCY_KEY, DOWNLOAD_PATH)

        with zipfile.ZipFile(DOWNLOAD_PATH, "r") as zip_ref:
            zip_ref.extractall(EXTRACT_PATH)

        sys.path.append(EXTRACT_PATH)

download_dependencies()

import numpy as np
import pandas as pd

# Standardized platform names
platform_corrections = {
    "Facebok": "Facebook",
    "Gooogle Ads": "Google Ads",
    "Tik-Tok": "TikTok"
}

def get_latest_file(prefix="raw/"):
    """Fetch the latest file from the raw S3 bucket."""
    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix)
    if "Contents" in response:
        latest_file = max(response["Contents"], key=lambda x: x["LastModified"])["Key"]
        return latest_file
    return None

def lambda_handler(event, context):
    latest_file = get_latest_file()
    if not latest_file:
        return {"status": "No new data found"}

    print(f"Processing file: {latest_file}")

    # Read file from S3
    obj = s3.get_object(Bucket=S3_BUCKET, Key=latest_file)
    df = pd.read_csv(io.BytesIO(obj["Body"].read()), dtype={
        "campaign_id": str,
        "platform": str,
        "date": str,
        "impressions": "Int64",
        "clicks": "Int64",
        "spend": float,
        "conversions": "Int64"
    })

    # Drop duplicates & clean data
    df.drop_duplicates(inplace=True)
    df["platform"] = df["platform"].replace(platform_corrections)
    df["clicks"].fillna(df["clicks"].median(), inplace=True)
    df["conversions"].fillna(0, inplace=True)
    df.dropna(subset=["campaign_id", "date"], inplace=True)

    # Feature Engineering
    df["CTR"] = (df["clicks"] / df["impressions"]).fillna(0)
    df["ROI"] = (df["conversions"] / df["spend"]).replace([np.inf, -np.inf], 0).fillna(0)

    # Save processed data
    timestamp = latest_file.split("_")[-1].replace(".csv", "")
    processed_file_key = f"processed/ad_campaign_data_{timestamp}.csv"

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=S3_BUCKET, Key=processed_file_key, Body=csv_buffer.getvalue())

    print(f"Processed file saved as: {processed_file_key}")
    return {"status": "Success", "processed_records": len(df)}