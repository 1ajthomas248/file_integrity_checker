from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

class TrackRequest(BaseModel):
    path: str

class HashResponse(BaseModel):
    filename: str
    sha256: str

class VerifyResponse(BaseModel):
    match: bool
    expected: str
    actual: str

class ScanItem(BaseModel):
    path: str
    status: str
    expected: str | None
    actual: str | None
    message: str | None