from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from domain.services import FileCompareService, CompareService

from .database import SessionFactory
from .repositories import SQLAlchemyFileCompareRepository, ApiCompareRepository

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


@app.post("/compare")
async def compare(files: list[UploadFile] = File(...)):
    repo = ApiCompareRepository()
    service = CompareService(compare_repo=repo)
    uploading_files = [(f.filename, await f.read()) for f in files]
    return service.compare(uploading_files)
