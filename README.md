# Chat with Documents - Intelligent AI System

## About the Project

This is an advanced artificial intelligence system that lets you ask natural language questions about uploaded documents, using state-of-the-art technologies such as OpenAI, Pinecone, LangChain, and LangGraph.

### What the System Does

- Document Upload: Send PDF, Word, Excel, PowerPoint, and text files
- Intelligent Processing: Automatically extracts and analyzes content
- Natural Chat: Converse with your documents as if you were speaking to a specialist
- Semantic Search: Finds relevant information even if you use different words
- Multiple Conversations: Each conversation keeps its own context and documents

### Demo

https://github.com/user-attachments/assets/fac6fb5d-e9d6-41cc-9bc3-6759b6a07069

---

## System Architecture

### Code Organization

```
proj-final-prog/
├── backend/                    # Python server (API + AI)
│   ├── api/                   # REST endpoints
│   │   ├── routers/           # Routes organized by feature
│   │   │   ├── agent.py       # AI chat
│   │   │   └── documents.py   # Document upload and search
│   │   └── schemas/           # API data structures
│   ├── agent/                 # AI system (LangGraph)
│   │   ├── graph.py           # Agent orchestration
│   │   ├── nodes.py           # Processing logic
│   │   └── agent_toolbox/     # Agent tools
│   │       └── tools/         # Document search
│   ├── vector_store/          # Pinecone integration
│   ├── utils/                 # Utilities
│   │   ├── embeddings.py      # Embedding generation (OpenAI)
│   │   ├── text_chunking.py   # Smart text chunking
│   │   └── file_processing.py # File processing
│   └── settings.py            # Configuration
├── frontend/                   # User interface (React/TypeScript)
└── pyproject.toml             # Dependencies and configuration
```

### How the System Works

1. Document Upload:
   - The user uploads a file (PDF, Word, etc.)
   - The system automatically detects the type and extracts the content
   - The text is split into smart chunks
   - Each chunk becomes an embedding (a numerical vector)
   - Embeddings are stored in Pinecone with metadata

2. Chat with AI:
   - The user asks a question
   - The system converts the question into an embedding
   - It searches for similar chunks in Pinecone
   - The AI analyzes the relevant chunks and the question
   - It generates a contextualized, natural response

3. Intelligent Agent:
   - Uses LangGraph to orchestrate the flow
   - OpenAI GPT-4 for natural language processing
   - Specialized tools for document search
   - Isolated context per conversation (thread_id)

---

## Complete Setup (For Beginners)

### Prerequisites

Make sure you have installed:

1. Python 3.12+ - [Download here](https://www.python.org/downloads/)
2. UV (modern Python package manager) - [Installation instructions](https://docs.astral.sh/uv/getting-started/installation/)

### 1. Download the Project

```bash
# Clone the repository
git clone https://github.com/MatheusOliveiraSilva/proj-final-prog
cd proj-final-prog
```

### 2. Set Up the Backend (Python Server)

```bash
# Enter the backend folder
cd backend

# Install dependencies with UV (faster than pip)
uv pip install -e .

# Go back to the project root
cd ..
```

### 3. Set Up the Frontend (Interface)

The frontend repository is available [here](https://github.com/MatheusOliveiraSilva/ChatWithDocs-Front). Follow the README instructions there.

### 4. Configure Environment Variables

Create a file named `.env` in the `backend/` folder with the following content:

```bash
# Open your text editor and create backend/.env
# Paste the content that will be sent separately
```

Important: API keys (OPENAI_API_KEY, PINECONE_API_KEY, etc.) will be sent separately to Professor Clarisse for security reasons. Paste them into the `.env` file you created.

### 5. Run the System

#### Terminal 1 - Backend (API):
```bash
cd backend
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend (Interface):
```bash
cd frontend
npm run dev
```

### 6. Access the System

- User interface: http://localhost:5173
- API (documentation): http://localhost:8000/docs

---

## Technologies Used

### Backend (Python)
- LangChain: Framework for AI applications
- LangGraph: Orchestration of intelligent agents
- OpenAI: Language models (GPT-4) and embeddings
- Pinecone: Vector database for semantic search
- FastAPI: Modern, fast web framework
- PyPDF2: PDF file processing
- Pandas: Data analysis (Excel/CSV)
- python-docx: Word document processing

### Frontend (TypeScript/React)
- React: UI library
- TypeScript: JavaScript with static typing
- Tailwind CSS: Styling framework
- Server-Sent Events: Real-time response streaming

### Infrastructure
- UV: Fast management of Python dependencies
- Docker: Containerization (optional)
- uvicorn: ASGI server for FastAPI

---

## How to Use the System

### 1. Upload Documents
- Open the web interface
- Click "Upload Document"
- Select your files (PDF, Word, Excel, etc.)
- Wait for automatic processing

### 2. Ask Questions
- Type your question in the chat box
- Questions can be about any content in the documents
- Examples:
  - "What is the summary of the AI document?"
  - "What are the main conclusions of the research?"
  - "Find information about machine learning"

### 3. Tips for Better Results
- Be specific: "Which performance metrics were mentioned?" is better than "How is the performance?"
- Use context: "In the chapter about neural networks, which algorithm is recommended?"
- Ask about relationships: "What is the relationship between concepts X and Y in the document?"

---

## Contribution

This project was developed as a master's final project. Suggestions and improvements are welcome!

---

## Academic Project

This system was developed as a master's final project, demonstrating the practical application of:

- Natural Language Processing (NLP)
- Retrieval-Augmented Generation (RAG)
- Modern AI architectures
- Full-stack development

The goal is to show how AI technologies can be applied to solve real problems of information access in documents, creating a natural and intuitive experience for users.

---

Built with modern AI technologies.
