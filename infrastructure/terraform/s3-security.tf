
# --------------------------------------------------
# S3 PUBLIC ACCESS BLOCK - LANDING
# --------------------------------------------------

resource "aws_s3_bucket_public_access_block" "landing" {
  bucket = aws_s3_bucket.landing.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# --------------------------------------------------
# S3 PUBLIC ACCESS BLOCK - BRONZE
# --------------------------------------------------

resource "aws_s3_bucket_public_access_block" "bronze" {
  bucket = aws_s3_bucket.bronze.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# --------------------------------------------------
# SERVER-SIDE ENCRYPTION - LANDING
# --------------------------------------------------

resource "aws_s3_bucket_server_side_encryption_configuration" "landing" {
  bucket = aws_s3_bucket.landing.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# --------------------------------------------------
# SERVER-SIDE ENCRYPTION - BRONZE
# --------------------------------------------------

resource "aws_s3_bucket_server_side_encryption_configuration" "bronze" {
  bucket = aws_s3_bucket.bronze.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
