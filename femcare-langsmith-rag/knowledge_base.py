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
            "title": "PCOS Symptoms and Management",
            "content": "Polycystic Ovary Syndrome (PCOS) is a common endocrine disorder affecting women of reproductive age, characterized by irregular menstrual cycles, elevated androgens, and polycystic ovarian morphology. Symptoms include hirsutism, acne, hair loss, weight gain, and subfertility. Management focuses on lifestyle modifications including weight loss and regular exercise, combined with medications such as metformin for metabolic improvement and oral contraceptives or spironolactone for hormonal regulation. Insulin resistance is a key feature in up to 70% of PCOS cases, making dietary management particularly important. [Source: WHO]"
        },
        {
            "title": "Endometriosis Diagnosis and Treatment",
            "content": "Endometriosis is a chronic condition characterized by the presence of endometrial tissue outside the uterus, affecting 5-10% of women in their reproductive years. The condition causes severe pelvic pain, dysmenorrhea, and infertility. Diagnosis is confirmed through laparoscopy, though MRI can be helpful for assessment of deep infiltrating disease. Treatment options include NSAIDs for pain management, combined hormonal contraceptives, progestins, and GnRH agonists for symptom relief and disease suppression. Surgical intervention may be necessary for advanced cases or assisted reproduction. [Source: EMA]"
        },
        {
            "title": "Perimenopause Signs and Management",
            "content": "Perimenopause is the transition phase to menopause, typically lasting 4-10 years, during which estrogen and progesterone levels fluctuate significantly. Common symptoms include irregular menstrual cycles, hot flashes, night sweats, mood changes, and sleep disturbances. FSH testing can support diagnosis, though clinical history is often sufficient given irregular cycles. Management includes hormone therapy (HT) for symptom relief, lifestyle modifications, regular exercise, and cognitive behavioral therapy. Non-hormonal options like SSRIs and SNRIs are available for women who cannot tolerate or prefer to avoid HT. [Source: PubMed]"
        },
        {
            "title": "Menstrual Cycle Irregularities",
            "content": "Menstrual irregularities can manifest as amenorrhea, oligomenorrhea, polymenorrhea, or menorrhagia, with causes ranging from hormonal disorders to structural abnormalities. Initial evaluation includes assessment of pregnancy status, thyroid function, prolactin levels, and pelvic imaging. Polycystic ovaries, uterine fibroids, and thyroid disorders are among the most common etiologies. Treatment depends on the underlying cause and patient preferences, ranging from observation and lifestyle changes to hormonal therapy, NSAIDs for heavy bleeding, or surgical intervention. Proper diagnosis is essential as some irregularities indicate serious underlying conditions. [Source: PubMed]"
        },
        {
            "title": "Iron Deficiency Anemia in Women",
            "content": "Iron deficiency anemia is particularly prevalent in women of reproductive age due to menstrual blood loss, with a prevalence of 10-20% in non-pregnant women. Common symptoms include fatigue, shortness of breath, pale skin, and weakened immune function. Diagnosis requires measurement of serum iron, ferritin, and total iron-binding capacity, with transferrin saturation below 20% indicating iron deficiency. Treatment consists of oral iron supplementation (ferrous sulfate 325 mg daily) or intravenous iron for severe cases, alongside identification and management of the underlying cause. Heavy menstrual bleeding should be evaluated and treated to prevent recurrence. [Source: WHO]"
        },
        {
            "title": "Hormonal Contraception Effects and Considerations",
            "content": "Combined oral contraceptives containing ethinyl estradiol and progestins effectively prevent pregnancy while providing additional benefits including cycle regulation and acne improvement. Estrogen exposure carries a small but increased risk of venous thromboembolism, particularly in women over 35 who smoke. Progesterone-only methods like the mini-pill and implants are alternatives for women who cannot tolerate estrogen. Long-acting reversible contraceptives (IUDs and implants) offer excellent efficacy with minimal systemic effects. Individual assessment is crucial, as contraceptive choice depends on medical history, side effect profile tolerance, and personal preferences. [Source: EMA]"
        },
        {
            "title": "Thyroid Conditions in Women",
            "content": "Autoimmune thyroid disease, particularly Hashimoto's thyroiditis, is 5-8 times more common in women than men, often presenting with hypothyroidism. Symptoms include fatigue, weight gain, cold intolerance, and hair loss, with diagnosis confirmed by elevated TSH and anti-TPO antibodies. Hypothyroidism is treated with levothyroxine replacement, with dose adjusted to maintain TSH in the target range based on individual patient factors. Hyperthyroidism, often from Graves' disease, requires antithyroid drugs, beta-blockers, or radioactive iodine. Regular monitoring is essential, particularly in women of reproductive age and during pregnancy, as thyroid disorders can affect fertility and fetal development. [Source: PubMed]"
        },
        {
            "title": "Fertility and Menstrual Cycle Tracking",
            "content": "Understanding the menstrual cycle is fundamental for fertility awareness and conception planning. The typical 28-day cycle comprises the follicular phase (days 1-14), ovulation (day 14), and luteal phase (days 15-28), with ovulation occurring approximately 14 days before the next menstrual period. Ovulation can be detected through basal body temperature tracking, cervical mucus changes, or LH surge detection with ovulation predictor kits. For women seeking pregnancy, timing intercourse during the fertile window (5 days before and day of ovulation) maximizes conception chances. Irregular cycles may indicate anovulation or other fertility issues requiring medical evaluation. [Source: WHO]"
        },
        {
            "title": "Hormonal Balance and Women's Health",
            "content": "Hormonal balance is critical for maintaining reproductive health, bone density, cardiovascular function, and psychological well-being in women. Estrogen and progesterone regulate not only the menstrual cycle but also skin, bone, and cardiovascular health throughout a woman's lifespan. Hormonal imbalances can result from thyroid dysfunction, adrenal insufficiency, PCOS, or premature ovarian insufficiency. Assessment typically includes measurement of FSH, LH, estradiol, progesterone, and testosterone levels. Management addresses the underlying cause through lifestyle modifications, hormonal therapy, or treatment of specific conditions affecting hormone regulation. [Source: PubMed]"
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

    def get_retriever(self, k: int = 3):
        """
        Get a LangChain retriever for the knowledge base.

        Args:
            k: Number of documents to retrieve (default: 3)

        Returns:
            LangChain retriever with semantic search capabilities
        """
        return self.vector_store.as_retriever(search_kwargs={"k": k})

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
