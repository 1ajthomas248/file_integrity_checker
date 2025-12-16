from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from hashing import compute_hash, verify_hash, compute_hash_bytes
from tracking import add_file, remove_file, list_files, scan_files
from schema import VerifyResponse, TrackRequest, HashResponse, ScanItem

app = FastAPI(
    title="File Integrity Checker",
    description="API that gives file integrity information",
    version="1.0.0"
)

@app.post("/hash", response_model=HashResponse)
async def give_hash(file: UploadFile = File(...)):
    try:
        contents = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read uploaded file")
    
    digest = compute_hash_bytes(contents)

    return HashResponse(
        filename=file.filename,
        sha256=digest
    )