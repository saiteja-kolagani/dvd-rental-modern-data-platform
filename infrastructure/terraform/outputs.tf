
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



output "vpc_id" {
  description = "DVD Rental VPC ID"
  value       = aws_vpc.main.id
}

output "ssm_instance_id" {
  description = "SSM EC2 instance ID"
  value       = aws_instance.ssm.id
}

output "ssm_instance_public_ip" {
  description = "SSM EC2 public IP"
  value       = aws_instance.ssm.public_ip
}

output "rds_endpoint" {
  description = "PostgreSQL RDS endpoint"
  value       = aws_db_instance.postgres.endpoint
}

output "rds_address" {
  description = "PostgreSQL RDS hostname"
  value       = aws_db_instance.postgres.address
}

output "rds_database_name" {
  description = "PostgreSQL database name"
  value       = aws_db_instance.postgres.db_name
}
