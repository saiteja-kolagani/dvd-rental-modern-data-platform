from src.utils.setup_logger import logger
from src.ingestion.ingestion_service import run_ingestion


def main():
    logger.info("Pipeline Started...")
    try:
     run_ingestion()
    except Exception as error:
       logger.error(f"Pipeline failed due to {error}")
       raise
    else:
       logger.info("DVD Rental Pipeline Completed Execution Successfully.")

if __name__=="__main__":
    main()