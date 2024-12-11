import os
from pathlib import Path

from domain.services import FilesManageService
from domain.models import DocumentFile

from fastapi import UploadFile


class LocalFilesManageService(FilesManageService):
    """
    Service for local file management (uploading, reading and etc).
    """
    def __init__(self):
        local_files_dir = os.environ.get("LOCAL_FILES_DIR")
        if not local_files_dir:
            raise ValueError("Enviroment variable `LOCAL_FILES_DIR` not defined")
        
        self.local_files_dir = Path(local_files_dir)

    async def save_file(self, file: UploadFile) -> DocumentFile:
        file_bytes = await file.read()
        
        file_path = self.local_files_dir / file.filename

        open(file_path, "wb").write(file_bytes)

        document_file = DocumentFile(
            name=file.filename,
            path=file_path
        )

        return document_file
        