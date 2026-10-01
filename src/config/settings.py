import os

from utils.setup_logger import logger


AWS_REGION = os.getenv('AWS_REGION')
S3_BRONZE_BUCKET = os.getenv('S3_BRONZE_BUCKET')
RAW_DATA_PATH = os.getenv('RAW_DATA_PATH')

def validate_settings() -> None:

    logger.info("Settings Validation Started...")

    try:
        required_settings = {
            'AWS_REGION': AWS_REGION,
            'S3_BRONZE_BUCKET': S3_BRONZE_BUCKET,
            'RAW_DATA_PATH': RAW_DATA_PATH
        }

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