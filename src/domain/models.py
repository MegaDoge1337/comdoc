from dataclasses import dataclass
    
@dataclass
class FileCompare:
    id: int
    first_file_name: str
    second_file_name: str
    first_file_guid: str
    second_file_guid: str
    first_file_proces_id: int
    second_file_proces_id: int

@dataclass
class FactInfo:
    id: int
    probability: float
    confidence: float
    page: int
    top: float
    left: float
    width: float
    height: float

@dataclass
class Fact:
    id: int
    fact_name: str
    fact_localization: str
    fact_value: str
    line_number: int
    info: FactInfo

@dataclass
class ComparedFact:
    fact_localization: str
    line_number: int
    f_value: str
    s_value: str
    f_info: FactInfo
    s_info: FactInfo
    is_equals: bool

@dataclass
class ComapareResult:
    fist_file_name: str
    first_file_guid: str
    second_file_name: str
    second_file_guid: str
    facts: list[ComparedFact]