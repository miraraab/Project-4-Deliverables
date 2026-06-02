import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

load_dotenv()


class FemcareKnowledgeBase:
    """Knowledge base for women's health information using ChromaDB and OpenAI embeddings."""

    MEDICAL_DOCUMENTS = [
        """
        PCOS (Polycystic Ovary Syndrome) is characterized by elevated androgen levels, ovulatory dysfunction, and polycystic ovarian morphology.
        Common symptoms include irregular menstrual cycles, acne, hirsutism, and weight gain. Management involves lifestyle modifications including
        regular exercise and balanced nutrition, along with pharmacological interventions such as metformin or hormonal contraceptives. Insulin
        resistance is present in approximately 70% of cases and requires monitoring through glucose and lipid profiles. [Source: WHO]
        """,

        """
        Endometriosis is a chronic condition where endometrial-like tissue grows outside the uterus, causing pain and infertility. Diagnosis
        typically requires imaging studies (ultrasound or MRI) and may involve laparoscopy for confirmation. Symptoms include dysmenorrhea,
        dyspareunia, and chronic pelvic pain that worsens during menstruation. Treatment options range from NSAIDs and hormonal contraceptives
        to GnRH agonists or surgical excision depending on severity and fertility goals. [Source: EMA]
        """,

        """
        Perimenopause is the transition phase preceding menopause, typically lasting 4-10 years, characterized by fluctuating estrogen and
        progesterone levels. Common signs include hot flashes, night sweats, mood changes, sleep disturbances, and irregular menstrual patterns.
        Bone density decline accelerates during this period, increasing fracture risk. Management includes lifestyle modifications, hormone
        therapy consideration, and monitoring for metabolic changes through regular health assessments. [Source: PubMed]
        """,

        """
        Menstrual cycle irregularities can result from hormonal imbalances, stress, excessive exercise, or underlying medical conditions such as
        thyroid disorders or PCOS. A normal cycle ranges from 21-35 days with variations considered normal. Amenorrhea (absence of periods) or
        polymenorrhea (frequent periods) warrants investigation including FSH, LH, and prolactin levels. Tracking cycle length and symptoms helps
        clinicians identify patterns and underlying causes. [Source: PubMed]
        """,

        """
        Iron deficiency in women is the most common micronutrient deficiency globally, often resulting from heavy menstrual bleeding, pregnancy,
        or inadequate dietary intake. Symptoms include fatigue, weakness, shortness of breath, and impaired cognitive function. Women of reproductive
        age require 18mg of iron daily, increasing to 27mg during pregnancy. Diagnosis involves serum ferritin and hemoglobin testing, with treatment
        including iron supplementation and dietary modification alongside addressing underlying causes of bleeding. [Source: WHO]
        """,

        """
        Hormonal contraceptives containing estrogen and progestin work by suppressing ovulation and altering cervical mucus. Common side effects
        include nausea, breast tenderness, and mood changes, typically resolving within 2-3 months. Benefits extend beyond contraception, including
        reduced menstrual bleeding, decreased acne, and relief from PCOS symptoms. However, increased risk of venous thromboembolism requires
        careful assessment of personal and family history, particularly in women over 35 who smoke. [Source: EMA]
        """,

        """
        Thyroid conditions in women are three times more common than in men due to hormonal influences. Hypothyroidism can cause irregular periods,
        weight gain, and reduced fertility, while hyperthyroidism may lead to lighter periods and increased menstrual irregularity. TSH screening is
        recommended during preconception counseling and pregnancy. Levothyroxine dosing requires periodic adjustment based on TSH levels, particularly
        during menstrual cycle fluctuations and pregnancy. [Source: PubMed]
        """,

        """
        Fertility and cycle tracking involves monitoring basal body temperature, cervical mucus consistency, and cycle length to predict ovulation.
        The fertile window typically occurs 5 days before ovulation and the day of ovulation itself. Ovulation generally occurs 12-16 days before
        the next menstrual period, though this varies among individuals. Tracking methods are useful for both conception attempts and contraception,
        with effectiveness improving when combined with awareness of other ovulation indicators like LH surge detection. [Source: WHO]
        """
    ]

    def __init__(self):
        """Initialize the knowledge base with ChromaDB and OpenAI embeddings."""
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Convert strings to Document objects
        documents = [
            Document(page_content=doc.strip(), metadata={"topic": topic})
            for doc, topic in zip(
                self.MEDICAL_DOCUMENTS,
                [
                    "PCOS",
                    "Endometriosis",
                    "Perimenopause",
                    "Menstrual Cycle",
                    "Iron Deficiency",
                    "Hormonal Contraception",
                    "Thyroid Conditions",
                    "Fertility and Cycle Tracking"
                ]
            )
        ]

        # Create ChromaDB vector store
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name="femcare_health"
        )

    def get_retriever(self):
        """Return a LangChain retriever with k=3 for document retrieval."""
        return self.vector_store.as_retriever(search_kwargs={"k": 3})
