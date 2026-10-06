import psycopg2

from src.utils.setup_logger import logger

class PostgreSQLClient:

    def __init__(self, host: str, port: str, database: str, user: str, password: str):
        self.connection = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)

    def insert_ingestion_metadata(
            self,
            batch_id,
            ingestion_timestamp,
            ingestion_date,
            source_system,
            source_file,
            source_table,
            s3_bucket,
            s3_key,
            file_size_bytes,
            status,
            error_message=None,
    ):
        query = """
            INSERT INTO dvd_rental_ingestion_metadata (
                batch_id,
                ingestion_timestamp,
                ingestion_date,
                source_system,
                source_file,
                source_table,
                s3_bucket,
                s3_key,
                file_size_bytes,
                status,
                error_message
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            );
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        batch_id,
                        ingestion_timestamp,
                        ingestion_date,
                        source_system,
                        source_file,
                        source_table,
                        s3_bucket,
                        s3_key,
                        file_size_bytes,
                        status,
                        error_message
                    )
                )
            self.connection.commit()
            logger.info(f"Metadata recorded successfully for batch {batch_id}")    
        except Exception as error:
            self.connection.rollback()
            logger.error(f"Failed to insert ingestion metadata for batch {batch_id}: {error}")
            raise

    def close(self):
        if self.connection:
            self.connection.close()
            logger.info("PostgreSQL connection closed.")