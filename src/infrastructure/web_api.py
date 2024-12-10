from fastapi import FastAPI, File, UploadFile
from .services import OsFileUploadingService


app = FastAPI()


@app.head("/")
async def ping():
    return None


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    service = OsFileUploadingService()
    document_file = await service.upload_file(file)
    return document_file
