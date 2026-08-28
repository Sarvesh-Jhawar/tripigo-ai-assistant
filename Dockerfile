FROM python:3.10-slim
WORKDIR /app

# Install build dependencies for compiled python packages (e.g., ChromaDB, rank-bm25)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files, data, and static UI
COPY app.py .
COPY routes/ ./routes/
COPY services/ ./services/
COPY data/ ./data/
COPY static/ ./static/


# Expose port (Render sets $PORT dynamically, default 10000)
EXPOSE 10000

# Set Python behavior variables
ENV HOST=0.0.0.0
ENV PORT=10000
ENV PYTHONUNBUFFERED=1

# Launch the FastAPI app using Uvicorn with dynamic port binding
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}"]

