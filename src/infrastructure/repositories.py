import os
import requests
from urllib.parse import urljoin
from typing import Any

from sqlalchemy.orm import Session

from domain.models import FileCompare, FactInfo, Fact
from domain.repositories import FileCompareRepository, FactExtractionRepository, FactRepository

from .orm import FileCompareORM, FactExtractionORM, FactInfoORM

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
                        second_file_guid=fc.s_file_guid,
                        first_file_proces_id=fc.f_file_process_id,
                        second_file_proces_id=fc.s_file_process_id)
            for fc in file_compare_orm
        ]
    
    def get_by_id(self, id: int) -> FileCompare:
        file_compare_orm = self.session.query(FileCompareORM).filter(FileCompareORM.id == id).first()

        if not file_compare_orm:
            return None
        
        return FileCompare(
            id=file_compare_orm.id,
            first_file_name=file_compare_orm.f_file_name,
            second_file_name=file_compare_orm.s_file_name,
            first_file_guid=file_compare_orm.f_file_guid,
            second_file_guid=file_compare_orm.s_file_guid,
            first_file_proces_id=file_compare_orm.f_file_process_id,
            second_file_proces_id=file_compare_orm.s_file_process_id
        )

class ApiFactExtractionRepository(FactExtractionRepository):
    def __init__(self) -> None:
        self.api_url = os.environ.get("FACT_EXTRACTION_SERVICE_URL")

        if not self.api_url:
            raise ValueError("Environment variable `FACT_EXTRACTION_SERVICE_URL` not defined")
    
    def extract_facts(self, files: list[tuple[str, bytes]]) -> Any:
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
        return response.json()

class SQLAlchemyFactRepository(FactRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def list_by_id(self, file_process_id: int):
        fact_orm = self.session.query(FactExtractionORM).filter(FactExtractionORM.file_process_id == file_process_id).all()
        facts = [
            Fact(id=f.id,
                 fact_name=f.fact_name,
                 fact_localization=f.fact_localization,
                 fact_value=f.fact_value,
                 line_number=f.line_number,
                 info=None)
            for f in fact_orm
        ]

        for fact in facts:
            fact_info_orm = self.session.query(FactInfoORM).filter(FactInfoORM.id == fact.id).first()

            if not fact_info_orm:
                continue

            fact.info = FactInfo(
                id=fact_info_orm.id,
                probability=fact_info_orm.probability,
                confidence=fact_info_orm.confidence,
                page=fact_info_orm.page,
                top=fact_info_orm.top,
                left=fact_info_orm.left,
                width=fact_info_orm.width,
                height=fact_info_orm.height
            )
        
        return facts