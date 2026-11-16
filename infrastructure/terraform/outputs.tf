
output "landing_bucket_name" {
  description = "Landing S3 bucket name"
  value       = aws_s3_bucket.landing.bucket
}

output "bronze_bucket_name" {
  description = "Bronze S3 bucket name"
  value       = aws_s3_bucket.bronze.bucket
}

output "aws_region" {
  description = "Configured AWS region"
  value       = var.aws_region
}
