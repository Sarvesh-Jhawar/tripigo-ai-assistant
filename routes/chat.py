"""
Chat Route.
Handles incoming user chat messages, triggers the hybrid search for context retrieval,
and generates an AI response using the LLM service.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from services.rag_service import hybrid_search
from services.llm_service import generate_answer

# Initialize the API router for chat endpoints
router = APIRouter()

# Define the expected JSON structure for incoming chat requests
class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_endpoint(request: ChatRequest):
    """
    Main endpoint for communicating with the AI Chatbot.
    It takes the user's message, finds relevant travel information,
    and returns a professionally formatted markdown response.
    """
    question = request.message
    
    # Step 1: Perform Hybrid Search (Vector + Keyword Search)
    # Retrieves the top 5 most relevant travel packages or policies from our database
    search_results = hybrid_search(question, top_k=5)
    
    # Step 2: Handle cases where no relevant information is found
    # This acts as a strict fallback to prevent the AI from hallucinating or guessing answers
    if not search_results:
        return {
            "answer": "I couldn't find that information in Tripigo's travel database.",
            "sources": []
        }
        
    # Extract the context text and the source titles from the search results
    contexts = [res["context"] for res in search_results]
    sources = [res["title"] for res in search_results]
    
    # Step 3: Generate Answer using the Large Language Model (LLM)
    # Pass the user's question and the retrieved context to generate a factual response
    answer = generate_answer(question, contexts)
    
    # Deduplicate the source titles for clean presentation
    unique_sources = list(set(sources))
    
    # Step 4: Append Sources to the Response
    # If the bot successfully found an answer, attach the sources at the bottom
    # so the user knows exactly where the information came from.
    if unique_sources and "I couldn't find that information in Tripigo's travel database." not in answer:
        sources_md = "\n\n---\n### Sources\n" + "\n".join([f"- {src}" for src in unique_sources])
        answer += sources_md
        
    # Return the final generated response and the list of sources used
    return {
        "answer": answer,
        "sources": unique_sources
    }
