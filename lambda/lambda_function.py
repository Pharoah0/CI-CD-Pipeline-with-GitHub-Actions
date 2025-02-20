import numpy as np
import pandas as pd
import boto3
import os
import io

# Standardized platform names
platform_corrections = {
    "Facebok": "Facebook",
    "Gooogle Ads": "Google Ads",
    "Tik-Tok": "TikTok"
}

s3 = boto3.client("s3")
S3_BUCKET = os.getenv("S3_BUCKET_NAME", "pe-ekimetrics-ad-campaign-data")

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
    obj = s3.get_object(Bucket=S3_BUCKET, Key=latest_file)
    
    # Choose a chunk size that balances speed and memory usage.
    chunk_size = 1000000  # 1,000,000 rows per chunk
    total_records = 0
    part_num = 1
    timestamp = latest_file.split("_")[-1].replace(".csv", "")
    
    # Process and upload each chunk separately.
    for chunk in pd.read_csv(
        obj["Body"],
        dtype={
            "campaign_id": str,
            "platform": str,
            "date": str,
            "impressions": "Int64",
            "clicks": "Int64",
            "spend": float,
            "conversions": "Int64"
        },
        chunksize=chunk_size
    ):
        # Process the chunk:
        chunk.drop_duplicates(inplace=True)
        chunk["platform"] = chunk["platform"].replace(platform_corrections)
        # Use assignment to avoid chained warnings:
        chunk["clicks"] = chunk["clicks"].fillna(chunk["clicks"].median())
        chunk["conversions"] = chunk["conversions"].fillna(0)
        chunk = chunk.dropna(subset=["campaign_id", "date"])
        chunk["CTR"] = (chunk["clicks"] / chunk["impressions"]).fillna(0)
        chunk["ROI"] = (chunk["conversions"] / chunk["spend"]).replace([np.inf, -np.inf], 0).fillna(0)
        
        records = len(chunk)
        total_records += records

        # Convert the chunk to CSV string.
        # Write header for the first part only.
        csv_data = chunk.to_csv(index=False, header=(part_num == 1))
        
        # Define the S3 key for this part.
        key = f"processed/ad_campaign_data_{timestamp}_part{part_num}.csv"
        s3.put_object(Bucket=S3_BUCKET, Key=key, Body=csv_data)
        print(f"Uploaded chunk part {part_num} with {records} records.")
        
        part_num += 1

    print(f"Processing complete. Total records processed: {total_records} in {part_num - 1} parts.")
    return {"status": "Success", "processed_records": total_records, "parts": part_num - 1}
