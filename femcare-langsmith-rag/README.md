# Menopause Health Navigator - LangSmith RAG

A Retrieval-Augmented Generation (RAG) application for comprehensive menopause health information, built with LangChain and integrated with LangSmith for observability and tracing.

## Features

- **Menopause-Focused Knowledge Base**: 9 curated medical documents covering vasomotor symptoms, HRT, GSM, bone health, cardiovascular changes, cognitive changes, sleep, mood health, and workplace menopause rights
- **Retrieval-Augmented Generation**: Combines ChromaDB with OpenAI embeddings and GPT-4 for accurate, evidence-based menopause health information
- **LangSmith Integration**: Full observability with `@traceable` decorators on all chain calls and retrieval operations
- **Confidence Scoring**: Automatic relevance scoring (0-1) with low-confidence warnings when sources are weak (<0.7)
- **Doctor Referral System**: Intelligent flagging for topics requiring medical consultation
- **Dual Operating Modes**: Test suite with 13 sample queries or interactive mode for custom questions
- **Vector Database**: ChromaDB with OpenAI embeddings for efficient semantic search
- **Modular Design**: Separate modules for RAG pipeline, knowledge base, and main application

## Project Structure

```
femcare-langsmith-rag/
├── main.py                 # Entry point for the application
├── rag_pipeline.py        # RAG pipeline implementation
├── knowledge_base.py      # Knowledge base management
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
└── README.md             # This file
```

## Installation

1. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `LANGCHAIN_API_KEY`: Your LangSmith API key

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Required. Your OpenAI API key for GPT-4 access
- `LANGCHAIN_API_KEY`: Required. Your LangSmith API key for tracing
- `LANGCHAIN_TRACING_V2`: Set to `true` to enable LangSmith tracing
- `LANGCHAIN_PROJECT`: Project name in LangSmith (default: `menopause-health-navigator`)
- `LANGCHAIN_ENDPOINT`: LangSmith API endpoint (default: `https://api.smith.langchain.com`)

## Usage

### Running the Application

#### Test Suite Mode (Default)
Runs 13 sample menopause health queries to generate LangSmith traces:
```bash
python main.py
```

This will:
- Execute all 13 test queries sequentially
- Display question, answer, sources, confidence level, and doctor referral status for each
- Generate LangSmith traces for analysis
- Print final summary with LangSmith dashboard link

#### Interactive Mode
For custom menopause health questions:
```bash
python main.py --interactive
```

This starts an interactive prompt where you can ask custom menopause-related health questions in real-time.

### Query Response Format

Each query returns a dictionary with:
```python
{
    "answer": str,              # Health information response with citations
    "sources": list,            # Documents cited (WHO, DGGG, PubMed, EMA, NAMS)
    "confidence": str,          # "high" (relevance ≥0.7) or "low" (<0.7)
    "referred_to_doctor": bool  # True if low confidence or sensitive topic
}
```

### Loading Documents

1. Create a `documents/` directory in the project root
2. Add your `.txt` files to the `documents/` directory
3. In your Python code or a script, use:
   ```python
   from knowledge_base import KnowledgeBase
   kb = KnowledgeBase()
   kb.ingest_documents()
   ```

### Programmatic Usage

```python
from rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
result = pipeline.query("What are the first signs of perimenopause?")

print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
print(f"Confidence: {result['confidence']}")
print(f"Doctor consultation recommended: {result['referred_to_doctor']}")
```

## Components

### main.py
Entry point with two operating modes:
- **Test Suite Mode** (default): Runs 13 menopause health test queries sequentially, generating LangSmith traces and detailed output
- **Interactive Mode** (`--interactive` flag): Interactive CLI for custom menopause health questions
- Built-in error handling for missing API keys with clear error messages

### rag_pipeline.py
Implements the RAG pipeline with:
- **@traceable decorators** for full LangSmith tracing of the `query()` method
- OpenAI embeddings for semantic understanding
- Chroma vector store for document retrieval with similarity scoring
- GPT-4 LLM for answer generation with comprehensive system prompt
- Confidence checking: calculates average relevance score of retrieved documents
- Low-confidence detection (<0.7): automatically flags responses requiring doctor consultation
- Tailored system prompt emphasizing menopause-specific health guidance and source citation

### knowledge_base.py
Manages the vector database with:
- 9 curated sample medical documents on menopause (vasomotor symptoms, HRT, GSM, bone health, cardiovascular, cognitive, sleep, mood, workplace)
- ChromaDB vector store persistence
- OpenAI embeddings for semantic indexing
- **@traceable decorators** on `get_retriever()` and `search()` methods for LangSmith observability
- Semantic search with configurable k (default: 3 documents)
- Support for custom document ingestion from `documents/` directory

## LangSmith Integration

All LLM calls and retrieval operations are automatically traced via `@traceable` decorators in LangSmith:

**Traced Components:**
- `menopause_health_navigator_query` (chain): Full query execution pipeline
- `get_menopause_retriever` (chain): Retriever initialization
- `search_knowledge_base` (retriever): Document search operations

**Capabilities:**
- Monitor query performance and latency
- Track token usage and costs
- Debug retrieval quality and relevance scores
- Analyze confidence levels and doctor referral patterns
- View conversation patterns across test suite runs

**Access Traces:**
After running the test suite, view traces at:
https://smith.langchain.com/projects/femcare-health-navigator

## 13 Test Queries

The test suite (default mode) runs these menopause health queries:
1. What are the first signs of perimenopause?
2. Why are my periods becoming irregular?
3. Can I still get pregnant during perimenopause?
4. What causes hot flashes and night sweats?
5. Why do I feel anxious or have brain fog?
6. Should I start HRT? What are the risks vs benefits for me?
7. How do I know if I've reached menopause?
8. Why can't I sleep anymore?
9. What are non-hormonal options for hot flashes?
10. Why am I gaining weight and what can I do?
11. I have a family history of breast cancer — is HRT safe for me?
12. Why do I feel depressed or have mood swings?
13. What does postmenopause mean exactly?

## Development

### Adding Custom Prompts

Edit the `prompt_template` in `rag_pipeline.py` to customize the system prompt and answer format.

### Changing the LLM Model

Modify the `model_name` parameter in the `RAGPipeline.__init__()` method.

### Adjusting Retrieval Parameters

In `rag_pipeline.py`, modify the `search_kwargs={"k": 3}` to change the number of retrieved documents.

## System Prompt

The application uses a comprehensive system prompt that:
- Identifies as "Femcare Health Navigator, a menopause health companion"
- Restricts responses to menopause-related medical context
- Requires source citation for all information
- Defers to healthcare providers when not confident
- Never provides diagnoses
- Contextualizes HRT guidance regarding WHI study evolution
- Acknowledges individual risk profile variation

## Confidence Scoring & Doctor Referral

The system automatically:
1. **Calculates relevance scores** for each retrieved document (0-1 scale)
2. **Averages scores** across the 3 retrieved documents
3. **Flags low confidence** when average score < 0.7
4. **Appends doctor referral recommendation** to answers with low confidence
5. **Returns flags** in response: `confidence: "high"|"low"`, `referred_to_doctor: bool`

## Troubleshooting

- **Missing API keys**: Ensure `.env` file exists with `OPENAI_API_KEY` and `LANGCHAIN_API_KEY`
- **LangSmith traces not appearing**: Verify `LANGCHAIN_API_KEY` is valid and `LANGCHAIN_PROJECT` is set to `menopause-health-navigator`
- **Vector store errors**: Delete the `./femcare_chroma_db/` directory to reset the database
- **Low confidence responses**: Indicates retrieved documents were weakly relevant; consider rephrasing the question or consulting a healthcare provider
- **No LangSmith dashboard link available**: Ensure `LANGCHAIN_PROJECT` environment variable matches the expected project name

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions about LangChain, visit: https://python.langchain.com/
For LangSmith documentation, visit: https://docs.smith.langchain.com/
