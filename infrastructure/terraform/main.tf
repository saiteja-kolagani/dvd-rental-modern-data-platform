resource "aws_s3_bucket" "landing" {
  bucket = var.landing_bucket_name

  tags = {
    Name  = "DVD Rental Landing Bucket"
    Layer = "Landing"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket" "bronze" {
  bucket = var.bronze_bucket_name

  tags = {
    Name  = "DVD Rental Bronze Bucket"
    Layer = "Bronze"
  }

  lifecycle {
    prevent_destroy = true
  }
}
