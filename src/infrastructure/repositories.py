from sqlalchemy.orm import Session

from domain.models import FileCompare
from domain.repositories import FileCompareRepository

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