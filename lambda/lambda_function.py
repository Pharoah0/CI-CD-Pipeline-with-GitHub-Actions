import boto3
import pandas as pd
import io
import numpy as np

s3 = boto3.client('s3')
BUCKET_NAME = "pe-ekimetrics-ad-campaign-data"

# Standardized platform names
platform_corrections = {
    "Facebok": "Facebook",
    "Gooogle Ads": "Google Ads",
    "Tik-Tok": "TikTok"
}

def get_latest_file(prefix="raw/"):
    """Fetch the latest file from the raw S3 bucket"""
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    if "Contents" in response:
        latest_file = max(response["Contents"], key=lambda x: x["LastModified"])["Key"]
        return latest_file
    return None

def lambda_handler(event, context):
    # Get the latest raw file
    latest_file = get_latest_file()
    if not latest_file:
        return {"status": "No new data found"}

    print(f"Processing file: {latest_file}")

    # Read file from S3
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=latest_file)
    
    # Read CSV efficiently (handle large datasets)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()), dtype={
        "campaign_id": str,
        "platform": str,
        "date": str,
        "impressions": "Int64",
        "clicks": "Int64",
        "spend": float,
        "conversions": "Int64"
    })

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Standardize platform names
    df["platform"] = df["platform"].replace(platform_corrections)

    # Handle missing values
    df["clicks"].fillna(df["clicks"].median(), inplace=True)  # Fill missing clicks with median
    df["conversions"].fillna(0, inplace=True)  # Assume 0 conversions if missing
    df.dropna(subset=["campaign_id", "date"], inplace=True)  # Remove rows with missing essential fields

    # Feature Engineering
    df["CTR"] = (df["clicks"] / df["impressions"]).fillna(0)  # Avoid NaN if impressions are zero
    df["ROI"] = (df["conversions"] / df["spend"]).replace([np.inf, -np.inf], 0).fillna(0)  # Avoid division by zero

    # Save processed data to S3
    timestamp = latest_file.split("_")[-1].replace(".csv", "")  # Extract timestamp from filename
    processed_file_key = f"processed/ad_campaign_data_{timestamp}.csv"

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=BUCKET_NAME, Key=processed_file_key, Body=csv_buffer.getvalue())

    print(f"Processed file saved as: {processed_file_key}")

    return {"status": "Success", "processed_records": len(df)}
