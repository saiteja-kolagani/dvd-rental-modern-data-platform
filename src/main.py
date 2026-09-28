from datetime import datetime
from utils.setup_logger import logger
from config.settings import validate_settings
from ingestion.batch_manager import create_batch_context

def main():

    batch = create_batch_context()

    job_start_timestamp = batch.ingestion_timestamp

    logger.info("Pipeline Started...")
    logger.info(f"Execution started at {job_start_timestamp}")
    logger.info(f"Batch ID: {batch.batch_id}")
    logger.info(f"Ingestion Date: {batch.ingestion_date}")

    validate_settings()


if __name__=="__main__":
    main()