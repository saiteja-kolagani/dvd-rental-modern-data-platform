
from src.utils.setup_logger import logger

from src.config.settings import (
    AWS_REGION,
    S3_BRONZE_BUCKET,
    POSTGRES_PASSWORD,
    POSTGRES_USER,
    POSTGRES_DATABASE,
    POSTGRES_PORT,
    POSTGRES_HOST,
    INGESTION_SOURCE,
    validate_settings,
)

from src.ingestion.batch_manager import create_batch_context
from src.ingestion.source_factory import create_source
from src.utils.s3_client import S3Client
from src.utils.postgres_client import PostgreSQLClient


def build_s3_key(file, ingestion_date: str, batch_id: str) -> str:

    return (
        f"bronze/{file.table_name}/"
        f"ingestion_date={ingestion_date}/"
        f"batch_id={batch_id}/"
        f"{file.file_name}"
    )


def run_ingestion() -> None:

    validate_settings()

    batch = create_batch_context()

    logger.info("Starting DVD Rental ingestion...")
    logger.info(f"Batch ID: {batch.batch_id}")
    logger.info(
        f"Batch Ingestion Timestamp: "
        f"{batch.ingestion_timestamp.isoformat()}"
    )
    logger.info(f"Ingestion Source: {INGESTION_SOURCE}")

    # Discover files from configured source
    source = create_source()
    files = source.discover_files()

    if not files:
        raise FileNotFoundError(
            "No CSV files found in the configured source."
        )

    logger.info(f"Discovered {len(files)} CSV files")

    s3_client = S3Client(region_name=AWS_REGION)

    postgres_client = PostgreSQLClient(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DATABASE,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )

    successful_files = 0
    failed_files = 0

    try:

        for file in files:

            s3_key = build_s3_key(
                file=file,
                ingestion_date=batch.ingestion_date,
                batch_id=batch.batch_id,
            )

            logger.info(f"Processing file: {file.file_name}")

            try:

                # LOCAL source
                if INGESTION_SOURCE == "LOCAL":

                    s3_client.upload_file_to_s3(
                        local_path=file.local_path,
                        bucket=S3_BRONZE_BUCKET,
                        s3_key=s3_key,
                    )

                # S3 Landing source
                elif INGESTION_SOURCE == "S3":

                    s3_client.copy_s3_object(
                        source_bucket=file.source_bucket,
                        source_key=file.source_key,
                        destination_bucket=S3_BRONZE_BUCKET,
                        destination_key=s3_key,
                    )

                # Insert successful ingestion metadata
                postgres_client.insert_ingestion_metadata(
                    batch_id=batch.batch_id,
                    ingestion_timestamp=batch.ingestion_timestamp,
                    ingestion_date=batch.ingestion_date,
                    source_system="DVD_RENTAL",
                    source_file=file.file_name,
                    source_table=file.table_name,
                    s3_bucket=S3_BRONZE_BUCKET,
                    s3_key=s3_key,
                    file_size_bytes=file.file_size_bytes,
                    status="SUCCESS",
                )

                successful_files += 1

                logger.info(
                    f"Successfully processed {file.file_name}"
                )

            except Exception as exc:

                failed_files += 1

                logger.exception(
                    f"Failed to process {file.file_name}"
                )

                # Attempt to record failure metadata
                try:

                    postgres_client.insert_ingestion_metadata(
                        batch_id=batch.batch_id,
                        ingestion_timestamp=batch.ingestion_timestamp,
                        ingestion_date=batch.ingestion_date,
                        source_system="DVD_RENTAL",
                        source_file=file.file_name,
                        source_table=file.table_name,
                        s3_bucket=S3_BRONZE_BUCKET,
                        s3_key=s3_key,
                        file_size_bytes=file.file_size_bytes,
                        status="FAILED",
                        error_message=str(exc),
                    )

                except Exception:

                    logger.exception(
                        f"Unable to record FAILED metadata "
                        f"for {file.file_name}"
                    )

    finally:

        postgres_client.close()

        logger.info(
            f"Batch completed: "
            f"Successful={successful_files}, "
            f"Failed={failed_files}, "
            f"Total={len(files)}"
        )

    if failed_files > 0:

        raise RuntimeError(
            f"Ingestion failed. "
            f"Successful: {successful_files}/{len(files)}. "
            f"Failed: {failed_files}/{len(files)}."
        )

    logger.info(
        f"Ingestion completed successfully. "
        f"Batch ID: {batch.batch_id}"
    )
