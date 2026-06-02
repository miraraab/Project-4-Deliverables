"""
Main entry point for the FemCare LangSmith RAG application.
"""
import os
from dotenv import load_dotenv
from rag_pipeline import RAGPipeline


def main():
    load_dotenv()

    pipeline = RAGPipeline()

    print("FemCare Health Navigator - RAG Application")
    print("==========================================\n")

    while True:
        query = input("Ask a question (or 'quit' to exit): ").strip()

        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not query:
            continue

        result = pipeline.query(query)
        print(f"\nAnswer: {result['answer']}\n")
        print(f"Sources: {result['sources']}\n")


if __name__ == "__main__":
    main()
