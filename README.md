# 💰 Retail AI Advisor (RAG-based Financial Assistant)

## 📌 Project Description
Retail AI Advisor is a Retrieval-Augmented Generation (RAG) based application that allows users to upload financial documents (PDF/TXT) and interact with them through a chat interface.

The system processes documents, converts them into embeddings, and retrieves relevant context to generate accurate, context-aware responses using a Large Language Model.

---

## 🎯 Goal of the Project
- Build an intelligent financial assistant using RAG architecture  
- Provide context-based answers instead of generic LLM responses  
- Reduce hallucination by grounding responses in uploaded documents  
- Simulate real-world AI systems used in finance and customer support  

---

## ⚙️ Tech Stack

### Backend
- Python  
- FastAPI  

### AI / ML
- LangChain  
- Google Gemini (LLM + Embeddings)  

### Frontend
- Streamlit  

### Database
- PostgreSQL (configured)  

---

## 🛠️ Tools & Libraries Used
- LangChain (RAG orchestration)  
- PyPDFLoader (PDF processing)  
- RecursiveCharacterTextSplitter (chunking)  
- Requests (API communication)  
- Uvicorn (server)  
- Streamlit (UI development)  

---

## 🧠 Key Concepts Implemented
- Retrieval-Augmented Generation (RAG)  
- Embeddings & Vector Search  
- Document Chunking  
- Semantic Retrieval  
- Conversational Memory  
- API-based Architecture  

---

## 🔄 Project Workflow
1. Upload document (PDF/TXT)  
2. Extract and split text into chunks  
3. Convert chunks into embeddings  
4. Store embeddings in vector database  
5. Retrieve relevant chunks for user query  
6. Generate response using LLM  

---

## 📂 Project Structure
retail_ai_advisor/
│
├── app/
│ ├── api/v1/endpoints/
│ │ ├── upload.py
│ │ └── query.py
│ ├── services/
│ │ ├── ingestion_service.py
│ │ └── query_service.py
│ ├── rag/
│ │ ├── agent.py
│ │ ├── embeddings.py
│ │ ├── vector_store.py
│ │ └── memory.py
│ ├── utils/
│ │ ├── chunking.py
│ │ └── loader.py
│ └── main.py
│
├── ui/
│ └── streamlit_app.py
│
├── data/
├── .env
├── .gitignore
├── pyproject.toml
└── README.md
