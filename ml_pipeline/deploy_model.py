import boto3
import os
import tarfile
import argparse

def download_model(bucket, s3_key, local_path):
    s3 = boto3.client('s3')
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    print(f"⬇️ Downloading model from s3://{bucket}/{s3_key}...")
    s3.download_file(bucket, s3_key, local_path)
    print("✅ Download complete.")

def extract_model(tar_path, extract_to):
    print(f"📦 Extracting {tar_path} to {extract_to}...")
    os.makedirs(extract_to, exist_ok=True)
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=extract_to)
    print("✅ Extraction complete.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket', required=True, help='S3 bucket name')
    parser.add_argument('--s3-key', required=True, help='Path to model.tar.gz in S3')
    parser.add_argument('--output-dir', default='./device/model/', help='Local directory to store the model')
    parser.add_argument('--extract', action='store_true', help='Extract tar.gz if specified')

    args = parser.parse_args()

    tar_path = os.path.join(args.output_dir, 'model.tar.gz')

    download_model(args.bucket, args.s3_key, tar_path)

    if args.extract:
        extract_model(tar_path, args.output_dir)

if __name__ == "__main__":
    main()

