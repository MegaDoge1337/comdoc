from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from domain.services import FileCompareService

from .database import SessionFactory
from .repositories import SQLAlchemyFileCompareRepository

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
