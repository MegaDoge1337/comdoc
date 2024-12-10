from abc import ABC, abstractmethod
from typing import Any

from .models import DocumentFile

class FilesManageService(ABC):
    
    @abstractmethod
    async def save_file(self, file: Any) -> DocumentFile:
        pass
