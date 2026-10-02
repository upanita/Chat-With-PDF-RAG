import ollama


MODEL_NAME = "llama3.2:3b"


class LLMService:
    def __init__(self):
        self.model = MODEL_NAME

    def generate_answer(self, question, context):
        prompt = f"""
You are a helpful assistant answering questions about a document.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I couldn't find that information in the document."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]