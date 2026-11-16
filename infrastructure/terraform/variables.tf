
variable "aws_region" {
  description = "AWS region for project infrastructure"
  type        = string
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "landing_bucket_name" {
  description = "Existing S3 Landing bucket"
  type        = string
}

variable "bronze_bucket_name" {
  description = "Existing S3 Bronze bucket"
  type        = string
}
