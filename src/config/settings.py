import os

from src.utils.setup_logger import logger


ENVIRONMENT = os.getenv("ENVIRONMENT", "LOCAL").upper()
INGESTION_SOURCE = os.getenv("INGESTION_SOURCE", "LOCAL").upper()

AWS_REGION = os.getenv('AWS_REGION')
S3_BRONZE_BUCKET = os.getenv('S3_BRONZE_BUCKET')
RAW_DATA_PATH = os.getenv('RAW_DATA_PATH')

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', "5432")
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

def validate_settings() -> None:

    logger.info("Settings Validation Started...")

    try:
        required_settings = {
            'AWS_REGION': AWS_REGION,
            'S3_BRONZE_BUCKET': S3_BRONZE_BUCKET,
            'RAW_DATA_PATH': RAW_DATA_PATH,
            'POSTGRES_HOST': POSTGRES_HOST,
            'POSTGRES_PORT': POSTGRES_PORT,
            'POSTGRES_DATABASE': POSTGRES_DATABASE,
            'POSTGRES_USER': POSTGRES_USER,
            'POSTGRES_PASSWORD': POSTGRES_PASSWORD
        }

        if INGESTION_SOURCE == 'LOCAL':
            required_settings["RAW_DATA_PATH"] = RAW_DATA_PATH

        if INGESTION_SOURCE not in ('LOCAL', 'S3'):
            raise ValueError(f"Unsupported INGESTION_SOURCE: {INGESTION_SOURCE}")

        missing_settings = [name for name, value in required_settings.items() if not value]

        if missing_settings:
            logger.warning(f"missing required settings: {', '.join(missing_settings)}")
            raise ValueError(f"missing required settings: {', '.join(missing_settings)}")
        else:
            logger.info("No missing reuired settings")
            logger.info("Settings Validation completed successfully.")
            

    except Exception as error:
        logger.error(f"Settings validation failed due to {error}")
        raise