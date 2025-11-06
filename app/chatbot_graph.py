import os
from typing import List, Dict, Any, Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from app.vector_store import faiss_vector_store
from app.config import config
from app.utils import logger, get_gemini_language_code

# Initialize Gemini LLM
# Use gemini-1.5-flash for faster responses and lower cost
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=config.GOOGLE_API_KEY, temperature=0.2, convert_system_message_to_human=True)

class ChatbotState(Dict):
    """
    Represents the state of our chatbot in the LangGraph.
    """
    query: str
    language: Literal["english", "amharic", "afaan_oromo"]
    context: List[str] = []
    response: str = ""

def retrieve(state: ChatbotState) -> Dict[str, Any]:
    """
    Retrieves relevant documents from the FAISS vector store based on the query.
    """
    logger.info(f"Retrieving context for query: '{state['query']}'")
    context = faiss_vector_store.search(state["query"], k=3)
    logger.info(f"Retrieved {len(context)} context chunks.")
    return {"context": context}

def generate(state: ChatbotState) -> Dict[str, Any]:
    """
    Generates a response using the LLM based on the query and retrieved context.
    """
    logger.info(f"Generating response for query: '{state['query']}' in language: {state['language']}")
    
    gemini_lang = get_gemini_language_code(state['language'])
    
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful Rental Management System chatbot. Answer in {language} using the following context. If the question cannot be answered from the context, state that you don't have enough information."),
            ("human", "Context: {context}\nQuestion: {question}"),
        ]
    )
    
    rag_chain = prompt_template | llm | StrOutputParser()
    
    try:
        response = rag_chain.invoke({
            "language": gemini_lang,
            "context": "\n\n".join(state["context"]),
            "question": state["query"]
        })
        logger.info("Response generated successfully.")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error during LLM generation: {e}")
        return {"response": "Sorry, I encountered an issue while generating a response. Please try rephrasing your question."}

# Build the LangGraph
workflow = StateGraph(ChatbotState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

chatbot_graph = workflow.compile()

if __name__ == "__main__":
    # Example usage
    print("Testing chatbot graph...")
    
    # Ensure FAISS is initialized before running the graph
    _ = faiss_vector_store # Accessing it triggers initialization
    
    # Test English query
    english_query = "What property types can I list?"
    english_result = chatbot_graph.invoke({"query": english_query, "language": "english"})
    print(f"\nEnglish Query: {english_query}")
    print(f"English Response: {english_result['response']}")

    # Test Amharic query
    amharic_query = "አዲስ ተጠቃሚ እንዴት እመዘገባለሁ?"
    amharic_result = chatbot_graph.invoke({"query": amharic_query, "language": "amharic"})
    print(f"\nAmharic Query: {amharic_query}")
    print(f"Amharic Response: {amharic_result['response']}")

    # Test Afaan Oromo query
    afaan_oromo_query = "Sirni Bulchiinsa Kiraayii maali?"
    afaan_oromo_result = chatbot_graph.invoke({"query": afaan_oromo_query, "language": "afaan_oromo"})
    print(f"\nAfaan Oromo Query: {afaan_oromo_query}")
    print(f"Afaan Oromo Response: {afaan_oromo_result['response']}")
