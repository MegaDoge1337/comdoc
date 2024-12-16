from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from domain.services import FileCompareService, FactExtractionService

from .database import SessionFactory
from .repositories import SQLAlchemyFileCompareRepository, ApiFactExtractionRepository

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/file_compares")
async def get_file_compares():
    session = SessionFactory()
    repo = SQLAlchemyFileCompareRepository(session=session)
    service = FileCompareService(file_compare_repo=repo)
    return service.get_list()


@app.post("/extract_facts")
async def extract_facts(files: list[UploadFile] = File(...)):
    repo = ApiFactExtractionRepository()
    service = FactExtractionService(compare_repo=repo)
    uploading_files = [(f.filename, await f.read()) for f in files]
    return service.extract_facts(uploading_files)
