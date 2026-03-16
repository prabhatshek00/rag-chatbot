<<<<<<< HEAD
# 📄 PDF RAG Chatbot
### Ask questions about any PDF using AI — 100% Free
## 🚀 Live Demo
[Click here to try the app](https://your-streamlit-link.streamlit.app)

Built with: Python · LangChain · FAISS · HuggingFace · Streamlit

---

## 🚀 Setup (5 minutes)

### Step 1 — Install Python
Download Python 3.10+ from https://python.org  
(Check "Add to PATH" during installation)

### Step 2 — Open Terminal / Command Prompt
- Windows: Press `Win + R`, type `cmd`, press Enter
- Mac: Press `Cmd + Space`, type `terminal`, press Enter

### Step 3 — Go to project folder
```
cd path/to/rag_chatbot
```

### Step 4 — Install dependencies
```
pip install -r requirements.txt
```
(This may take 3-5 minutes — it downloads AI models)

### Step 5 — Get free HuggingFace token
1. Go to https://huggingface.co
2. Create a free account
3. Go to Settings → Access Tokens
4. Click "New token" → Name it anything → Role: Read → Generate
5. Copy the token (starts with `hf_`)

### Step 6 — Run the app
```
streamlit run app.py
```
Your browser will open automatically at http://localhost:8501

---

## 💬 How to use
1. Paste your HuggingFace token in the sidebar
2. Upload any PDF
3. Ask questions in the chat box!

---

## 🛠️ Tech Stack (for your resume/interview)
| Component | Tool | Purpose |
|-----------|------|---------|
| UI | Streamlit | Web interface |
| PDF parsing | pypdf | Extract text from PDF |
| Text splitting | LangChain | Break text into chunks |
| Embeddings | sentence-transformers | Convert text → vectors |
| Vector store | FAISS | Fast similarity search |
| LLM | Mistral-7B (HuggingFace) | Generate answers |
| Chain | LangChain RetrievalQA | Connects everything |

---

## ❓ Troubleshooting
- **Slow first run**: The embedding model downloads (~90MB) on first use
- **Rate limit error**: Wait 30 seconds (free HF tier has limits)
- **Token error**: Make sure you copied the full token including `hf_`
- **Blank answers**: Try rephrasing your question more specifically
=======
# rag-chatbot
RAG-based PDF chatbot using LangChain, FAISS, HuggingFace, and Streamlit. Upload any PDF and ask questions — 100% free and open source.
>>>>>>> 3eb188434f2e719c1dd1f2eb3b01da7bd1096219
