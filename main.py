from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
import io
import os

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

MAX_SIZE = 91 * 1024  # 91 KB
VALID_EXTENSIONS = {".csv", ".json", ".txt"}
REQUIRED_TOKEN = "o16hrb3objnq5ic8"

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    x_upload_token_3056: str = Header(None)
):
    # Authentication
    if x_upload_token_3056 != REQUIRED_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # File type validation
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in VALID_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Read file
    content = await file.read()

    # File size validation
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # CSV processing
    if ext == ".csv":
        text = content.decode("utf-8")
        reader = csv.DictReader(io.StringIO(text))
        rows = list(reader)

        columns = reader.fieldnames
        total_value = 0.0
        category_counts = {}

        for row in rows:
            if "value" in row:
                try:
                    total_value += float(row["value"])
                except:
                    pass
            if "category" in row:
                cat = row["category"]
                category_counts[cat] = category_counts.get(cat, 0) + 1

        return {
            "email": "22f2000984@ds.study.iitm.ac.in",
            "filename": file.filename,
            "rows": len(rows),
            "columns": columns,
            "totalValue": round(total_value, 2),
            "categoryCounts": category_counts,
        }

    return {"message": "File accepted"}
