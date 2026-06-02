"""
RAG Pipeline implementation using LangChain and LangSmith.
Combines a vector database with an LLM for retrieval-augmented generation.
"""
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langsmith import traceable
from knowledge_base import FemcareKnowledgeBase

load_dotenv()


class RAGPipeline:
    def __init__(self, model_name="gpt-4o-mini", temperature=0.7):
        self.model_name = model_name
        self.temperature = temperature

        self.embeddings = OpenAIEmbeddings()

        self.knowledge_base = FemcareKnowledgeBase()
        self.vector_store = self.knowledge_base.vector_store

        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature
        )

        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are Femcare Health Navigator, a menopause health companion supporting women through perimenopause, menopause, and postmenopause. You answer questions using only the provided medical context, which covers topics including vasomotor symptoms (hot flushes, night sweats), HRT options and safety, genitourinary syndrome of menopause (GSM), bone health, cardiovascular risk, cognitive changes, sleep disruption, mood and mental health, and workplace menopause rights.

Always cite your sources. If you are not confident in the answer based on the context, respond with: "I recommend discussing this with your doctor or a menopause specialist" and provide a brief reason why. Never provide a diagnosis. Never claim to replace a medical professional. When discussing HRT, always acknowledge that individual risk profiles vary and that guidance has evolved significantly since the 2002 WHI study.

Context:
{context}

Question: {question}

Answer:"""
        )

        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

    @traceable(name="menopause_health_navigator_query", run_type="chain")
    def query(self, user_input: str) -> dict:
        """
        Query the RAG pipeline with a user question.

        Args:
            user_input: The user's question about menopause health

        Returns:
            Dictionary with:
                - answer (str): The health information response
                - sources (list): List of document sources cited
                - confidence (str): "high" or "low" confidence level
                - referred_to_doctor (bool): True if user should consult a healthcare provider
        """
        try:
            docs_with_scores = self.vector_store.similarity_search_with_scores(user_input, k=3)
            relevance_scores = [score for _, score in docs_with_scores]
            docs = [doc for doc, _ in docs_with_scores]
        except AttributeError:
            docs = self.vector_store.similarity_search(user_input, k=3)
            relevance_scores = [0.75] * len(docs)

        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0

        is_low_confidence = avg_relevance < 0.7
        confidence_level = "low" if is_low_confidence else "high"

        context_text = "\n\n".join([doc.page_content for doc in docs])

        prompt = self.prompt_template.format(context=context_text, question=user_input)
        answer = self.llm.invoke(prompt).content

        sources = [doc.metadata.get("source", "Unknown") for doc in docs]

        if is_low_confidence:
            answer += "\n\n⚠️ Low Confidence Response: For personalised menopause care, consider speaking with a menopause specialist or your GP."

        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence_level,
            "referred_to_doctor": is_low_confidence
        }
