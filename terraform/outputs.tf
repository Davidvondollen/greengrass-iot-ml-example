output "iot_thing_name" {
  description = "Name of the IoT Thing device"
  value       = aws_iot_thing.pi.name
}

output "lambda_function_name" {
  description = "Name of the deployed Lambda function"
  value       = aws_lambda_function.data_prep.function_name
} 
