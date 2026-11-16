
# --------------------------------------------------
# S3 VERSIONING - LANDING
# --------------------------------------------------

resource "aws_s3_bucket_versioning" "landing" {
  bucket = aws_s3_bucket.landing.id

  versioning_configuration {
    status = "Enabled"
  }
}

# --------------------------------------------------
# S3 VERSIONING - BRONZE
# --------------------------------------------------

resource "aws_s3_bucket_versioning" "bronze" {
  bucket = aws_s3_bucket.bronze.id

  versioning_configuration {
    status = "Enabled"
  }
}
