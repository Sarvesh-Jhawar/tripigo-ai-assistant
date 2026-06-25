"""
Health Check Route.
Provides a simple endpoint to verify that the server is running and accessible.
"""
from fastapi import APIRouter

# Initialize the API router for health-related endpoints
router = APIRouter()

@router.get("/health")
def health_check():
    """
    Simple GET endpoint to check the health of the API.
    Returns a JSON object indicating the server status.
    Useful for uptime monitoring or Docker container health checks.
    """
    return {"status": "healthy"}
