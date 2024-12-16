from abc import ABC, abstractmethod
from typing import Any

from .models import FileCompare, CompareInstance

class FileCompareRepository(ABC):
    @abstractmethod
    def list(self) -> list[FileCompare]:
        pass

class FactExtractionRepository(ABC):
    @abstractmethod
    def extract_facts(self, files: list[tuple[str, bytes]]) -> Any:
        pass