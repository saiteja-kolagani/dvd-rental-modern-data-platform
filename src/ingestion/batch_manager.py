from utils.setup_logger import logger
from datetime import datetime, timezone
from dataclasses import dataclass

@dataclass(frozen=True)
class BatchContext:
    batch_id: str
    ingestion_timestamp: datetime
    ingestion_date: str 

def create_batch_context() -> BatchContext:

    ingestion_timestamp = datetime.now(timezone.utc)
    batch_id = f"{ingestion_timestamp.strftime('%Y%m%d_%H%M%S')}_dvdrental"
    ingestion_date = ingestion_timestamp.strftime('%Y-%m-%d')

    return BatchContext(
        ingestion_timestamp=ingestion_timestamp,
        batch_id=batch_id,
        ingestion_date=ingestion_date
    )