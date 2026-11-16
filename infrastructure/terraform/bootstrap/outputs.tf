
output "terraform_state_bucket" {
  description = "Terraform remote state S3 bucket"
  value       = aws_s3_bucket.terraform_state.bucket
}
