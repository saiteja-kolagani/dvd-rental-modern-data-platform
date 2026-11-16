
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "DVD-Rental-Modern-Data-Platform"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}
