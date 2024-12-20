from fastapi import FastAPI, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware

from domain.services import FileCompareService, \
                            FactExtractionService, \
                            FactComparatorService, \
                            FileProcessService, \
                            PdfHighlightService

from .database import SessionFactory
from .repositories import SQLAlchemyFileCompareRepository, \
                            ApiFactExtractionRepository, \
                            SQLAlchemyFactRepository, \
                            SQLAlchemyFileProcessRepository, \
                            MinioFileStorageRepository, \
                            FitzPdfHighlightRepository

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
    return service.list()


@app.post("/extract_facts")
async def extract_facts(files: list[UploadFile] = File(...)):
    repo = ApiFactExtractionRepository()
    service = FactExtractionService(fact_extraction_repo=repo)
    uploading_files = [(f.filename, await f.read()) for f in files]
    return service.extract_facts(uploading_files)


@app.get("/compare_facts/{file_compare_id}")
async def compare_facts(file_compare_id: int):
    session = SessionFactory()

    fact_repo = SQLAlchemyFactRepository(session=session)
    file_compare_repo = SQLAlchemyFileCompareRepository(session=session)

    service = FactComparatorService(
        fact_repo=fact_repo,
        file_compare_repo=file_compare_repo
    )

    return service.compare(file_compare_id)

@app.get("/check_processing/{file_compare_id}")
async def check_processing(file_compare_id: int):
    session = SessionFactory()

    file_compare_repo = SQLAlchemyFileCompareRepository(session=session)
    file_process_repo = SQLAlchemyFileProcessRepository(session=session)

    service = FileProcessService(
        file_compare_repo=file_compare_repo,
        file_process_repo=file_process_repo
    )

    return service.check_processing(file_compare_id)

@app.get("/view_file/{file_compare_id}/{target}")
async def view_file(file_compare_id: int, target: str):
    session = SessionFactory()

    pdf_highlight_repo = FitzPdfHighlightRepository()
    file_storage_repo = MinioFileStorageRepository()
    file_compare_repo = SQLAlchemyFileCompareRepository(session=session)
    fact_repo = SQLAlchemyFactRepository(session=session)

    service = PdfHighlightService(pdf_highlight_repo=pdf_highlight_repo,
                                  file_storage_repo=file_storage_repo,
                                  file_compare_repo=file_compare_repo,
                                  fact_repo=fact_repo)

    file_bytes = service.hightlight_facts(file_compare_id, target)

    return Response(file_bytes, headers={
        "Content-Disposition": f"inline; filename=\"{target}\""
    }, media_type="application/pdf")