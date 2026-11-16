
# ==================================================
# S3 LIFECYCLE CONFIGURATION
# ==================================================

# --------------------------------------------------
# LANDING BUCKET
# Current objects expire after 90 days.
# Incomplete multipart uploads are aborted after 7 days.
# --------------------------------------------------

resource "aws_s3_bucket_lifecycle_configuration" "landing" {
  bucket = aws_s3_bucket.landing.id

  depends_on = [
    aws_s3_bucket_versioning.landing
  ]

  rule {
    id     = "landing-data-retention"
    status = "Enabled"

    filter {
      prefix = "landing/"
    }

    expiration {
      days = 90
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

# --------------------------------------------------
# BRONZE BUCKET
# Current objects are retained indefinitely.
# Incomplete multipart uploads are aborted after 7 days.
# --------------------------------------------------

resource "aws_s3_bucket_lifecycle_configuration" "bronze" {
  bucket = aws_s3_bucket.bronze.id

  depends_on = [
    aws_s3_bucket_versioning.bronze
  ]

  rule {
    id     = "bronze-abort-incomplete-uploads"
    status = "Enabled"

    filter {
      prefix = "bronze/"
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}
