import os
import sys
import logging

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

print("Setting up Project Root Directory")

try:
    PROJECT_ROOT_DIRECTORY = Path(__file__).parent.parent.parent
except:
    PROJECT_ROOT_DIRECTORY = Path.cwd().parent.parent

print(f"Project Root Directory: {PROJECT_ROOT_DIRECTORY}")

def setup_logger_handler(file_path: str | None = None, level=logging.INFO) -> logging.Logger:

    print("Setup Logger Handler Started...")

    try:

        print("Checking if any handlers existed...")

        root_handler = logging.getLogger()
        if root_handler.handlers:
            return logging.getLogger(__name__)

        if file_path is None:
            file_path = os.getenv('LOG_FILE_PATH')

        print(f"File Path: {file_path}")

        if not file_path:
            raise ValueError('No File Path has provided!')

        log_path = Path(file_path)

        if not log_path.is_absolute():
            log_path = PROJECT_ROOT_DIRECTORY / log_path

        print(f"Absolute Log Path: {log_path}")

        print("Configuring logger...")

        logging.basicConfig(
            level=level,
            format="%(asctime)s | %(funcName)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler(log_path, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ],
            force=True
        )

        return logging.getLogger(__name__)

    except Exception as error:
        print(f"Failed to configure logger due to {error}")
        raise

logger = setup_logger_handler()

