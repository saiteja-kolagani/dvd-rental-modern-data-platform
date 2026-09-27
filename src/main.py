from datetime import datetime
from utils.setup_logger import logger
from config.settings import validate_settings

def main():

    job_start_timestamp = datetime.now().astimezone()

    logger.info("Pipeline Started...")
    logger.info(f"Execution started at {job_start_timestamp}")

    validate_settings()


if __name__=="__main__":
    main()