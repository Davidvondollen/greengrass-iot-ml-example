variable "aws_region" {
  description = "The AWS region to deploy resources to"
  type        = string
  default     = "us-west-2"
}

variable "iot_thing_name" {
  description = "The name of the IoT Thing device"
  type        = string
  default     = "greengrass-pi"
}

variable "lambda_function_name" {
  description = "Name for the Lambda data preparation function"
  type        = string
  default     = "data-prep"
}

variable "s3_bucket" {
  description = "S3 bucket used for storing model and data"
  type        = string
}
