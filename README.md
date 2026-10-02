# Chat with Your PDF — Local RAG Application

A fully local **Retrieval-Augmented Generation (RAG)** application that allows users to upload a PDF document and ask questions about its contents.

The application extracts text from the PDF, splits it into meaningful chunks, converts the chunks into vector embeddings, stores them in a local vector database, retrieves the most relevant content for a question, and uses a locally running LLM to generate a grounded answer.

No paid AI APIs are required.

---

## 🚀 Overview

**Chat with Your PDF** demonstrates the core concepts behind a RAG-based AI application using a completely local development stack.

Instead of sending the entire document to a language model, the application:

1. Extracts text from the uploaded PDF.
2. Splits the text into sentence-aware chunks.
3. Generates embeddings for each chunk.
4. Stores the embeddings in ChromaDB.
5. Converts the user's question into an embedding.
6. Retrieves the most relevant document chunks.
7. Sends only the retrieved context to the local LLM.
8. Generates an answer grounded in the retrieved document content.
9. Displays the answer along with the source pages.

---

## ✨ Features

- 📄 Upload PDF documents
- 🔍 Semantic document search
- 🧩 Sentence-aware document chunking
- 🧠 Local text embeddings using FastEmbed
- 🗄️ Local vector storage using ChromaDB
- 🤖 Local LLM inference using Ollama
- 💬 Ask natural-language questions about uploaded documents
- 📚 Document-specific retrieval
- 📑 Source page references
- 🚫 No paid API keys required
- 🔒 Document processing runs locally
- ⚡ React + FastAPI architecture

---

## 🏗️ Architecture

```text
┌───────────────────────────────┐
│        React Frontend         │
│       TypeScript + MUI        │
└───────────────┬───────────────┘
                │
                │ HTTP
                ▼
┌───────────────────────────────┐
│          FastAPI              │
│          Backend              │
└───────────────┬───────────────┘
                │
                ▼
       ┌─────────────────┐
       │   PDF Upload    │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │     PyMuPDF     │
       │  Text Extraction│
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │    Chunking     │
       │ Sentence-aware  │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │    FastEmbed    │
       │   Embeddings    │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │    ChromaDB     │
       │  Vector Store   │
       └────────┬────────┘
                │
                │ Retrieval
                ▼
       ┌─────────────────┐
       │     Ollama      │
       │   llama3.2:3b   │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │ Grounded Answer │
       │ + Source Pages  │
       └─────────────────┘
```

---

## 🔄 RAG Pipeline

### 1. Document ingestion

When a PDF is uploaded, the backend extracts its text using **PyMuPDF**.

### 2. Chunking

The extracted text is normalized and divided into sentence-aware chunks.

The current implementation uses:

- Chunk size: `1200` characters
- Chunk overlap: `200` characters

The overlap helps preserve context between neighboring chunks.

### 3. Embedding generation

Each document chunk is converted into a numerical vector using:

```text
BAAI/bge-small-en-v1.5
```

The application uses FastEmbed to run the embedding model locally.

### 4. Vector storage

The generated embeddings are stored in **ChromaDB**.

The application uses cosine similarity for semantic retrieval.

### 5. Question embedding

When the user asks a question, the question is converted into an embedding using the same embedding model.

### 6. Retrieval

ChromaDB searches for the most semantically similar chunks belonging to the selected document.

The current application retrieves the top 3 chunks.

### 7. LLM generation

The retrieved chunks are passed as context to:

```text
Ollama
└── llama3.2:3b
```

The LLM is instructed to answer using only the supplied document context.

If the required information cannot be found in the retrieved context, the application instructs the model not to invent an answer.

### 8. Sources

The API returns the retrieved chunks together with their document ID, page number, chunk ID, and retrieval distance.

The frontend displays the source pages along with the generated answer.

---

## 🛠️ Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Material UI (MUI)
- Fetch API

### Backend

- Python
- FastAPI
- Uvicorn
- PyMuPDF
- FastEmbed
- ChromaDB
- Ollama

### Local AI

**Embedding model**

```text
BAAI/bge-small-en-v1.5
```

**Language model**

```text
llama3.2:3b
```

### Development Tools

- Git
- GitHub
- VS Code
- PowerShell

---

## 📁 Project Structure

```text
Chat-PDF-(RAG)/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   └── services/
│   │       ├── embedding_service.py
│   │       ├── llm_service.py
│   │       ├── pdf_service.py
│   │       ├── rag_service.py
│   │       └── vector_service.py
│   │
│   ├── sample_data/
│   ├── requirements.txt
│   │
│   └── test_*.py
│
├── frontend/
│   ├── src/
│   │   ├── services/
│   │   │   └── api.ts
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── .gitignore
└── README.md
```

---

## 💻 Prerequisites

Make sure the following are installed:

- Python 3.12+
- Node.js 22+
- npm
- Git
- Ollama

The application is designed to run locally and does not require a paid cloud AI service.

---

# ⚙️ Setup

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Chat-PDF-(RAG)
```

---

## 2. Backend setup

Navigate to the backend:

```powershell
cd backend
```

Create and activate a Python virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## 3. Install and prepare Ollama

Install Ollama and make sure it is running.

Pull the local model:

```powershell
ollama pull llama3.2:3b
```

Test the model:

```powershell
ollama run llama3.2:3b
```

Then try:

```text
What is 2 + 2?
```

---

## 4. Start the backend

From the `backend` directory:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

---

## 5. Start the frontend

Open another terminal and navigate to:

```powershell
cd frontend
```

Install frontend dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The application will normally be available at:

```text
http://localhost:5173
```

---

# 🧪 Example

Upload a PDF and ask questions such as:

```text
What certifications are mentioned in the document?
```

```text
What technologies does the candidate use for frontend development?
```

```text
What experience does the candidate have with backend technologies?
```

```text
What are the candidate's educational qualifications?
```

The application retrieves relevant document sections and uses those sections as context for the generated answer.

---

# 🧪 Testing

The backend contains individual test scripts used during development to validate different parts of the pipeline.

Examples include:

```text
test_pdf.py
test_pdf_service.py
test_chunking.py
test_embedding.py
test_embedding_service.py
test_vector_service.py
test_rag_retrieval.py
test_rag_service.py
test_rag_pipeline.py
test_ollama.py
test_llm_service.py
```

These tests were used to validate:

- PDF extraction
- Chunk creation
- Embedding generation
- Vector storage
- Semantic retrieval
- LLM connectivity
- RAG answer generation
- End-to-end RAG functionality

---

# 🔐 Privacy

This project is designed around local processing.

Documents are processed locally by the application and the LLM runs through Ollama on the local machine.

No OpenAI API key or paid AI API is required.

> Note: Users should still review their local environment, logs, storage, and any future deployment configuration before processing sensitive documents.

---

# ⚠️ Current Limitations

This is currently a local development/portfolio project.

Current limitations include:

- One active document is selected for a chat session.
- Uploaded files are stored locally.
- No authentication or user accounts.
- No cloud deployment.
- No production-grade document lifecycle management.
- No OCR support for image-only PDFs.
- LLM performance depends on available local system memory.
- The current UI provides basic source display rather than advanced source navigation.
- Ollama and the local model must be installed separately.

---

# 🔮 Future Improvements

Potential improvements include:

- [ ] Multi-document management
- [ ] Document listing and deletion
- [ ] Conversation history
- [ ] Streaming LLM responses
- [ ] Improved source citations
- [ ] Expandable source previews
- [ ] Drag-and-drop PDF upload
- [ ] PDF size and security validation
- [ ] Better error handling
- [ ] Automated backend tests
- [ ] Docker support
- [ ] Production-ready configuration
- [ ] Authentication
- [ ] OCR for scanned PDFs
- [ ] RAG evaluation metrics
- [ ] Retrieval quality improvements
- [ ] Conversation persistence

---

# 🎯 Learning Goals

This project was built to understand and demonstrate the fundamentals of a RAG system rather than simply calling an external AI API.

Key concepts explored include:

- Retrieval-Augmented Generation
- Text chunking
- Sentence-aware chunking
- Embeddings
- Query vs. document embeddings
- Vector databases
- Semantic similarity search
- Cosine distance
- Metadata filtering
- Context construction
- Grounded LLM generation
- Local LLM inference
- FastAPI backend architecture
- React frontend integration

---

## 📌 Project Status

**Current status: Working local MVP**

The core flow is implemented and tested:

```text
PDF Upload
    ↓
Text Extraction
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Semantic Retrieval
    ↓
Ollama
    ↓
Grounded Answer
    ↓
Source Pages
```

The next stage is focused on improving the application's UI/UX, reliability, testing, documentation, and containerization.

---

## 👩‍💻 Author

**Upanita Mahala**

Software Developer | React | TypeScript | Full-Stack Development

Built as a hands-on project to explore local AI, RAG architecture, vector search, embeddings, and LLM-powered applications.
