# Menopause Health Navigator - LangSmith RAG

A Retrieval-Augmented Generation (RAG) application for comprehensive menopause health information, built with LangChain and integrated with LangSmith for observability and tracing.

## Features

- **Menopause-Focused Knowledge Base**: Comprehensive coverage of vasomotor symptoms, HRT, bone health, cardiovascular changes, and workplace considerations
- **Retrieval-Augmented Generation**: Combines a vector database with GPT-4 for accurate, evidence-based menopause health information
- **LangSmith Integration**: Full observability and tracing of all LLM calls and retrieval operations
- **Vector Database**: Uses Chroma for efficient semantic search
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

```bash
python main.py
```

The application will start an interactive prompt where you can ask menopause-related health questions. The knowledge base includes evidence-based medical information on vasomotor symptoms, hormone replacement therapy, bone health, cardiovascular changes, cognitive symptoms, sleep disruption, mood changes, and workplace considerations.

### Loading Documents

1. Create a `documents/` directory in the project root
2. Add your `.txt` files to the `documents/` directory
3. In your Python code or a script, use:
   ```python
   from knowledge_base import KnowledgeBase
   kb = KnowledgeBase()
   kb.ingest_documents()
   ```

### Querying the RAG Pipeline

```python
from rag_pipeline import RAGPipeline

pipeline = RAGPipeline()
result = pipeline.query("Your health-related question here")
print(result["answer"])
print(result["sources"])
```

## Components

### main.py
Entry point that provides an interactive command-line interface for querying the RAG system.

### rag_pipeline.py
Implements the RAG pipeline using:
- OpenAI embeddings for semantic understanding
- Chroma vector store for document retrieval
- GPT-4 LLM for answer generation
- LangSmith for full observability

### knowledge_base.py
Manages the vector database:
- Document loading from the `documents/` directory
- Text chunking and embedding
- Chroma vector store persistence
- Semantic search capabilities

## LangSmith Integration

All LLM calls and retrieval operations are automatically traced in LangSmith. You can:
- Monitor query performance and latency
- Track token usage and costs
- Debug retrieval quality
- Analyze conversation patterns

Access your traces at: https://eu.smith.langchain.com/o/b1b7036f-bc62-4cd5-b9ee-3bc5f9a32a03

## Development

### Adding Custom Prompts

Edit the `prompt_template` in `rag_pipeline.py` to customize the system prompt and answer format.

### Changing the LLM Model

Modify the `model_name` parameter in the `RAGPipeline.__init__()` method.

### Adjusting Retrieval Parameters

In `rag_pipeline.py`, modify the `search_kwargs={"k": 3}` to change the number of retrieved documents.

## Troubleshooting

- **Missing API keys**: Ensure `.env` file exists and contains valid API keys
- **No documents found**: Create a `documents/` directory and add `.txt` files
- **Vector store errors**: Delete the `chroma_db/` directory to reset the database

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions about LangChain, visit: https://python.langchain.com/
For LangSmith documentation, visit: https://docs.smith.langchain.com/
