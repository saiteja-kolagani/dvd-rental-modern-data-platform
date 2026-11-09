
from pathlib import Path

from src.ingestion.source_file import SourceFile
from src.ingestion.file_discovery import discover_csv_files


class LocalSource:

    def __init__(self, data_path: str):
        self.data_path = data_path

    def discover_files(self) -> list[SourceFile]:

        paths = discover_csv_files(self.data_path)

        return [
            SourceFile(
                file_name=path.name,
                table_name=path.stem,
                file_size_bytes=path.stat().st_size,
                local_path=path,
            )
            for path in paths
        ]
