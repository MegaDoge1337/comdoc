from typing import Any

from .models import FileCompare, ComparedFact, ComapareResult, Fact
from .repositories import FileCompareRepository, \
                            FactExtractionRepository, \
                            FactRepository, \
                            FileProcessRepository, \
                            FileStorageRepository, \
                            PdfHighlightRepository

class FileCompareService:
    def __init__(self, file_compare_repo: FileCompareRepository):
        self.repo = file_compare_repo
    
    def list(self) -> list[FileCompare]:
        return self.repo.list()
    
    def get_by_id(self, id: int) -> FileCompare:
        return self.repo.get_by_id(id)

class FactExtractionService:
    def __init__(self, fact_extraction_repo: FactExtractionRepository):
        self.repo = fact_extraction_repo
    
    def extract_facts(self, files: list[tuple[str, bytes]]) -> Any:
        return self.repo.extract_facts(files)

class FactComparatorService:
    def __init__(self, 
        fact_repo: FactRepository,
        file_compare_repo: FileCompareRepository
    ):
        self.fact_repo = fact_repo
        self.file_compare_repo = file_compare_repo
    
    def compare(self, file_compare_id: int) -> ComapareResult:
        file_compare = self.file_compare_repo.get_by_id(file_compare_id)

        result = ComapareResult(
            fist_file_name=file_compare.first_file_name,
            first_file_guid=file_compare.first_file_guid,
            second_file_name=file_compare.second_file_name,
            second_file_guid=file_compare.second_file_guid,
            facts=[]
        )

        f_facts = self.fact_repo.list_by_id(file_compare.first_file_proces_id)
        s_facts = self.fact_repo.list_by_id(file_compare.second_file_proces_id)

        f_facts_len = len(f_facts)
        s_facts_len = len(s_facts)

        if f_facts_len > s_facts_len:
            for f_fact in f_facts:
                fact = ComparedFact(
                    fact_localization=f_fact.fact_localization,
                    line_number=f_fact.line_number,
                    f_value=f_fact.fact_value,
                    s_value=None,
                    f_info=f_fact.info,
                    s_info=None,
                    is_equals=False
                )

                for s_fact in s_facts:
                    is_same_name = s_fact.fact_localization == f_fact.fact_localization
                    is_same_line = s_fact.line_number == f_fact.line_number

                    if is_same_name and is_same_line:
                        fact.s_value = s_fact.fact_value
                        fact.s_info = s_fact.info
                        fact.is_equals = f_fact.fact_value == s_fact.fact_value
                        break

                result.facts.append(fact)
        else:
            for s_fact in s_facts:
                fact = ComparedFact(
                    fact_localization=s_fact.fact_localization,
                    line_number=s_fact.line_number,
                    s_value=s_fact.fact_value,
                    f_value=None,
                    s_info=s_fact.info,
                    f_info=None,
                    is_equals=False
                )

                for f_fact in f_facts:
                    is_same_name = f_fact.fact_localization == s_fact.fact_localization
                    is_same_line = f_fact.line_number == s_fact.line_number

                    if is_same_name and is_same_line:
                        fact.f_value = f_fact.fact_value
                        fact.f_info = f_fact.info
                        fact.is_equals = s_fact.fact_value == f_fact.fact_value
                        break

                result.facts.append(fact)

        return result

class FileProcessService:
    def __init__(self, file_compare_repo: FileCompareRepository,
                 file_process_repo: FileProcessRepository):
        self.file_compare_repo = file_compare_repo
        self.file_process_repo = file_process_repo
    
    def check_processing(self, file_compare_id: int) -> bool:
        file_compare = self.file_compare_repo.get_by_id(file_compare_id)
        
        if not file_compare:
            return None
        
        first_file_process = self.file_process_repo.get_by_id(file_compare.first_file_proces_id)
        second_file_process = self.file_process_repo.get_by_id(file_compare.second_file_proces_id)

        is_first_file_processed = first_file_process.status == "done"
        is_second_file_processed = second_file_process.status == "done"

        return {
            "file_compare": file_compare_id,
            "is_done": is_first_file_processed and is_second_file_processed
        }

class PdfHighlightService:
    def __init__(self, pdf_highlight_repo: PdfHighlightRepository,
                 file_storage_repo: FileStorageRepository,
                 file_compare_repo: FileCompareRepository,
                 fact_repo: FactRepository):
        self.pdf_highlight_repo = pdf_highlight_repo
        self.file_storage_repo = file_storage_repo
        self.file_compare_repo = file_compare_repo
        self.fact_repo = fact_repo
    
    def hightlight_facts(self, file_compare_id: int, target: str) -> bytes:
        file_compare = self.file_compare_repo.get_by_id(file_compare_id)
        
        facts = None
        file_bytes = None

        if target == "f_file":
            facts = self.fact_repo.list_by_id(file_compare.first_file_proces_id)
            file_bytes = self.file_storage_repo.get_by_name(file_compare.first_file_guid)
        
        if target == "s_file":
            facts = self.fact_repo.list_by_id(file_compare.second_file_proces_id)
            file_bytes = self.file_storage_repo.get_by_name(file_compare.second_file_guid)

        return self.pdf_highlight_repo.highlight_facts(facts, file_bytes)