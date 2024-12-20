from abc import ABC, abstractmethod
from typing import Any

from .models import FileCompare, Fact, FileProcess

class FileCompareRepository(ABC):
    @abstractmethod
    def list(self) -> list[FileCompare]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> FileCompare:
        pass

class FactExtractionRepository(ABC):
    @abstractmethod
    def extract_facts(self, files: list[tuple[str, bytes]]) -> Any:
        pass

class FactRepository(ABC):
    @abstractmethod
    def list_by_id(self, file_process_id: int) -> list[Fact]:
        pass

class FileProcessRepository(ABC):
    @abstractmethod
    def get_by_id(self, file_process_id: int) -> FileProcess:
        pass

class FileStorageRepository(ABC):
    @abstractmethod
    def get_by_name(self, file_name: int):
        pass

class PdfHighlightRepository(ABC):
    @abstractmethod
    def highlight_facts(self, facts: list[Fact], file_bytes: bytes) -> bytes:
        pass