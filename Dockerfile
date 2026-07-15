FROM python:3.10-slim
WORKDIR /app

# Install build dependencies for compiled python packages (e.g., ChromaDB, rank-bm25)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files and data
COPY app.py .
COPY routes/ ./routes/
COPY services/ ./services/
COPY data/ ./data/

# Expose port 7860 (Hugging Face Spaces default container port)
EXPOSE 7860

# Set Python behavior variables
ENV HOST=0.0.0.0
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

# Launch the FastAPI app using Uvicorn on port 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
