from abc import ABC, abstractmethod
from typing import Any

from .models import DocumentFile, CompareOutput

class FilesManageService(ABC):
    """Service for files management"""
    @abstractmethod
    async def save_file(self, file: Any) -> DocumentFile:
        pass

class CompareDocumentService(ABC):
    """Service for comparing documents"""
    @abstractmethod
    async def compare_documents(
        self, 
        first_document: Any, 
        second_document: Any
    ) -> CompareOutput:
        pass
