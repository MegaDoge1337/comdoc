from .models import FileCompare, CompareInstance
from .repositories import FileCompareRepository, CompareRepository

class FileCompareService:
    def __init__(self, file_compare_repo: FileCompareRepository):
        self.repo = file_compare_repo
    
    def get_list(self) -> list[FileCompare]:
        return self.repo.list()

class CompareService:
    def __init__(self, compare_repo: CompareRepository):
        self.repo = compare_repo
    
    def compare(self, files: list[tuple[str, bytes]]) -> CompareInstance:
        return self.repo.compare(files)