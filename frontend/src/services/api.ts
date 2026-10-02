const API_BASE_URL = "http://127.0.0.1:8000";

export interface UploadResponse {
  message: string;
  document_id: string;
  filename: string;
  chunks: number;
}

export async function uploadPdf(
  file: File
): Promise<UploadResponse> {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/api/documents/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      error?.detail || "Failed to upload PDF."
    );
  }

  return response.json();
}

export interface ChatSource {
  text: string;
  document_id: string;
  page: number;
  chunk_id: string;
  distance: number;
}

export interface ChatResponse {
  answer: string;
  sources: ChatSource[];
}

export async function askQuestion(
  question: string,
  documentId: string
): Promise<ChatResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/chat`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        document_id: documentId,
      }),
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => null);

    throw new Error(
      error?.detail || "Failed to get an answer."
    );
  }

  return response.json();
}