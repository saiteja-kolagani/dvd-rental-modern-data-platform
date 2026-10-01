from utils.setup_logger import logger
from ingestion.ingestion_service import run_ingestion


def main():
    logger.info("Pipeline Started...")
    run_ingestion()

if __name__=="__main__":
    main()