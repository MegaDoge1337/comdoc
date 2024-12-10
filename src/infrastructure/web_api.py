from fastapi import FastAPI, File, UploadFile
from .services import LocalFilesManageService


app = FastAPI()


@app.head("/")
async def ping():
    return None


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    service = LocalFilesManageService()
    document_file = await service.save_file(file)
    return document_file
