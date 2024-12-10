from abc import ABC, abstractmethod
from typing import Any

from .models import DocumentFile

class FilesUploadingService(ABC):
    
    @abstractmethod
    async def upload_file(self, file: Any) -> DocumentFile:
        pass
