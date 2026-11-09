
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceFile:

    file_name: str
    table_name: str
    file_size_bytes: int

    local_path: Path | None = None

    source_bucket: str | None = None
    source_key: str | None = None
