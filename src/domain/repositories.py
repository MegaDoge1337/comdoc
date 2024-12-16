from abc import ABC, abstractmethod

from .models import FileCompare, CompareInstance

class FileCompareRepository(ABC):
    @abstractmethod
    def list(self) -> list[FileCompare]:
        pass

class CompareRepository(ABC):
    @abstractmethod
    def compare(self, files: list[tuple[str, bytes]]) -> CompareInstance:
        pass