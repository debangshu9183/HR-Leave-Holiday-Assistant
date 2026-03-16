import os
import shutil
import sqlite3
import tempfile
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.pdf_loader import extract_pdf_text
from src.csv_database import load_csv_to_db
from src.prompt import build_prompt
from src.groq_client import create_client, MODEL
from src.chatbot import chat_with_hr

# ── CONFIG ──────────────────────────────────────────────
PDF_PATH = os.getenv("PDF_PATH", r"F:\HR_chatbot\data\Leave Details.pdf")
CSV_PATH = os.getenv("CSV_PATH", r"F:\HR_chatbot\data\Holiday_List_2026.csv")

# ── SHARED STATE ─────────────────────────────────────────
client = None
system_prompt = None
db_connection: Optional[sqlite3.Connection] = None
is_ready = False


def load_pdf(path: str):
    global system_prompt
    system_prompt = build_prompt(extract_pdf_text(path))


def load_csv(path: str):
    global db_connection
    _, db_connection = load_csv_to_db(path)


def check_ready():
    global is_ready
    is_ready = system_prompt is not None and db_connection is not None


# ── STARTUP ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    client = create_client()
    if os.path.exists(PDF_PATH) and os.path.exists(CSV_PATH):
        load_pdf(PDF_PATH)
        load_csv(CSV_PATH)
        check_ready()
        print("HR Assistant ready — data loaded from disk.")
    else:
        print("Data files not found — upload via /upload/pdf and /upload/csv")
    yield
    if db_connection:
        db_connection.close()


# ── APP ──────────────────────────────────────────────────
app = FastAPI(title="TuTeck HR Assistant API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── SCHEMAS ──────────────────────────────────────────────
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    answer: str
    history: List[Message]


# ── ROUTES ───────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "ok",
        "ready": is_ready,
        "pdf_loaded": system_prompt is not None,
        "csv_loaded": db_connection is not None,
    }


@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf" and not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted.")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    try:
        load_pdf(tmp_path)
        check_ready()
        return {"message": f"'{file.filename}' loaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.unlink(tmp_path)


@app.post("/upload/csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files accepted.")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    try:
        load_csv(tmp_path)
        check_ready()
        return {"message": f"'{file.filename}' loaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.unlink(tmp_path)


@app.post("/chat/", response_model=ChatResponse)
async def chat(body: ChatRequest):
    if not is_ready:
        raise HTTPException(
            status_code=503,
            detail="HR Assistant not ready. Upload a PDF and CSV first via /upload/pdf and /upload/csv."
        )
    history = [m.model_dump() for m in body.history]
    answer = chat_with_hr(
        user_question=body.message,
        history=history,
        client=client,
        model=MODEL,
        system_prompt=system_prompt,
        connection=db_connection,
    )
    history.append({"role": "user", "content": body.message})
    history.append({"role": "assistant", "content": answer})
    return ChatResponse(answer=answer, history=[Message(**m) for m in history])