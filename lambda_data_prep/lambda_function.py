import boto3
import pandas as pd
import io

s3 = boto3.client('s3')
BUCKET = '<your-s3-bucket>'
RAW_KEY = 'raw/sensor_data.csv'
TRAIN_KEY = 'train/data.csv'

def lambda_handler(event, context):
    # Fetch raw sensor data from S3
    response = s3.get_object(Bucket=BUCKET, Key=RAW_KEY)
    df = pd.read_csv(io.BytesIO(response['Body'].read()))

    # Create future columns by shifting data
    df['temperature_future'] = df['temperature'].shift(-1)
    df['humidity_future'] = df['humidity'].shift(-1)
    df.dropna(inplace=True)

    # Save prepared training data directly back to S3
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=BUCKET, Key=TRAIN_KEY, Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': 'Training data prepared successfully!'
    }

