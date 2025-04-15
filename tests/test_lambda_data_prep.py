import unittest
import boto3, json
from moto import mock_s3
from lambda_data_prep.lambda_function import lambda_handler
import pandas as pd
import io

class TestLambdaDataPrep(unittest.TestCase):
    @mock_s3
    def test_lambda_data_prep(self):
        bucket = 'test-bucket' #update with your bucket if needed, and drop below data
        raw_key = 'raw/sensor_data.csv'
        train_key = 'train/data.csv'

        s3 = boto3.client('s3')
        s3.create_bucket(Bucket=bucket)

        df_raw = pd.DataFrame({
            'temperature': [20, 21, 22],
            'humidity': [50, 51, 52]
        })
        csv_buffer = io.StringIO()
        df_raw.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=bucket, Key=raw_key, Body=csv_buffer.getvalue())

        with patch('lambda_data_prep.lambda_function.BUCKET', bucket), \
             patch('lambda_data_prep.lambda_function.RAW_KEY', raw_key), \
             patch('lambda_data_prep.lambda_function.TRAIN_KEY', train_key):
            response = lambda_handler({}, {})

        self.assertEqual(response['statusCode'], 200)

        result = s3.get_object(Bucket=bucket, Key=train_key)
        df_result = pd.read_csv(io.BytesIO(result['Body'].read()))

        self.assertIn('temperature_future', df_result.columns)
        self.assertIn('humidity_future', df_result.columns)
        self.assertEqual(len(df_result), 2)

if __name__ == '__main__':
    unittest.main()

