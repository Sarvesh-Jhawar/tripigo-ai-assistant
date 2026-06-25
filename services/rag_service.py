"""
RAG (Retrieval-Augmented Generation) Service.
This is the core search engine of the chatbot. It implements a Hybrid Search algorithm,
combining Vector Search (via ChromaDB) and Keyword Search (via BM25Okapi) using 
Reciprocal Rank Fusion (RRF) to find the most accurate travel information.
"""
import chromadb
from services.vector_service import embed_text
from rank_bm25 import BM25Okapi

# Initialize a persistent local ChromaDB client to store and retrieve vector embeddings
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="tripigo_collection")

# Global variables for the BM25 Keyword Search index
bm25 = None
all_ids = []
all_docs = []
all_metas = []

def init_bm25():
    """
    Initializes or reloads the BM25 search index by fetching all documents currently 
    stored in ChromaDB. This ensures keyword search is perfectly synced with vector data.
    """
    global bm25, all_ids, all_docs, all_metas
    try:
        # Fetch all stored data from the vector database
        data = collection.get()
        if data and data.get('documents'):
            all_ids = data['ids']
            all_docs = data['documents']
            all_metas = data['metadatas']
            
            # Tokenize the documents (split into lowercase words) for the BM25 algorithm
            tokenized_corpus = [doc.lower().split() for doc in all_docs]
            bm25 = BM25Okapi(tokenized_corpus)
    except Exception as e:
        print(f"BM25 Initialization failed or collection is empty: {e}")

# Initialize BM25 on server startup
init_bm25()

def hybrid_search(query: str, top_k: int = 5):
    """
    Performs a Hybrid Search to find the best matching travel documents.
    It runs both a Vector Search (for semantic meaning) and a Keyword Search 
    (for exact words), then combines the results using Reciprocal Rank Fusion (RRF).
    
    Args:
        query (str): The user's search query.
        top_k (int): The number of top results to return (default 5).
        
    Returns:
        list[dict]: A list of formatted context chunks containing the relevant information.
    """
    # Safety check: If the database is completely empty, return nothing
    if collection.count() == 0:
        return []

    # --- Phase 1: Vector Search ---
    # Convert the query into a vector and find the semantically closest documents
    query_embedding = embed_text(query)
    vector_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k * 2, collection.count())
    )
    
    # Dictionary to hold the combined RRF scores for each document ID
    rrf_scores = {}
    
    # Process vector search results and apply RRF scoring
    if vector_results and vector_results.get('ids') and vector_results['ids'][0]:
        v_ids = vector_results['ids'][0]
        v_docs = vector_results['documents'][0]
        v_metas = vector_results['metadatas'][0]
        for rank, (vid, vdoc, vmeta) in enumerate(zip(v_ids, v_docs, v_metas)):
            if vid not in rrf_scores:
                rrf_scores[vid] = {"score": 0, "doc": vdoc, "meta": vmeta}
            # RRF Formula: 1 / (rank + constant)
            rrf_scores[vid]["score"] += 1.0 / (rank + 60)
            
    # --- Phase 2: Keyword Search (BM25) ---
    # Find documents containing the exact words used in the query
    if bm25:
        tokenized_query = query.lower().split()
        bm25_scores = bm25.get_scores(tokenized_query)
        
        # Get the indices of the highest scoring documents
        top_n_indices = sorted(range(len(bm25_scores)), key=lambda i: bm25_scores[i], reverse=True)[:top_k * 2]
        
        # Process keyword search results and apply RRF scoring
        for rank, idx in enumerate(top_n_indices):
            if bm25_scores[idx] > 0: # Only consider matches that have a score > 0
                vid = all_ids[idx]
                if vid not in rrf_scores:
                    rrf_scores[vid] = {"score": 0, "doc": all_docs[idx], "meta": all_metas[idx]}
                # Add to the existing RRF score
                rrf_scores[vid]["score"] += 1.0 / (rank + 60)
            
    # --- Phase 3: Combine and Sort ---
    # Sort all found documents by their combined RRF score and pick the top_k
    sorted_results = sorted(rrf_scores.values(), key=lambda x: x["score"], reverse=True)[:top_k]
    
    # --- Phase 4: Format the Context ---
    # Construct clean, readable strings to send to the LLM
    chunks = []
    for res in sorted_results:
        meta = res['meta']
        doc = res['doc']
        
        # Build context string utilizing the available metadata
        context_parts = []
        if 'title' in meta:
            context_parts.append(f"=== {meta['title']} ===")
        if 'destination' in meta:
            context_parts.append(f"Destination: {meta['destination']}")
        if 'duration' in meta:
            context_parts.append(f"Duration: {meta['duration']}")
        if 'price' in meta:
            context_parts.append(f"Price: ₹{meta['price']}")
        
        context_parts.append(doc)
        
        chunks.append({
            "title": meta.get('title', 'Unknown Source'),
            "context": "\n".join(context_parts)
        })
        
    return chunks
