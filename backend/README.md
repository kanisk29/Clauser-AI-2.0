<<<<<<< HEAD
# ⚖️ Clauser AI – Contract Risk Analyzer

Clauser AI is an AI-powered contract analysis tool that identifies legal risks, explains clauses, and suggests mitigations. It supports custom knowledge injection using Retrieval-Augmented Generation (RAG) and is designed as a lightweight, deployable system.

---

### Live Demo: https://clauser-ai-by-kanisk.streamlit.app/

---

## 🚀 Features

* 📄 Upload and analyze PDF/DOCX contracts
* ⚠️ Detect high, medium, and low-risk clauses
* 🧠 AI-driven explanations with mitigation suggestions
* 📚 Custom Knowledge Base (RAG) for company playbooks
* 📥 Download revised contracts with applied mitigations
* ⚡ Lightweight deployment using FakeEmbeddings (no heavy ML dependencies)

---

## 🏗️ Architecture

```
User Input (Contract)
        ↓
Text Extraction (PDF/DOCX)
        ↓
Chunking
        ↓
Vector Store (Chroma)
        ↓
(Optional) RAG Retrieval
        ↓
LLM (Groq - Llama 3.3)
        ↓
Structured Risk Output (JSON)
        ↓
DOCX Generation (Mitigated Contract)
```

---

## 🧠 Tech Stack

* **Frontend:** Streamlit
* **LLM:** Groq (Llama 3.3 70B)
* **Vector DB:** Chroma
* **Embeddings:** FakeEmbeddings (lightweight, deploy-safe)
* **Document Processing:** PyPDF2, python-docx
* **Observability:** LangSmith

---

## 📂 Project Structure

```
.
├── app.py                # Streamlit UI
├── ingestion.py         # File parsing + indexing
├── retrieval.py         # RAG + LLM logic
├── eval_pipeline.py     # Evaluation pipeline (LangSmith)
├── requirements.txt     # Dependencies
├── .gitignore
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/your-username/clauser-ai.git
cd clauser-ai
```

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run the App

```
streamlit run app.py
```

---

## ☁️ Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Deploy on Streamlit Cloud
3. Add secret in dashboard:

```
GROQ_API_KEY = "your_api_key"
```

---

## 🧪 Example Use Case

* Upload a vendor agreement
* Select persona (e.g., Service Provider)
* Optionally upload company playbook
* Run analysis
* Accept mitigations
* Download revised contract

---

## ⚠️ Disclaimer

This tool is for educational purposes only.
It does **not** provide legal advice. Always consult a qualified legal professional.

---

## 🔮 Future Improvements

* Replace FakeEmbeddings with real semantic embeddings
* Hybrid retrieval (BM25 + vector search)
* Better Indian law grounding
* Clause-level explainability
* Multi-jurisdiction support

## ⭐ If you found this useful

Consider giving the repo a star.
=======
# Clauser-AI-2.0
>>>>>>> 3623819d384bbaf657d9d9885c0a7ea17b6c15c6
