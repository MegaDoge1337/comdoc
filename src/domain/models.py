from dataclasses import dataclass

@dataclass
class DocumentFile:
    name: str
    md5: str
    bytes_size: int
    path: str