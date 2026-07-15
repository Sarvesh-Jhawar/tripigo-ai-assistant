"""
Main application entry point for the Tripigo Tales Travel Assistant Backend.
This file initializes the FastAPI application, configures CORS settings, 
and registers the different API routers (chat, ingest, health).
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes import chat, ingest, health

# Initialize the FastAPI application with a custom title
app = FastAPI(title="Tripigo Tales Travel Assistant")

# Configure CORS (Cross-Origin Resource Sharing)
# This allows our frontend application (like a React or Vite app) to communicate
# with this backend API without security blocks from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, restrict this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all HTTP headers
)

# Include the routing logic from our different route modules
app.include_router(chat.router)    # Handles the /chat endpoint for AI interaction
app.include_router(ingest.router)  # Handles the /ingest endpoint for database population
app.include_router(health.router)  # Handles the /health check endpoint

# Auto-ingestion on startup if ChromaDB is empty
@app.on_event("startup")
def startup_event():
    from services.rag_service import collection, init_bm25
    from routes.ingest import ingest_data
    try:
        # Check if the database has any items
        count = collection.count()
        if count == 0:
            print("ChromaDB collection is empty. Running auto-ingestion of travel chunks...")
            result = ingest_data()
            print(f"Auto-ingestion completed: {result}")
        else:
            print(f"ChromaDB collection already contains {count} chunks. Syncing BM25 search index...")
            init_bm25()
    except Exception as e:
        print(f"Startup check failed: {e}")

# Serve React static frontend files if built
dist_path = os.path.join(os.path.dirname(__file__), "frontend-example", "dist")
if os.path.exists(dist_path):
    print(f"Mounting static frontend assets from: {dist_path}")
    app.mount("/assets", StaticFiles(directory=os.path.join(dist_path, "assets")), name="assets")
    
    # Catch-all route to serve the React SPA index.html
    @app.get("/{catchall:path}")
    async def serve_spa(catchall: str):
        # Keep API routes accessible
        if catchall.startswith("chat") or catchall.startswith("ingest") or catchall.startswith("health"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not Found")
        return FileResponse(os.path.join(dist_path, "index.html"))
else:
    print(f"Frontend build folder not found at {dist_path}. Running backend-only mode.")

if __name__ == "__main__":
    import uvicorn
    # Run the application using the Uvicorn ASGI server
    # Host '0.0.0.0' makes it accessible on the local network
    # Port '8000' is the default port for FastAPI
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
