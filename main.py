from src.utils.setup_logger import logger
from src.ingestion.ingestion_service import run_ingestion


def main():
    logger.info("Pipeline Started...")
    run_ingestion()

if __name__=="__main__":
    main()