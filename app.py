"""
Main application entry point for the Tripigo Tales Travel Assistant Backend.
This file initializes the FastAPI application, configures CORS settings, 
and registers the different API routers (chat, ingest, health).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

if __name__ == "__main__":
    import uvicorn
    # Run the application using the Uvicorn ASGI server
    # Host '0.0.0.0' makes it accessible on the local network
    # Port '8000' is the default port for FastAPI
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
