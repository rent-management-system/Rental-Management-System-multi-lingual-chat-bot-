import json
from typing import List
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sentence_transformers import SentenceTransformer
import os

# Hardcoded knowledge base content
# --- translation.json (Amharic) ---
AMHARIC_TRANSLATION_JSON = {
  "home": "መነሻ",
  "about": "ስለ እኛ",
  "contact": "እኛን ያግኙን",
  "services": "አገልግሎቶች",
  "properties": "ንብረቶች",
  "login": "ግባ",
  "register": "ይመዝገቡ",
  "search": "ፈልግ",
  "rent": "ኪራይ",
  "buy": "ግዛ",
  "sell": "ሽጥ",
  "faq": "ተደጋጋሚ ጥያቄዎች",
  "terms": "ውሎች እና ሁኔታዎች",
  "privacy": "ግላዊነት መመሪያ",
  "dashboard": "ዳሽቦርድ",
  "profile": "መገለጫ",
  "logout": "ውጣ",
  "welcome": "እንኳን ደህና መጡ",
  "description": "ይህ የኪራይ አስተዳደር ስርዓት ነው።",
  "address": "አድራሻ",
  "phone": "ስልክ",
  "email": "ኢሜይል"
}

# --- translation copy.json (English) ---
ENGLISH_TRANSLATION_JSON = {
  "home": "Home",
  "about": "About Us",
  "contact": "Contact Us",
  "services": "Services",
  "properties": "Properties",
  "login": "Login",
  "register": "Register",
  "search": "Search",
  "rent": "Rent",
  "buy": "Buy",
  "sell": "Sell",
  "faq": "FAQ",
  "terms": "Terms and Conditions",
  "privacy": "Privacy Policy",
  "dashboard": "Dashboard",
  "profile": "Profile",
  "logout": "Logout",
  "welcome": "Welcome",
  "description": "This is a rental management system.",
  "address": "Address",
  "phone": "Phone",
  "email": "Email"
}

# --- translation copy 2.json (Afaan Oromo) ---
AFAAN_OROMO_TRANSLATION_JSON = {
  "home": "Mana",
  "about": "Waa'ee Keenya",
  "contact": "Nu Qunnamuuf",
  "services": "Tajaajiloota",
  "properties": "Qabeenya",
  "login": "Seeni",
  "register": "Galmaa'i",
  "search": "Barbaadi",
  "rent": "Kireeffadhu",
  "buy": "Biti",
  "sell": "Gurguri",
  "faq": "Gaaffiiwwan Yeroo Baay'ee Gaafatamani",
  "terms": "Haalawwan fi Ulaagaalee",
  "privacy": "Imaammata Iccitii",
  "dashboard": "Daashboordii",
  "profile": "Profaayilii",
  "logout": "Ba'i",
  "welcome": "Nagaa Gali",
  "description": "Kun sirna bulchiinsa kiraayaati.",
  "address": "Teessoo",
  "phone": "Bilbila",
  "email": "Imeelii"
}

# --- Faq.txt ---
FAQ_TEXT = """
FAQ – Frequently Asked Questions

Q1: What property types can I list or search for?
A1: You can list and search for various property types including apartments, houses, condos, commercial spaces, and land.

Q2: How do I register as a new user?
A2: Click on the "Register" link in the navigation bar, fill out the required information, and submit the form. You will receive a confirmation email.

Q3: Can I manage multiple properties under one account?
A3: Yes, our system allows you to manage multiple properties efficiently from your dashboard.

Q4: What payment methods are accepted for rent?
A4: We accept various payment methods including bank transfers, credit/debit cards, and mobile money. Specific options may vary by region.

Q5: Is there a fee for listing a property?
A5: Listing fees vary based on the type of property and the duration of the listing. Please refer to our "Services" page for detailed pricing.

Q6: How can I contact customer support?
A6: You can contact customer support via email at support@rentalmgmt.com or by calling our hotline at +251-912-345678 during business hours.

Q7: What if I forget my password?
A7: Click on the "Forgot Password" link on the login page and follow the instructions to reset your password.

Q8: Are there any restrictions on property listings?
A8: All properties must comply with local housing regulations and our terms of service. Illegal or fraudulent listings are strictly prohibited.

Q9: How do I update my profile information?
A9: Log in to your account, navigate to the "Profile" section in your dashboard, and you can edit your personal details there.

Q10: Can I get notifications for new properties matching my criteria?
A10: Yes, you can set up email notifications for new listings that match your saved search criteria in your dashboard settings.
"""

# --- Final project 1-4 final.docx (Summarized content) ---
# NOTE: In a real scenario, python-docx would be used to extract full text.
# For this exercise, a representative summary is used as per instructions.
DOCX_SUMMARY_TEXT = """
=== RENTAL MANAGEMENT SYSTEM – FULL PROJECT SUMMARY ===

The Rental Management System (RMS) is a final-year Computer Science project developed by five Unity University students at Adama Campus (2024/2025 academic year):

• Abenezer Ayele (ID: 04605/14)
• Dagmawi Teferi (ID: 04606/14)
• Henok Tesfaye (ID: 04583/14)
• Kaleb Worku (ID: 04534/14)
• Nehmya Biruk (ID: 04601/14)

**Project Goal**: Build a modern, affordable, and fully multilingual web platform that connects landlords and tenants in Ethiopia without expensive brokers.

**Key Features**:
• Pay-per-post model – landlords pay only once to list a property (no monthly subscription)
• 100% FREE search for tenants
• Supports three languages: English, Amharic, Afaan Oromo
• High-quality photos + map view (OpenStreetMap)
• Direct messaging & phone call to landlords
• Secure application system with document upload
• Responsive design – works on mobile and desktop

**Three Simple Steps for Tenants**:
1. Sign up / Log in → Search homes by location, price, bedrooms
2. Contact owner → Submit application + documents
3. Move in → Use platform to report issues or leave reviews

**Developer Roles & Contributions**:
• Abenezer Ayele – Backend API, FastAPI, LangGraph RAG Chatbot
• Dagmawi Teferi – Frontend UI/UX (React + Tailwind), multilingual design
• Henok Tesfaye – Database design (PostgreSQL + JSONB), authentication
• Kaleb Worku – Payment integration, property listing logic
• Nehmya Biruk – Map integration, testing, deployment (Render)

**Technology Stack (MERN + AI)**:
• Frontend: React.js, Tailwind CSS
• Backend: FastAPI (Python)
• Database: PostgreSQL with JSONB for flexible property data
• AI Chatbot: Google Gemini 2.0 Flash + LangGraph + FAISS vector store
• Embeddings: paraphrase-multilingual-MiniLM-L12-v2 (supports Amharic & Oromo)
• Deployment: Render.com (free tier)
• Maps: OpenStreetMap API

**Chapter 1 – Introduction**
The rental market in Ethiopia suffers from high broker fees and outdated processes. This project replaces brokers with a digital platform that saves landlords 30%+ on advertising and gives tenants free access.

**Chapter 2 – Objectives**
General: Transform Ethiopia’s rental industry
Specific:
• Reduce landlord advertising cost by ≥30%
• Reduce tenant search time by ≥50%
• 100% multilingual support (English, Amharic, Afaan Oromo)
• Secure & scalable architecture
• Zero data breaches in testing

**Chapter 3 – System Design**
• Client-Server architecture
• Microservices: User Management, Payment, Property Search, Chatbot
• PostgreSQL with JSONB for dynamic property fields
• UML diagrams: Class, Sequence, Deployment
• Access control: Owner / Tenant / Broker / Admin roles

**Chapter 4 – Implementation & Testing**
• Agile + Iterative development
• Google OAuth login
• FAISS in-memory vector store for AI chatbot
• Multilingual embeddings for accurate Amharic/Oromo search
• Full unit tests with pytest

**Current Limitations**:
• Rent payments are offline (cash/bank) – online payment coming soon
• Listings must be updated manually by landlords
• Map shows location only (no navigation yet)
• Terms & Conditions only in English (will be translated)

**Future Plans**:
• Full rent payment integration
• AI-powered property recommendations
• User reviews & ratings
• Mobile app (React Native)
• Expand to all regions of Ethiopia

**Support**: Email support@bate.com or use the contact form.

This platform is built with love by five Ethiopian developers to make renting simple, fair, and accessible for everyone."""

def load_and_split_documents() -> List[str]:
    """
    Loads the hardcoded documents, extracts relevant text, and splits them into chunks.
    """
    all_texts = []

    # Process JSONs: Extract values and concatenate
    all_texts.append(" ".join(AMHARIC_TRANSLATION_JSON.values()))
    all_texts.append(" ".join(ENGLISH_TRANSLATION_JSON.values()))
    all_texts.append(" ".join(AFAAN_OROMO_TRANSLATION_JSON.values()))

    # Add full text from Faq.txt
    all_texts.append(FAQ_TEXT)

    # Add summarized text from DOCX
    all_texts.append(DOCX_SUMMARY_TEXT)

    combined_text = "\n\n".join(all_texts)

    # Split into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(combined_text)
    return chunks

class MultilingualEmbeddings:
    """
    Wrapper for sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 embeddings.
    Loads the model only once.
    """
    _model = None

    @classmethod
    def get_embedding_model(cls):
        if cls._model is None:
            # Ensure that the model is downloaded to a persistent location if possible
            # For Render free tier, it will download on each cold start.
            # This model is relatively small (approx 100MB)
            # Using a smaller model for memory optimization on Render's free tier.
            # 'paraphrase-multilingual-MiniLM-L6-v2' is a smaller alternative to 'L12-v2'.
            token = os.getenv("HUGGINGFACEHUB_API_TOKEN", None)
            cls._model = SentenceTransformer(
                "sentence-transformers/paraphrase-multilingual-MiniLM-L6-v2",
                device="cpu",
                use_auth_token=token
            )
        return cls._model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        model = self.get_embedding_model()
        return model.encode(texts).tolist()

    def embed_query(self, text: str) -> List[float]:
        model = self.get_embedding_model()
        return model.encode(text).tolist()

# Initialize the embedding model globally but lazily
# This will be used by the vector_store.py
embedding_model = MultilingualEmbeddings()

if __name__ == "__main__":
    # Example usage and verification
    print("Loading and splitting documents...")
    chunks = load_and_split_documents()
    print(f"Number of chunks: {len(chunks)}")
    print(f"First chunk: {chunks[0][:200]}...")

    print("\nTesting embedding model...")
    sample_texts = ["Hello world", "ሰላም አለም", "Akkam jirtu"]
    embeddings = embedding_model.embed_documents(sample_texts)
    print(f"Embeddings for '{sample_texts[0]}': {embeddings[0][:5]}...")
    print(f"Embedding dimension: {len(embeddings[0])}")
