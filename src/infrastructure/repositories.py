import os
import requests
from urllib.parse import urljoin

from sqlalchemy.orm import Session

from domain.models import FileCompare, CompareInstance
from domain.repositories import FileCompareRepository, CompareRepository

from .orm import FileCompareORM

class SQLAlchemyFileCompareRepository(FileCompareRepository):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def list(self) -> list[FileCompare]:
        file_compare_orm = self.session.query(FileCompareORM).all()
        return [
            FileCompare(id=fc.id, 
                        first_file_name=fc.f_file_name,
                        second_file_name=fc.s_file_name,
                        first_file_guid=fc.f_file_guid,
                        second_file_guid=fc.s_file_guid)
            for fc in file_compare_orm
        ]

class ApiCompareRepository(CompareRepository):
    def __init__(self) -> None:
        self.api_url = os.environ.get("COMPARE_SERVICE_URL")

        if not self.api_url:
            raise ValueError("Environment variable `COMPARE_SERVICE_URL` not defined")
    
    def compare(self, files: list[tuple[str, bytes]]):
        first_file = files[0]
        second_file = files[1]
        
        if not first_file:
            raise ValueError("First recieved file is None or corrupted")
        
        if not second_file:
            raise ValueError("Second recieved file is None or corrupted")
        
        files = {
            "file1": first_file,
            "file2": second_file
        }

        response = requests.post(urljoin(self.api_url, "/Upload"), files=files)
        response_json = response.json()

        return CompareInstance(
            file_compare=int(response_json.get("file_compare")),
            message=response_json.get("message"),
        )
