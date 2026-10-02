from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.llm_service import LLMService


class RAGService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_service: VectorService,
        llm_service: LLMService,
    ):
        self.embedding_service = embedding_service
        self.vector_service = vector_service
        self.llm_service = llm_service

    def answer_question(
        self,
        question,
        document_id,
        top_k=3,
    ):
        query_embedding = self.embedding_service.embed_query(
            question
        )

        results = self.vector_service.search(
            query_embedding,
            document_id=document_id,
            top_k=top_k,
        )

        if not results:
            return {
                "answer": (
                    "I couldn't find relevant information "
                    "in the selected document."
                ),
                "sources": [],
            }

        context_parts = []

        for result in results:
            context_parts.append(
                f"Page {result['page']}:\n"
                f"{result['text']}"
            )

        context = "\n\n".join(context_parts)

        answer = self.llm_service.generate_answer(
            question,
            context,
        )

        return {
            "answer": answer,
            "sources": results,
        }