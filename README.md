# Tripigo Tales AI Assistant ✈️🤖

An advanced, production-ready travel chatbot backend built with **FastAPI**. It uses **Retrieval-Augmented Generation (RAG)** combined with **Hybrid Search (Vector + Keyword)** to provide highly accurate, beautifully formatted travel recommendations without hallucinating.

Created by **Sarvesh Jhawar**.

---

## 🌟 Key Features

- **Hybrid Search Architecture**: Combines ChromaDB (Vector Search) and BM25 (Keyword Search) using Reciprocal Rank Fusion (RRF) for the most accurate context retrieval.
- **Strict Anti-Hallucination**: The bot is rigidly programmed to say "I couldn't find that information in Tripigo's travel database" if the answer isn't in the provided data.
- **Lightning Fast AI**: Uses Groq's `llama-3.1-8b-instant` model for near-instantaneous responses.
- **Beautiful Formatting**: Automatically returns responses in clean Markdown (tables, bold text, bullet points).
- **Auto-Sources**: Appends the exact sources/documents used to generate the answer at the bottom of the response.

---

## 📁 Project Structure

```text
tripigo-chatbot/
│
├── app.py                     # Main FastAPI entry point & CORS config
├── requirements.txt           # Python dependencies
├── .env                       # API keys & environment variables
├── generate_docs.py           # Script to generate DOCX documentation
│
├── routes/                    # API Endpoints
│   ├── chat.py                # Handles /chat POST requests
│   ├── ingest.py              # Handles /ingest POST requests
│   └── health.py              # Handles /health GET requests
│
├── services/                  # Core Business Logic
│   ├── llm_service.py         # Groq LLM integration & prompt engineering
│   ├── rag_service.py         # Hybrid Search engine & RRF algorithm
│   └── vector_service.py      # SentenceTransformer text embedding
│
├── data/                      # Raw Data Storage
│   └── tripigo_chunks.json    # The travel knowledge base (JSON format)
│
├── chroma_db/                 # Persistent Vector Database directory
└── frontend-example/          # Example React/Vite frontend
```

---

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.9+
- Node.js (for the frontend example)

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/tripigo-ai-assistant.git
cd tripigo-ai-assistant
```

### 3. Backend Setup
Create a virtual environment and install the dependencies:
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
# Activate it (Mac/Linux)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory (or use the existing placeholder) and add your Groq API key.
Visit [Groq Cloud](https://console.groq.com/keys) to generate an API key.
```env
GROQ_API_KEY="your-groq-api-key-here"
```

---

## 🚀 How to Run Locally

### Starting the Backend
Run the FastAPI server without the reload flag to avoid WatchFiles conflicts when generating local files:
```bash
uvicorn app:app
```
The backend will run at: `http://localhost:8000`

### Starting the Frontend Example
Open a new terminal window, navigate to the frontend folder, and run it:
```bash
cd frontend-example
npm install
npm run dev
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/chat` | Send a JSON payload `{"message": "your question"}`. Returns a Markdown answer and sources. |
| **POST** | `/ingest` | Reads `data/tripigo_chunks.json` and repopulates the ChromaDB and BM25 search indexes. Run this when you update your data! |
| **GET** | `/health` | Simple health check `{"status": "healthy"}`. |

---

## 🛠️ Customization

### Changing the AI's Answer Length
You can easily increase or decrease the length and detail of the AI's responses by modifying the `SYSTEM_PROMPT` inside `services/llm_service.py`.

**To make answers much shorter:**
Add this to the prompt: *"Keep your answers brief, maximum 3-4 sentences. Do not provide unnecessary details unless explicitly asked."*

**To make answers highly detailed:**
Add this to the prompt: *"Provide exhaustive, highly detailed explanations. Expand on the destination's culture, best times to visit, and include a daily itinerary breakdown if possible."*
