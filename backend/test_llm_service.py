from app.services.llm_service import LLMService


def main():
    service = LLMService()

    question = "What technologies does Upanita use for backend development?"

    context = """
The resume states that Upanita has experience developing
Java Spring Boot backend services and REST APIs.
She has also worked with Java-based API consumption
and integration of SOAP and REST for distributed data flows.
"""

    answer = service.generate_answer(
        question,
        context,
    )

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()