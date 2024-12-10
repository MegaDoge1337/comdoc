import os
import hashlib
from pathlib import Path

from domain.services import FilesUploadingService
from domain.models import DocumentFile

from fastapi import UploadFile


class OsFileUploadingService(FilesUploadingService):

    async def upload_file(self, file: UploadFile) -> DocumentFile:
        file_bytes = await file.read()
        
        uploads_dir = Path(os.environ["UPLOADS_DIR"])
        file_path = uploads_dir / file.filename

        open(file_path, "wb").write(file_bytes)

        document_file = DocumentFile(
            name=file.filename,
            md5=hashlib.md5(file_bytes).hexdigest(),
            bytes_size=int(file.size),
            path=file_path
        )

        return document_file
        