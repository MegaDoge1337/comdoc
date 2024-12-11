from dataclasses import dataclass

@dataclass
class DocumentFile:
    name: str
    path: str

@dataclass
class Session:
    guid: str

@dataclass
class CompareOutput:
    messages: list[str]
    compare_id: int

    def format_message(self) -> str:
        return "\n".join(self.messages)