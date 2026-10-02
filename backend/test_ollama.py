import ollama


def main():
    context = """
    The resume states that the candidate has experience developing
    Java Spring Boot backend services and REST APIs. The candidate
    has also worked with Java-based API consumption and integration
    of SOAP and REST for distributed data flows.
    """

    question = "What technologies does the candidate use for backend development?"

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information provided
in the context below.

Do not use your general knowledge.
Do not invent information.
If the answer is not present in the context, say:
"I couldn't find that information in the provided document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    print("\nOllama response:")
    print(response["message"]["content"])


if __name__ == "__main__":
    main()