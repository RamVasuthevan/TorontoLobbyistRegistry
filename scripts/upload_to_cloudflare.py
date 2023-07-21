import boto3
import sys
from config import Config

def upload_to_cloudflare(file_name, timestamp):
    s3 = boto3.resource('s3',
        endpoint_url = f'https://{Config.CLOUDFLARE_ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id = Config.CLOUDFLARE_ACCESS_KEY_ID,
        aws_secret_access_key = Config.CLOUDFLARE_SECRET_ACCESS_KEY
    )

    bucket_name = Config.CLOUDFLARE_R2_BUCKET_NAME
    if not bucket_name:
        print("Bucket name not set in environment variables.")
        sys.exit(1)

    # Create a new folder with the timestamp
    new_folder = f"{bucket_name}/{timestamp}"
    s3.Object(bucket_name, f"{new_folder}/").put()

    # Upload the file to the new folder
    s3.meta.client.upload_file(file_name, bucket_name, f"{new_folder}/{file_name}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python upload_to_cloudflare.py <file_name> <timestamp>")
        sys.exit(1)

    file_name = sys.argv[1]
    timestamp = sys.argv[2]

    upload_to_cloudflare(file_name, timestamp)
