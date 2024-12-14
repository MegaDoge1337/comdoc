from dataclasses import dataclass
    
@dataclass
class FileCompare:
    id: int
    first_file_name: str
    second_file_name: str
    first_file_guid: str
    second_file_guid: str
