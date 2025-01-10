import os
import requests
from urllib.parse import urljoin
from typing import Any

from sqlalchemy.orm import Session

from minio import Minio

import fitz

from domain.models import FileCompare, FactInfo, Fact, FileProcess, ComapareResult
from domain.repositories import FileCompareRepository, \
                                FactExtractionRepository, \
                                FactRepository, \
                                FileProcessRepository, \
                                FileStorageRepository, \
                                PdfHighlightRepository

from .orm import FileCompareORM, FactExtractionORM, FactInfoORM, FileProcessORM

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
            fact_info_orm = self.session.query(FactInfoORM).filter(FactInfoORM.fact_extraction_id == fact.id).first()

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

class SQLAlchemyFileProcessRepository(FileProcessRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, file_process_id: int) -> FileProcess:
        file_process_orm = self.session.query(FileProcessORM).filter(FileProcessORM.id == file_process_id).first()

        if not file_process_orm:
            return None
        
        return FileProcess(status=file_process_orm.status)
    
class MinioFileStorageRepository(FileStorageRepository):
    def __init__(self) -> None:
        self.minio_url = os.environ.get("MINIO_URL")
        self.secret_key = os.environ.get("MINIO_SECRET_KEY")
        self.access_key = os.environ.get("MINIO_ACCESS_KEY")
        self.bucket_name = os.environ.get("MINIO_BUCKET_NAME")

        # Get and cast secure arg for Minio client
        secure = os.environ.get("MINIO_SECURE")
        if not secure:
            raise ValueError("Environment variable `MINIO_SECURE` not defined")
        else:
            self.secure = secure == "True"

        if not self.minio_url:
            raise ValueError("Environment variable `MINIO_URL` not defined")

        if not self.secret_key:
            raise ValueError("Environment variable `MINIO_SECRET_KEY` not defined")
        
        if not self.access_key:
            raise ValueError("Environment variable `MINIO_ACCESS_KEY` not defined")

        if not self.bucket_name:
            raise ValueError("Environment variable `MINIO_BUCKET_NAME` not defined")
    
    def get_by_name(self, file_name: str) -> bytes:
        client = Minio(
            self.minio_url, 
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )

        response = client.get_object(self.bucket_name, file_name)
        return response.read()

class FitzPdfHighlightRepository(PdfHighlightRepository):
    def highlight_facts(self, compared_facts: ComapareResult, file_bytes: bytes, target: str) -> bytes:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for compared_fact in compared_facts.facts:
            fact_info = None

            if target == "f_file":
                fact_info = compared_fact.f_info
        
            if target == "s_file":
                fact_info = compared_fact.s_info

            if not fact_info:
                continue

            page = doc[fact_info.page - 1]

            page.remove_rotation()

            x1 = fact_info.left
            y1 = fact_info.top
            x2 = fact_info.left + fact_info.width
            y2 = fact_info.top + fact_info.height

            if compared_fact.is_equals:
                highlight_color = (0, 1, 0)
            else:
                highlight_color = (1, 0, 0)

            highlight_rect = fitz.Rect(x1, y1, x2, y2)
            annot = page.add_rect_annot(highlight_rect)
            annot.set_colors(stroke=highlight_color)
            annot.update()
        
        return doc.write()