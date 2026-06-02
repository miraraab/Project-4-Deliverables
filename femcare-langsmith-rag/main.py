"""
Main entry point for the FemCare LangSmith RAG application.
"""
import os
import sys
from dotenv import load_dotenv
from rag_pipeline import RAGPipeline


TEST_QUERIES = [
    "What are the first signs of perimenopause?",
    "Why are my periods becoming irregular?",
    "Can I still get pregnant during perimenopause?",
    "What causes hot flashes and night sweats?",
    "Why do I feel anxious or have brain fog?",
    "Should I start HRT? What are the risks vs benefits for me?",
    "How do I know if I've reached menopause?",
    "Why can't I sleep anymore?",
    "What are non-hormonal options for hot flashes?",
    "Why am I gaining weight and what can I do?",
    "I have a family history of breast cancer — is HRT safe for me?",
    "Why do I feel depressed or have mood swings?",
    "What does postmenopause mean exactly?",
]


def print_response(query: str, result: dict, query_number: int, total: int) -> None:
    """
    Pretty-print a single query response.

    Args:
        query: The user's question
        result: The RAG pipeline response
        query_number: Current query number
        total: Total number of queries
    """
    print(f"\n{'='*80}")
    print(f"Query {query_number}/{total}: {query}")
    print(f"{'='*80}")
    print(f"\nAnswer:\n{result['answer']}\n")
    print(f"Sources: {', '.join(result['sources'])}")
    print(f"Confidence: {result['confidence'].upper()}")
    if result['referred_to_doctor']:
        print("⚠️  Doctor consultation recommended")
    print()


def run_test_queries() -> None:
    """Run all 13 test queries sequentially to generate LangSmith traces."""
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("   Please set OPENAI_API_KEY in your .env file")
        sys.exit(1)

    if not os.getenv("LANGCHAIN_API_KEY"):
        print("⚠️  Warning: LANGCHAIN_API_KEY not found in environment variables")
        print("   LangSmith tracing will not be available")

    print("\n" + "="*80)
    print("FemCare Health Navigator - Test Suite")
    print("Running 13 menopause health queries for LangSmith tracing")
    print("="*80)

    pipeline = RAGPipeline()

    for i, query in enumerate(TEST_QUERIES, 1):
        try:
            result = pipeline.query(query)
            print_response(query, result, i, len(TEST_QUERIES))
        except Exception as e:
            print(f"\n❌ Error processing query {i}: {str(e)}")
            continue

    print("\n" + "="*80)
    print(f"✅ Test suite complete! Processed {len(TEST_QUERIES)} queries")
    print("\nLangSmith traces available at: https://smith.langchain.com/projects/femcare-health-navigator")
    print("="*80 + "\n")


def interactive_mode() -> None:
    """Run the application in interactive mode."""
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        sys.exit(1)

    pipeline = RAGPipeline()

    print("\nFemCare Health Navigator - Interactive Mode")
    print("==========================================\n")

    while True:
        query = input("Ask a question (or 'quit' to exit): ").strip()

        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not query:
            continue

        try:
            result = pipeline.query(query)
            print(f"\nAnswer: {result['answer']}\n")
            print(f"Sources: {result['sources']}")
            print(f"Confidence: {result['confidence'].upper()}")
            if result['referred_to_doctor']:
                print("⚠️  Doctor consultation recommended")
            print()
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")


def main() -> None:
    """Main entry point. Run test suite or interactive mode based on arguments."""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        run_test_queries()


if __name__ == "__main__":
    main()
