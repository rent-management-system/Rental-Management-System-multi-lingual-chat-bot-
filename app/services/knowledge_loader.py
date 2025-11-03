import json
from typing import List

class KnowledgeLoader:
    def __init__(self):
        self.knowledge_path = "./knowledge_base"
    
    async def load_all_documents(self) -> List[str]:
        """Load all knowledge base documents"""
        documents = []
        
        # 1. Load project documentation
        project_docs = self._load_project_documentation()
        documents.append(f"PROJECT_DOCS:\n{project_docs}")
        
        # 2. Load translation files as context
        translations = self._load_translations_context()
        documents.append(f"TRANSLATIONS:\n{translations}")
        
        # 3. Load FAQ knowledge
        faqs = self._load_faqs()
        documents.extend(faqs)
        
        return documents
    
    def _load_project_documentation(self) -> str:
        """Load your complete graduation project"""
        return """
        RENTAL MANAGEMENT SYSTEM - GRADUATION PROJECT
        
        BACKGROUND:
        The rental industry in Ethiopia faces challenges with high broker fees...
        
        PROBLEM STATEMENT:
        Landlords face high advertising costs, tenants struggle with search process...
        
        OBJECTIVES:
        - Develop web-based platform with pay-per-post model
        - Multi-language support (Amharic, English, Afan Oromo)
        - Cost-effective property listing
        - No-fee tenant search experience
        
        TECHNICAL STACK:
        - Frontend: React.js
        - Backend: Python (Django/FastAPI) 
        - Database: PostgreSQL
        - Deployment: Render.com
        
        FEATURES:
        - Property listing management
        - Advanced search with filters
        - Map integration
        - User authentication
        - Multi-language UI
        
        SCOPE:
        - Property advertisement with pay-per-post
        - Tenant search interface
        - User authentication and security
        - Multi-language support
        
        LIMITATIONS:
        - Map shows locations only (no navigation)
        - Manual payment processing
        - Property verification challenges
        """
    
    def _load_translations_context(self) -> str:
        """Load all translation files as searchable context"""
        translations = {
            "amharic": {
                "home": "", "about": "cc", "properties": "c",
                "your_ai_rent_management_system": "cc",
                "bate_exclamation": "c", 
                "find_your_next_home": "c",
                "about_paragraph": "c"
            },
            "english": {
                "home": "Home", "about": "About", "properties": "Properties",
                "your_ai_rent_management_system": "Your AI Rent Management System", 
                "bate_exclamation": "Bate!",
                "find_your_next_home": "Find your next home with ease and confidence",
                "about_paragraph": "The Rental Management System transforms how landlords and tenants connect..."
            },
            "afan_oromo": {
                "home": "Mana", "about": "Waa'ee", "properties": "Qabeenya",
                "your_ai_rent_management_system": "Sirna Bulchiinsa Kirraa AI Kee",
                "bate_exclamation": "Baatee!",
                "find_your_next_home": "Mana jireenya kee itti aanu salphaan fi ofitti amanamummaan barbaadi", 
                "about_paragraph": "Sirni Bulchiinsa Kiraayiin kun walitti dhufeenya abbootii manaa fi kireeffattoota jijjiira..."
            }
        }
        return json.dumps(translations, ensure_ascii=False, indent=2)
    
    def _load_faqs(self) -> List[str]:
        """Load FAQ documents"""
        faqs = []
        
        # General FAQs
        faqs.append("""
        FREQUENTLY ASKED QUESTIONS:
        
        Q: How do I list my property?
        A: Landlords can list properties using the pay-per-post model...
        
        Q: Is there a fee for tenants?
        A: No, tenants can search and contact landlords for free...
        
        Q: What languages are supported?
        A: English, Amharic, and Afan Oromo are fully supported...
        
        Q: How does the pay-per-post model work?
        A: Landlords pay a small fee only when they list a property...
        """)
        
        return faqs
