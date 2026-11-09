
from src.config.settings import (
    INGESTION_SOURCE,
    RAW_DATA_PATH,
    S3_LANDING_BUCKET,
    S3_LANDING_PREFIX,
)

from src.ingestion.local_source import LocalSource
from src.ingestion.s3_source import S3Source
from src.utils.s3_client import S3Client
from src.config.settings import AWS_REGION


def create_source():

    if INGESTION_SOURCE == "LOCAL":
        return LocalSource(
            data_path=RAW_DATA_PATH
        )

    if INGESTION_SOURCE == "S3":
        s3_client = S3Client(
            region_name=AWS_REGION
        )

        return S3Source(
            s3_client=s3_client,
            bucket=S3_LANDING_BUCKET,
            prefix=S3_LANDING_PREFIX,
        )

    raise ValueError(
        f"Unsupported ingestion source: {INGESTION_SOURCE}"
    )
