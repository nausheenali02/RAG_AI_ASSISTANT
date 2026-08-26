# 🤖 RAG AI Assistant

An intelligent **document-based AI assistant** that uses **Retrieval-Augmented Generation (RAG)** to understand uploaded documents and provide context-aware answers.

The application allows users to upload **PDF, DOCX, or TXT files** and interact with their documents using two capabilities:

* 📑 **Document Summarization** — Generate a concise summary of the uploaded document.
* 💬 **Document Q&A** — Ask natural-language questions and receive answers based on the document content.

The system uses **Google Gemini** for language generation and embeddings, **LangChain** for RAG orchestration, and **Chroma** as the vector database.

---

## ✨ Features

### 📄 Multi-Format Document Upload

Upload documents in:

* PDF
* DOCX
* TXT

The application automatically selects the appropriate document loader.

### 📑 Document Summarization

Generate a concise summary of an uploaded document containing:

* Main topic
* Key points
* Important findings
* Conclusion

### 💬 Chat with Your Document

Ask questions about the uploaded document using natural language.

For example:

```text
What is this document about?

What are the main findings?

Explain the methodology used.

What conclusion does the author reach?
```

The system retrieves relevant sections of the document before generating the response.

### 🔎 Retrieval-Augmented Generation

The application uses a RAG pipeline to ground the LLM's responses in the uploaded document.

This helps reduce the possibility of the model generating information that is not present in the document.

### 📚 Source References

For document questions, the application displays the relevant document pages used during retrieval.

### 🖥️ Streamlit Interface

The application provides a simple and interactive web interface.

After uploading a document, users can choose between:

```text
📑 Summarize Document       💬 Chat with Document
```

---

# 🧠 How RAG Works

The application follows this pipeline:

```text
                    User Uploads Document
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Document Loader   │
                  │ PDF / DOCX / TXT    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    Text Splitting   │
                  │ Chunk Size: 1000    │
                  │ Overlap: 200        │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Gemini Embeddings   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │  Chroma Vector DB   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     Retriever       │
                  │      Top-K: 4       │
                  └──────────┬──────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
        Document Summary            User Question
                │                         │
                │                         ▼
                │                Relevant Chunks
                │                         │
                │                         ▼
                │                 Google Gemini
                │                         │
                ▼                         ▼
        Document Summary          Context-Aware Answer
                                          │
                                          ▼
                                   Source References
```

---

# 🔄 RAG Pipeline

## 1. Document Loading

The uploaded document is processed using LangChain document loaders.

The application supports:

```text
PDF  → PyPDFLoader
DOCX → Docx2txtLoader
TXT  → TextLoader
```

---

## 2. Text Splitting

Large documents are divided into smaller chunks using:

```text
RecursiveCharacterTextSplitter
```

Current configuration:

```text
Chunk Size   : 1000
Chunk Overlap: 200
```

The overlap helps preserve contextual continuity between neighboring chunks.

---

## 3. Embeddings

Each document chunk is converted into a vector representation using Google's Gemini embedding model:

```text
models/gemini-embedding-001
```

These embeddings allow the application to perform semantic similarity search.

---

## 4. Vector Database

The generated embeddings are stored in:

```text
Chroma
```

Chroma enables efficient retrieval of document chunks that are semantically related to a user's question.

---

## 5. Retrieval

When a user asks a question, the application searches the vector store and retrieves the most relevant chunks.

Current configuration:

```text
Top-K = 4
```

---

## 6. Context Augmentation

The retrieved chunks are added to the prompt as context.

The model is instructed to answer using the retrieved document information rather than relying on unrelated general knowledge.

---

## 7. Response Generation

Google Gemini generates the final response using the retrieved context.

The application uses:

```text
gemini-3-flash-preview
```

with:

```text
temperature = 0
```

This configuration is intended to produce consistent and focused responses.

---

# 🏗️ Project Architecture

The project follows a modular structure:

```text
RAG_AI_ASSISTANT/
│
├── app.py
│   └── Streamlit user interface
│
├── rag.py
│   └── Document processing
│   └── Text splitting
│   └── Gemini embeddings
│   └── Chroma vector store
│   └── Retriever
│   └── RAG chain
│   └── Summary chain
│
├── styles.py
│   └── Application styling
│
├── requirements.txt
│   └── Project dependencies
│
├── .env
│   └── Google Gemini API key
│
└── README.md
    └── Project documentation
```

> **Note:** The `.env` file should remain local and should never be committed to GitHub.

---

# 🛠️ Tech Stack

| Technology                         | Purpose                            |
| ---------------------------------- | ---------------------------------- |
| **Python**                         | Core programming language          |
| **Streamlit**                      | Web application interface          |
| **LangChain**                      | RAG pipeline and LLM orchestration |
| **Google Gemini**                  | Large Language Model               |
| **Gemini Embeddings**              | Document vectorization             |
| **Chroma**                         | Vector database                    |
| **PyPDFLoader**                    | PDF processing                     |
| **Docx2txtLoader**                 | DOCX processing                    |
| **TextLoader**                     | TXT processing                     |
| **RecursiveCharacterTextSplitter** | Document chunking                  |
| **python-dotenv**                  | Environment variable management    |

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/nausheenali02/RAG_AI_ASSISTANT.git
```

Move into the project directory:

```bash
cd RAG_AI_ASSISTANT
```

---

## 2. Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 API Key Configuration

This project uses the **Google Gemini API**.

Create a file named:

```text
.env
```

in the root directory.

Add:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Replace the placeholder with your actual Google Gemini API key.

### ⚠️ Security

Never upload your API key to GitHub.

Your `.gitignore` should contain:

```text
.env
.venv/
__pycache__/
```

---

# ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Streamlit will start the application locally and provide a URL in the terminal.

Open the displayed URL in your browser.

---

# 🖥️ Using the Application

## Step 1 — Upload a Document

Upload a:

```text
📄 PDF
📄 DOCX
📄 TXT
```

document.

The application processes the document and prepares it for retrieval.

---

## Step 2 — Select an Action

After uploading the document, two options are displayed:

```text
┌────────────────────────┐   ┌────────────────────────┐
│          📑            │   │          💬            │
│                        │   │                        │
│  Summarize Document    │   │  Chat with Document    │
│                        │   │                        │
│  [📑 Summarize]        │   │  [💬 Start Chat]       │
└────────────────────────┘   └────────────────────────┘
```

---

## Step 3 — Summarize

Select:

```text
📑 Summarize Document
```

Then click:

```text
✨ Generate Summary
```

The system sends the document content to Gemini and generates a structured summary.

---

## Step 4 — Chat

Select:

```text
💬 Chat with Document
```

Then ask questions about the uploaded document.

Example:

```text
What is the main objective of the research?

What methodology was used?

What are the key findings?

What are the limitations?

What is the conclusion?
```

The system retrieves relevant chunks from the document and uses them as context for Gemini.

---

# 🛡️ Hallucination Reduction

A major objective of this project is to provide answers grounded in the uploaded document.

The RAG prompt instructs the model to:

* Use retrieved document context.
* Avoid inventing information.
* State when the answer cannot be found in the document.
* Keep responses concise and relevant.

However, **RAG does not completely eliminate hallucinations**. The quality of the response depends on document quality, chunking, retrieval quality, and LLM behavior.

---

# 🎯 Use Cases

This application can be used for:

### 🎓 Education

* Lecture notes
* Study material
* Academic assignments
* Research papers

### 🔬 Research

* Research papers
* Technical reports
* Literature review
* Scientific documents

### 💼 Business

* Business reports
* Project documentation
* Internal reports
* Product documentation

### 📚 General Document Analysis

* Manuals
* Articles
* Reports
* Text documents

---

# 📌 Example

Suppose a user uploads a research paper.

Instead of manually reading the entire document, the user can ask:

```text
What problem does this paper address?
```

The system:

```text
Question
   ↓
Semantic Retrieval
   ↓
Relevant Document Chunks
   ↓
Gemini
   ↓
Answer
   ↓
Source Pages
```

This allows users to interact with long documents using natural language.

---

# 🚀 Future Enhancements

The current application can be extended with:

* 🧠 Improved conversational memory
* 📚 Multiple document uploads
* 🔎 Hybrid search
* ⚡ Vector-store caching
* 📊 Document analytics
* 🌐 Web search integration
* 📥 Downloadable summaries
* 📝 Structured report generation
* 📖 More detailed citations
* 🖼️ Table and image understanding
* 🔐 User authentication
* ☁️ Cloud deployment
* 📈 RAG evaluation and retrieval metrics

---

# ⚠️ Limitations

Currently, the system has several limitations:

* One uploaded document is processed at a time.
* Retrieval quality depends on chunking and embedding quality.
* Scanned/image-only PDFs may require OCR.
* The application depends on the Gemini API.
* Very large documents may increase API usage and processing time.
* RAG reduces hallucinations but cannot guarantee completely hallucination-free responses.

---

# 🔮 Future Vision

The goal is to evolve this project into a more complete **AI Research and Document Assistant** capable of:

```text
Multiple Documents
       ↓
Semantic Search
       ↓
RAG
       ↓
Conversational Memory
       ↓
Web Search
       ↓
Source Verification
       ↓
Structured Reports
       ↓
AI Research Assistant
```

---

# 👩‍💻 Author
## Nausheen Ali
B.Tech Computer Science
Specialization: Artificial Intelligence & Machine Learning
