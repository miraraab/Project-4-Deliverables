"""
Knowledge Base management using Chroma vector database.
Handles document ingestion, embedding, and retrieval.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langsmith import traceable

load_dotenv()


class KnowledgeBase:
    def __init__(self, persist_directory="./chroma_db", documents_directory="./documents"):
        self.persist_directory = persist_directory
        self.documents_directory = documents_directory
        self.embeddings = OpenAIEmbeddings()

        Path(persist_directory).mkdir(parents=True, exist_ok=True)

        self.vector_store = None
        self._initialize_vector_store()

    def _initialize_vector_store(self):
        """Initialize or load the vector store."""
        if os.path.exists(os.path.join(self.persist_directory, "chroma.sqlite3")):
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        else:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )

    def load_documents_from_directory(self):
        """Load documents from the documents directory."""
        if not os.path.exists(self.documents_directory):
            os.makedirs(self.documents_directory)
            print(f"Created documents directory at {self.documents_directory}")
            return []

        loader = DirectoryLoader(
            self.documents_directory,
            glob="**/*.txt",
            loader_cls=TextLoader
        )

        documents = loader.load()
        return documents

    def ingest_documents(self):
        """Load and ingest documents into the vector store."""
        documents = self.load_documents_from_directory()

        if not documents:
            print("No documents found to ingest.")
            return

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = text_splitter.split_documents(documents)

        self.vector_store.add_documents(chunks)
        print(f"Successfully ingested {len(chunks)} document chunks.")

    def get_vector_store(self):
        """Get the vector store instance."""
        return self.vector_store

    def search(self, query: str, k: int = 3):
        """
        Search the knowledge base for relevant documents.

        Args:
            query: The search query
            k: Number of results to return

        Returns:
            List of relevant documents
        """
        return self.vector_store.similarity_search(query, k=k)


class FemcareKnowledgeBase:
    """
    Specialized knowledge base for women's health topics.
    Contains curated medical documents and provides retrieval capabilities.
    """

    SAMPLE_DOCUMENTS = [
        {
            "title": "Hot Flushes and Night Sweats",
            "content": "Hot flushes affect about 8 in 10 women during menopause and are caused by falling estrogen levels affecting your body's temperature control center. You may feel sudden intense heat in your face, neck, and chest, often followed by heavy sweating and chills that can last 2-10 minutes. Common triggers include caffeine, alcohol, spicy foods, stress, and warm environments. Treatment options include hormone therapy (which works for 75-90% of women), lifestyle changes like dressing in layers and staying cool, or non-hormonal medications like SSRIs or gabapentin if you prefer to avoid hormones. [Source: WHO]"
        },
        {
            "title": "Hormone Replacement Therapy (HRT)",
            "content": "Hormone replacement therapy uses estrogen and/or progesterone to relieve menopause symptoms and comes in many forms including tablets, patches, creams, and rings. HRT is very effective for hot flushes, night sweats, vaginal dryness, and mood changes, with most women noticing improvement within weeks. Concerns from older studies about breast cancer and heart disease have been clarified by newer research—HRT is considered safe for most women when started early in menopause and doesn't increase breast cancer risk with estrogen-only therapy. Current medical guidelines recommend discussing HRT individually with your doctor to decide if it's right for you based on your symptoms and medical history. [Source: WHO 2023, DGGG]"
        },
        {
            "title": "Vaginal Dryness and Urinary Problems",
            "content": "About 1 in 3 menopausal women experience vaginal dryness, irritation, or painful intercourse because falling estrogen levels thin the vaginal tissue and reduce natural moisture. Urinary symptoms like frequent urination, urgency, or discomfort are also common due to changes in the urinary tract tissues. These symptoms can significantly affect sexual function and quality of life, but they respond well to treatment. Non-hormonal options include vaginal moisturizers and lubricants, while hormonal treatments include vaginal estrogen creams or tablets with very minimal systemic absorption, or systemic HRT if you're already taking it for other symptoms. [Source: DGGG]"
        },
        {
            "title": "Protecting Your Bone Health",
            "content": "During menopause, bone loss accelerates due to falling estrogen levels, putting you at increased risk of osteoporosis and fractures, especially in the first 5-8 years after your last period. One in three women over age 50 develops osteoporosis, which weakens bones and increases fracture risk. Prevention includes getting enough calcium (1000-1200 mg daily from diet or supplements), vitamin D (800-2000 IU daily), regular weight-bearing exercise like walking or strength training, and quitting smoking. A bone density scan (DXA) can check your bone health, and if needed, medications like bisphosphonates can help slow bone loss. [Source: PubMed, WHO]"
        },
        {
            "title": "Heart Health and Menopause",
            "content": "Before menopause, women have lower risk of heart disease than men, but this protection decreases after menopause as estrogen levels drop. After menopause, your cholesterol and blood pressure may increase, and your risk for heart disease rises significantly. To protect your heart, exercise regularly (150 minutes per week), eat a healthy diet, maintain a healthy weight, manage stress, and don't smoke. Talk to your doctor about checking your cholesterol and blood pressure regularly, especially if you have other risk factors like family history or diabetes. [Source: WHO, EMA]"
        },
        {
            "title": "Managing Brain Fog and Memory Changes",
            "content": "About half of menopausal women report difficulty concentrating, memory problems, or 'brain fog' that can affect work and daily life. These changes are usually temporary and related to sleep disruption from night sweats and hormonal changes affecting your brain chemistry. You're not at higher risk of Alzheimer's disease just from menopause, though good brain health practices help—stay mentally active, exercise regularly, eat a healthy diet, get adequate sleep, and manage stress. If your cognitive symptoms are severe or getting worse, talk to your doctor about other possible causes. [Source: PubMed, NAMS]"
        },
        {
            "title": "Better Sleep During Menopause",
            "content": "Sleep problems affect 4 in 10 menopausal women and are often caused by night sweats waking you up, hormonal changes affecting your sleep cycle, or anxiety. Getting better sleep is essential because poor sleep worsens other menopause symptoms, affects mood and concentration, and increases health risks. Helpful strategies include keeping your bedroom cool and dark, maintaining a regular sleep schedule, avoiding caffeine and alcohol, doing relaxation exercises, and regular exercise (but not right before bed). If night sweats are causing your sleep problems, treating the hot flushes with HRT or other medications often improves sleep significantly. [Source: NAMS, PubMed]"
        },
        {
            "title": "Mood Changes, Anxiety, and Depression",
            "content": "Depression and anxiety are more common during perimenopause, affecting about 1 in 10 women, and can be triggered or worsened by menopause-related hormonal changes and sleep disruption. You may feel persistent sadness, worry, loss of interest in activities you enjoy, or anxiety that wasn't there before. Regular exercise, good sleep, stress management, talking to a therapist, and treating hot flushes (which worsen mood symptoms) all help. Some antidepressants like paroxetine or venlafaxine work well for both depression and hot flushes, or HRT may help if you also have vasomotor symptoms. [Source: DGGG, PubMed]"
        },
        {
            "title": "Menopause at Work",
            "content": "Nearly half of working women report that menopause symptoms affect their job performance, concentration, or attendance. In Germany and EU countries, employers are legally required to provide reasonable adjustments if menopause symptoms significantly impact your work. Reasonable adjustments might include flexible hours, remote work options, temperature control (like positioning near windows or using fans), access to rest areas, or adjusted break times. You can discuss specific symptoms and needs with your HR department or occupational health service without sharing all details. Knowing your legal rights and documenting how symptoms affect your work helps when requesting accommodations. [Source: DGGG, EU Occupational Health Guidelines]"
        }
    ]

    def __init__(self, persist_directory="./femcare_chroma_db"):
        """
        Initialize the FemCare knowledge base with sample documents.

        Args:
            persist_directory: Path to persist Chroma database
        """
        self.persist_directory = persist_directory
        Path(persist_directory).mkdir(parents=True, exist_ok=True)

        self.embeddings = OpenAIEmbeddings()
        self.vector_store = self._initialize_vector_store()

    def _initialize_vector_store(self):
        """Initialize Chroma vector store and load sample documents."""
        vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="femcare_docs"
        )

        if vector_store._collection.count() == 0:
            self._load_sample_documents(vector_store)

        return vector_store

    def _load_sample_documents(self, vector_store):
        """Load sample medical documents into the vector store."""
        documents = [
            Document(
                page_content=doc["content"],
                metadata={"title": doc["title"], "source": "FemCare Knowledge Base"}
            )
            for doc in self.SAMPLE_DOCUMENTS
        ]

        vector_store.add_documents(documents)
        print(f"Loaded {len(documents)} sample medical documents into knowledge base.")

    @traceable(name="get_menopause_retriever", run_type="chain")
    def get_retriever(self, k: int = 3):
        """
        Get a LangChain retriever for the knowledge base.

        Args:
            k: Number of documents to retrieve (default: 3)

        Returns:
            LangChain retriever with semantic search capabilities
        """
        return self.vector_store.as_retriever(search_kwargs={"k": k})

    @traceable(name="search_knowledge_base", run_type="retriever")
    def search(self, query: str, k: int = 3):
        """
        Search the knowledge base for relevant documents.

        Args:
            query: The search query
            k: Number of results to return

        Returns:
            List of relevant documents
        """
        return self.vector_store.similarity_search(query, k=k)
