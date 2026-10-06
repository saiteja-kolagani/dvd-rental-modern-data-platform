import os

from src.utils.setup_logger import logger
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

def discover_csv_files(data_path: str | None = None) -> list[Path]:


    try: 
        logger.info('Started execution of discover_csv_files() function')
        logger.info(f"Initial data_path: {data_path}")

        PROJECT_ROOT_DIR = Path(__file__).parent.parent.parent

        logger.info(f"Project Root Directory: {PROJECT_ROOT_DIR}")

        if data_path is None:
            data_path = os.getenv('RAW_DATA_PATH')
            logger.info(f"data_path from environmental variables: {data_path}")

        raw_path = PROJECT_ROOT_DIR / data_path

        logger.info(f"Raw Path from root folder: {raw_path}")

        if not raw_path.exists():
            raise FileNotFoundError(f"Raw data directory does not exist: {raw_path}")

        if not raw_path.is_dir():
            raise NotADirectoryError(f"Raw data path is not a directory: {raw_path}")

        csv_files = sorted(raw_path.glob("*.csv"))

        logger.info(f"CSV Files: {csv_files}")

        if not csv_files:
            raise FileNotFoundError(f"No CSV files are found in {raw_path}")

        return csv_files
    except Exception as error:
        logger.error(f"discover_csv_files() failed due to {error}")
        raise RuntimeError(f"discover_csv_files() failed due to {error}")
    
    