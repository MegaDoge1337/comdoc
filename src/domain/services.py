from .models import FileCompare
from .repositories import FileCompareRepository

class FileCompareService:
    def __init__(self, file_compare_repo: FileCompareRepository):
        self.repo = file_compare_repo
    
    def get_list(self) -> list[FileCompare]:
        return self.repo.list()
