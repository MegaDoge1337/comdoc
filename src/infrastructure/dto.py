from pydantic import BaseModel

class FactExtractionDto(BaseModel):
    file_compare: int
    message: str