import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.pdf_service import extract_pdf_chunks
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.rag_service import RAGService
from app.services.llm_service import LLMService


app = FastAPI(
    title="Chat with Your PDF",
    description="A local RAG application for chatting with PDF documents.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embedding_service = EmbeddingService()
vector_service = VectorService()
llm_service = LLMService()

rag_service = RAGService(
    embedding_service=embedding_service,
    vector_service=vector_service,
    llm_service=llm_service,
)


class ChatRequest(BaseModel):
    question: str
    document_id: str


@app.get("/")
def root():
    return {
        "message": "Chat with Your PDF API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    document_id = str(uuid.uuid4())

    file_bytes = await file.read()

    temporary_path = f"sample_data/{document_id}.pdf"

    with open(temporary_path, "wb") as output_file:
        output_file.write(file_bytes)

    chunks = extract_pdf_chunks(
        temporary_path,
        document_id,
    )

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embedding_service.embed_documents(
        documents
    )

    vector_service.add_documents(
        chunks,
        embeddings,
    )

    return {
        "message": "PDF uploaded and processed successfully.",
        "document_id": document_id,
        "filename": file.filename,
        "chunks": len(chunks),
    }


@app.post("/api/chat")
def chat(request: ChatRequest):
    return rag_service.answer_question(
        request.question,
        document_id=request.document_id,
    )