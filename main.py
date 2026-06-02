import os
import sys
from dotenv import load_dotenv
from rag_pipeline import FemcareRAGPipeline


def main():
    """Run test queries through the FemcareRAGPipeline and generate LangSmith traces."""

    # Load environment variables from .env
    load_dotenv()

    # Validate required API keys
    required_keys = ["OPENAI_API_KEY", "LANGCHAIN_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]

    if missing_keys:
        print("❌ Error: Missing required API keys in .env file")
        for key in missing_keys:
            print(f"   - {key}")
        print("\nPlease ensure your .env file contains:")
        print("   OPENAI_API_KEY=your_openai_api_key")
        print("   LANGCHAIN_API_KEY=your_langsmith_api_key")
        sys.exit(1)

    # Initialize the RAG pipeline
    try:
        print("🚀 Initializing FemcareRAGPipeline...\n")
        pipeline = FemcareRAGPipeline()
    except Exception as e:
        print(f"❌ Error initializing pipeline: {e}")
        sys.exit(1)

    # Test queries to generate LangSmith traces
    test_queries = [
        "What are the main symptoms of PCOS?",
        "How is endometriosis typically diagnosed?",
        "What changes can I expect during perimenopause?",
        "Why do I feel so tired before my period?",
        "Can stress affect my menstrual cycle?"
    ]

    # Process each query
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"Query {i}/5")
        print(f"{'='*70}")

        try:
            # Execute query
            result = pipeline.query(query)

            # Print results
            print(f"\n❓ Question:\n{query}\n")
            print(f"✅ Answer:\n{result['answer']}\n")
            print(f"📚 Sources:\n{', '.join(result['sources']) if result['sources'] else 'No specific sources'}\n")
            print(f"🎯 Confidence: {result['confidence'].upper()}")
            print(f"👨‍⚕️ Doctor Referral: {'Yes ⚠️' if result['referred_to_doctor'] else 'No'}")

        except Exception as e:
            print(f"❌ Error processing query: {e}")
            continue

    # Print final message with LangSmith link
    print(f"\n{'='*70}")
    print("✨ All queries completed!")
    print(f"{'='*70}\n")
    print("📊 LangSmith traces available at:")
    print("   https://smith.langchain.com/projects/femcare-health-navigator\n")


if __name__ == "__main__":
    main()
