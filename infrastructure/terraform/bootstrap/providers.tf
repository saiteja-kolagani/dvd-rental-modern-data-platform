
provider "aws" {
  region = "ap-south-1"

  default_tags {
    tags = {
      Project     = "DVD-Rental-Modern-Data-Platform"
      Environment = "dev"
      ManagedBy   = "Terraform"
      Purpose     = "Terraform Remote State"
    }
  }
}
