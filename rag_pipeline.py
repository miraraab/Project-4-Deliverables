import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langsmith.run_helpers import traceable
from knowledge_base import FemcareKnowledgeBase

load_dotenv()


class FemcareRAGPipeline:
    """RAG pipeline for women's health Q&A with LangSmith tracing."""

    def __init__(self):
        """Initialize the RAG pipeline with knowledge base and LLM."""
        # Load knowledge base and retriever
        self.kb = FemcareKnowledgeBase()
        self.retriever = self.kb.get_retriever()

        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0
        )

        # Define system prompt
        system_prompt = """You are Femcare Health Navigator, a women's health companion. You answer questions using only the provided medical context. Always cite your sources. If you are not confident in the answer based on the context, respond with: 'I recommend discussing this with your doctor' and provide a brief reason why. Never provide a diagnosis. Never claim to replace a medical professional."""

        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", """Based on the following medical context, answer the user's question.

Context:
{context}

Question: {question}""")
        ])

        # Build LCEL chain: retriever → format docs → prompt → LLM → parser
        def format_docs(docs):
            return "\n\n".join([doc.page_content for doc in docs])

        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    @traceable
    def _execute_rag_chain(self, user_input: str) -> str:
        """Execute the RAG chain with LangSmith tracing."""
        answer = self.chain.invoke(user_input)
        return answer

    @traceable
    def _check_confidence(self, user_input: str) -> tuple[float, list]:
        """Check relevance scores of retrieved documents and return confidence level."""
        docs_with_scores = self.kb.vector_store.similarity_search_with_score(user_input, k=3)

        if not docs_with_scores:
            return 0.0, []

        scores = [score for _, score in docs_with_scores]
        return min(scores), scores

    @traceable
    def query(self, user_input: str) -> dict:
        """
        Process user query and return answer with sources and confidence.

        Args:
            user_input: The user's health-related question

        Returns:
            dict with keys:
                - answer: The generated response with sources cited
                - sources: List of relevant medical topics
                - confidence: "high" or "low"
                - referred_to_doctor: bool indicating if low confidence triggered referral
        """
        # Retrieve documents and get their metadata
        docs = self.retriever.invoke(user_input)

        # Generate answer using the RAG chain
        answer = self._execute_rag_chain(user_input)

        # Check confidence based on relevance scores
        min_score, scores = self._check_confidence(user_input)
        confidence = "high"
        referred_to_doctor = False

        if min_score < 0.7:
            confidence = "low"
            answer += "\n\n⚠️ **Low Confidence**: The available information may not fully address your question. I recommend discussing this with your doctor."
            referred_to_doctor = True

        # Extract sources from document metadata
        sources = []
        for doc in docs:
            topic = doc.metadata.get("topic", "Unknown")
            if topic not in sources:
                sources.append(topic)

        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence,
            "referred_to_doctor": referred_to_doctor
        }
