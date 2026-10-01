from pathlib import Path
from utils.setup_logger import logger
from config.settings import (
    AWS_REGION,
    S3_BRONZE_BUCKET,
    RAW_DATA_PATH,
    validate_settings
)
from ingestion.batch_manager import create_batch_context
from ingestion.file_discovery import discover_csv_files
from utils.s3_client import S3Client


def build_s3_key(file_path: Path, ingestion_date: str, batch_id: str) -> str:

    table_name = file_path.stem 

    return (
        f"bronze/{table_name}/ingestion_date={ingestion_date}/batch_id={batch_id}/{file_path.name}"
    )


def run_ingestion() -> None:

    validate_settings()

    batch = create_batch_context()

    logger.info(f"Starting DVD Rental ingestion...")
    logger.info(f"Batch ID: {batch.batch_id}")
    logger.info(f"Batch Ingestion Timestamp: {batch.ingestion_timestamp.isoformat()}")

    files = discover_csv_files(RAW_DATA_PATH)

    logger.info(f"Discovered {len(files)} CSV files")

    s3_client = S3Client(region_name=AWS_REGION)

    successful_files = 0

    for file_path in files:
        s3_key = build_s3_key(file_path=file_path, ingestion_date=batch.ingestion_date, batch_id=batch.batch_id)

        logger.info(f"Uploading {file_path.name} to s3://{S3_BRONZE_BUCKET}/{s3_key}")

        try:
            s3_client.upload_file_to_s3(local_path=file_path, bucket=S3_BRONZE_BUCKET, s3_key=s3_key)
            successful_files += 1
            logger.info(f"Successfully uploaded {file_path.name} to S3")
        except Exception:
            logger.exception(f"Failed to upload {file_path.name}")

    logger.info(f"Batch completed: {successful_files}/{len(files)} files uploaded to S3 successfully.")

    if successful_files != len(files):
        raise RuntimeError(
            f"Ingestion failed for one or more files"
            f"Successful: {successful_files}/{len(files)}"
        )

    logger.info(f"Ingestion completed successfully. Batch ID: {batch.batch_id}")
