"""
RAG Pipeline implementation using LangChain and LangSmith.
Combines a vector database with an LLM for retrieval-augmented generation.
"""
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from knowledge_base import KnowledgeBase


class RAGPipeline:
    def __init__(self, model_name="gpt-4", temperature=0.7):
        self.model_name = model_name
        self.temperature = temperature

        self.embeddings = OpenAIEmbeddings()

        self.knowledge_base = KnowledgeBase()
        self.vector_store = self.knowledge_base.get_vector_store()

        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature
        )

        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a helpful health information assistant for femcare-related questions.
Use the provided context to answer the user's question accurately and helpfully.

Context:
{context}

Question: {question}

Answer:"""
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt_template}
        )

    def query(self, question: str) -> dict:
        """
        Query the RAG pipeline with a question.

        Args:
            question: The user's question

        Returns:
            Dictionary with 'answer' and 'sources' keys
        """
        result = self.qa_chain.invoke({"query": question})

        sources = [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]

        return {
            "answer": result["result"],
            "sources": sources
        }
