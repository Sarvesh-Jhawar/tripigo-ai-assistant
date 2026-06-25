"""
Data Ingestion Route.
Handles reading data from our JSON files, converting them into vector embeddings,
and storing them in our ChromaDB and BM25 search indexes.
"""
import json
from fastapi import APIRouter
from services.vector_service import embed_documents
from services.rag_service import collection, init_bm25

# Initialize the API router for ingestion endpoints
router = APIRouter()

@router.post("/ingest")
def ingest_data():
    """
    Endpoint to trigger data ingestion.
    Reads `tripigo_chunks.json`, processes the text, generates vector embeddings,
    and saves everything into ChromaDB for fast semantic search.
    """
    try:
        # Step 1: Read the raw travel data from our local JSON file
        with open("data/tripigo_chunks.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            
        ids = []
        documents = []
        metadatas = []
        
        # Step 2: Process each item in the JSON data
        for item in data:
            ids.append(item["id"])
            
            # Extract basic fields
            keywords = item.get("keywords", [])
            title = item.get("title", "")
            content = item.get("content", "")
            
            # Combine title, content, and keywords into one large string.
            # This rich text improves the accuracy of both Vector and Keyword search.
            full_text = f"{title}. {content} " + " ".join(keywords)
            documents.append(full_text)
            
            # Construct metadata object to store alongside the vector.
            # Metadata is useful for filtering or displaying rich UI results later.
            meta = {
                "id": item["id"],
                "title": title,
                "type": item.get("type", ""),
            }
            if "destination" in item:
                meta["destination"] = item["destination"]
            if "duration" in item:
                meta["duration"] = item["duration"]
            if "price" in item:
                meta["price"] = item["price"]
            
            # Merge any nested metadata fields into a flat structure
            # ChromaDB requires metadata to be a flat dictionary of simple types (string, int, bool)
            if "metadata" in item and isinstance(item["metadata"], dict):
                for k, v in item["metadata"].items():
                    if isinstance(v, (str, int, float, bool)):
                        meta[k] = v
                    elif isinstance(v, list):
                        meta[k] = ", ".join([str(x) for x in v])
            
            metadatas.append(meta)
            
        # Step 3: Generate vector embeddings for all the document texts
        embeddings = embed_documents(documents)
        
        # Step 4: Store everything in the ChromaDB vector database
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )
        
        # Step 5: Re-initialize the BM25 Keyword Search index with the new data
        init_bm25()
        
        # Return success status along with the number of chunks successfully processed
        return {"status": "success", "chunks": len(ids)}
        
    except Exception as e:
        # Catch any errors during ingestion and return them safely to avoid crashing the server
        return {"status": "error", "message": str(e)}
