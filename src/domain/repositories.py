from abc import ABC, abstractmethod
from typing import Any

from .models import FileCompare

class FileCompareRepository(ABC):
    @abstractmethod
    def list(self) -> list[FileCompare]:
        pass