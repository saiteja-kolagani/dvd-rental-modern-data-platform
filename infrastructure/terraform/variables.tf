
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



# --------------------------------------------------
# Networking
# --------------------------------------------------

variable "vpc_cidr" {
  description = "CIDR block for the project VPC"
  type        = string
  default     = "10.20.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Public subnet for the SSM EC2 instance"
  type        = string
  default     = "10.20.10.0/24"
}

variable "private_subnet_a_cidr" {
  description = "Private subnet in ap-south-1a"
  type        = string
  default     = "10.20.1.0/24"
}

variable "private_subnet_b_cidr" {
  description = "Private subnet in ap-south-1b"
  type        = string
  default     = "10.20.2.0/24"
}

# --------------------------------------------------
# RDS PostgreSQL
# --------------------------------------------------

variable "db_identifier" {
  description = "RDS PostgreSQL instance identifier"
  type        = string
  default     = "dvd-rental-postgres-dev"
}

variable "db_name" {
  description = "Initial PostgreSQL database name"
  type        = string
  default     = "dvdrental"
}

variable "db_username" {
  description = "RDS master username"
  type        = string
  default     = "dvd_admin"
}

variable "db_engine_version" {
  description = "PostgreSQL engine version"
  type        = string
  default     = "17.11"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t4g.micro"
}

variable "db_allocated_storage" {
  description = "Initial RDS storage in GB"
  type        = number
  default     = 20
}

# --------------------------------------------------
# SSM EC2
# --------------------------------------------------

variable "ssm_instance_type" {
  description = "EC2 instance type for SSM access"
  type        = string
  default     = "t3.micro"
}
