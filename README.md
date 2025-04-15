# Greengrass IoT ML Example

This repository demonstrates an end-to-end IoT solution with edge machine learning inference using AWS IoT Core, Greengrass, Lambda, and SageMaker, deployed via Terraform.

---

## Overview

- **Device**: Raspberry Pi collects sensor data and predicts future sensor states locally using a trained ML model.
- **AWS Cloud**: Sensor data is processed via AWS Lambda and SageMaker for model training.
- **Infrastructure**: Fully automated via Terraform.

---

## Prerequisites

- AWS account with sufficient permissions
- Terraform installed locally
- Raspberry Pi with AWS Greengrass Core installed
- Python 3.9+ installed on the Raspberry Pi
- AWS CLI installed and configured locally and on the Pi

---

## Repository Structure

```
greengrass-iot-ml-example/
├── device/
│   ├── sensor_reader.py            # Sensor data collection script
│   ├── ml_predictor.py             # Local ML inference script
│   └── requirements.txt            # Python dependencies for Raspberry Pi
├── lambda_data_prep/
│   ├── lambda_function.py          # Data preparation AWS Lambda function
│   └── package_lambda.sh           # Script to package and deploy Lambda function
├── ml_pipeline/
│   ├── train.py                    # SageMaker ML model training script
│   ├── deploy_model.py             # Script to deploy trained model to Raspberry Pi
│   └── requirements.txt            # ML pipeline dependencies
├── terraform/
│   ├── main.tf                     # Terraform infrastructure definitions
│   ├── variables.tf                # Terraform variables
│   └── outputs.tf                  # Terraform output definitions
├── tests/
│   ├── test_sensor_reader.py       # Tests for sensor data collection
│   ├── test_lambda_data_prep.py    # Tests for Lambda data prep function
│   └── test_ml_pipeline.py         # Tests for ML training pipeline
├── requirements-test.txt           # Dependencies for test suite
├── README.md                       # Project documentation
└── .gitignore                      # Git ignore file
```

---

## Deployment Steps

### 1. Infrastructure Setup (Terraform)

Navigate to the Terraform directory and deploy the infrastructure:

```bash
cd terraform
terraform init
terraform apply
```

### 2. Deploy AWS Lambda Data Preparation Function

Navigate to the Lambda data prep directory and deploy the AWS Lambda function:

```bash
cd ../lambda_data_prep
bash package_lambda.sh

aws lambda update-function-code \
  --function-name <your-lambda-function-name> \
  --zip-file fileb://package.zip
```

> **Note**: Replace `<your-lambda-function-name>` with your Lambda function's actual name.

### 3. Run SageMaker ML Training Job

Trigger a SageMaker training job using AWS CLI or AWS Console:

```bash
aws sagemaker create-training-job \
  --training-job-name raspberrypi-ml-training \
  --role-arn <sagemaker-role-arn> \
  --algorithm-specification TrainingImage=<your-sklearn-image>,TrainingInputMode=File \
  --input-data-config '[{"ChannelName":"train","DataSource":{"S3DataSource":{"S3Uri":"s3://<bucket>/train/data.csv"}}}]' \
  --output-data-config '{"S3OutputPath":"s3://<bucket>/model/"}' \
  --resource-config '{"InstanceType":"ml.m5.large","InstanceCount":1,"VolumeSizeInGB":10}' \
  --stopping-condition '{"MaxRuntimeInSeconds":600}'
```

> **Note**: Replace placeholders (`<sagemaker-role-arn>`, `<bucket>`, `<your-sklearn-image>`) with your AWS details.

### 4. Deploy ML Model to Raspberry Pi

Download the trained ML model from S3 to your Raspberry Pi:

```bash
aws s3 cp s3://<bucket>/model/model.tar.gz ./
mkdir -p ./device/model/
tar -xzf model.tar.gz -C ./device/model/
```

> **Note**: Adjust the paths and bucket names accordingly.

---

## Running Device Code (Raspberry Pi)

### Manual Execution (for Testing)

Ensure Python dependencies are installed:

```bash
pip install -r device/requirements.txt
```

Run device scripts manually:

```bash
python device/sensor_reader.py
python device/ml_predictor.py
```

### Automated Execution via Greengrass Core

Deploy `sensor_reader.py` and `ml_predictor.py` as Greengrass components through the AWS Greengrass console. Greengrass will handle lifecycle management and automated execution.

---

## Running the Test Suite

### Install Test Dependencies

```bash
pip install -r requirements-test.txt
```

### Execute Tests

Run tests individually or collectively:

```bash
pytest tests/
```

---

## Clean-Up

Remove AWS resources and avoid unnecessary costs:

```bash
cd terraform
terraform destroy
```

> **Caution**: This command permanently deletes AWS resources created by Terraform.

---

