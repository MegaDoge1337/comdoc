from fastapi import FastAPI, File, UploadFile
from .services import LocalFilesManageService


app = FastAPI()


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    service = LocalFilesManageService()
    document_file = await service.save_file(file)
    return document_file
