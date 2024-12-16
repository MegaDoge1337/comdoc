from typing import Any

from .models import FileCompare
from .repositories import FileCompareRepository, FactExtractionRepository

class FileCompareService:
    def __init__(self, file_compare_repo: FileCompareRepository):
        self.repo = file_compare_repo
    
    def get_list(self) -> list[FileCompare]:
        return self.repo.list()

class FactExtractionService:
    def __init__(self, fact_extraction_repo: FactExtractionRepository):
        self.repo = fact_extraction_repo
    
    def extract_facts(self, files: list[tuple[str, bytes]]) -> Any:
        return self.repo.extract_facts(files)