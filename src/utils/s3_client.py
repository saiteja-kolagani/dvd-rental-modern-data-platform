import boto3

from pathlib import Path
from botocore.exceptions import ClientError
from src.utils.setup_logger import logger

class S3Client:
    def __init__(self, region_name: str):
        self.client = boto3.client('s3', region_name=region_name)

    def upload_file_to_s3(self, local_path: Path, bucket: str, s3_key: str) -> None:

        file_path = Path(local_path)
        
        if not file_path.is_file():
            raise FileNotFoundError(f"Local file not found: {file_path}")
        
        try:
            logger.info(f"File uploading to s3: {str(file_path)}")

            self.client.upload_file(
                str(file_path),
                bucket,
                s3_key,
                ExtraArgs={
                    "ContentType": "text/csv"
                }
            )

            logger.info(f"File:{file_path.name} uploaded successfully to S3://{bucket}/{s3_key}")

        except ClientError as error:
            logger.error(f"Failed to upload file: {file_path.name} due to {error}")
            raise

    def download_file_from_s3(self, bucket: str, s3_key: str, local_path: str) -> None:
        file_path = Path(local_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            self.client.download_file(bucket, s3_key, str(file_path))

            logger.info(f"Downloaded s3://{bucket}/{s3_key}")

        except ClientError as error:
            logger.exception(f"S3 download failed: {s3_key} due to {error}")
            raise

    def copy_s3_object(self, source_bucket: str, source_key: str, destination_bucket: str, destination_key: str) -> None:
        try:
            self.client.copy_object(
                CopySource={
                    "Bucket": source_bucket,
                    "Key": source_key
                },
                Bucket=destination_bucket,
                Key=destination_key
            )

            logger.info(
                f"Copied s3://{source_bucket}/{source_key}"
                f" to s3://{destination_bucket}/{destination_key}"
            )

        except ClientError:
            logger.exception(
                f"S3 copy failed: {source_key}"
            )
            raise  