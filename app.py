import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from huggingface_hub import InferenceClient
import os

st.set_page_config(page_title="PDF Chat Assistant", page_icon="📄", layout="centered")
st.title("📄 PDF Chat Assistant")
st.markdown("Upload any PDF and ask questions — 100% free!")
st.divider()

with st.sidebar:
    st.header("⚙️ Setup")
    hf_token = st.text_input("HuggingFace API Token", type="password", placeholder="hf_xxxxxxxxxxxxxxxx")
    st.markdown("[Get free token ↗](https://huggingface.co/settings/tokens)")
    st.divider()
    st.markdown("**Steps:**")
    st.markdown("1. Paste your token above")
    st.markdown("2. Upload a PDF")
    st.markdown("3. Ask questions!")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    return text

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_text(text)

@st.cache_resource(show_spinner="Indexing your PDF...")
def build_vector_store(text):
    chunks = split_text(text)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )
    return FAISS.from_texts(chunks, embeddings)

def get_answer(question, vector_store, token):
    docs = vector_store.similarity_search(question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    client = InferenceClient(token=token)

    messages = [
        {
            "role": "system",
            "content": f"You are a helpful assistant. Answer questions using ONLY the context below.\n\nContext:\n{context}"
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat_completion(
        messages=messages,
        model="Qwen/Qwen2.5-72B-Instruct",
        max_tokens=400,
        temperature=0.3,
    )

    answer = response.choices[0].message.content
    return answer, docs

if uploaded_file and hf_token:
    with st.spinner("Reading PDF..."):
        raw_text = extract_text(uploaded_file)

    if not raw_text.strip():
        st.error("Could not read this PDF. It may be a scanned image.")
        st.stop()

    st.success(f"✅ Loaded: **{uploaded_file.name}** — {len(raw_text):,} characters")
    st.divider()

    vector_store = build_vector_store(raw_text)

    st.subheader("💬 Ask anything about your PDF")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Type your question here...")

    if question:
        with st.chat_message("user"):
            st.markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer, docs = get_answer(question, vector_store, hf_token)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    with st.expander("📌 Sources from PDF"):
                        for i, doc in enumerate(docs, 1):
                            st.caption(f"Chunk {i}:")
                            st.text(doc.page_content[:300] + "...")
                except Exception as e:
                    err = str(e)
                    if "401" in err:
                        st.error("❌ Invalid token. Check your HuggingFace token in the sidebar.")
                    elif "429" in err or "Rate" in err:
                        st.warning("⏳ Rate limit. Wait 30 seconds and try again.")
                    else:
                        st.error(f"❌ Error: {err}")

    if st.session_state.messages:
        if st.button("🗑️ Clear chat"):
            st.session_state.messages = []
            st.rerun()

elif uploaded_file and not hf_token:
    st.warning("⬅️ Please enter your HuggingFace token in the sidebar.")
elif hf_token and not uploaded_file:
    st.info("⬆️ Please upload a PDF file above.")
else:
    st.markdown("""
    ### 👋 Welcome!
    This app lets you **chat with any PDF** using AI.
    
    **To get started:**
    1. Get your free token at [huggingface.co](https://huggingface.co/settings/tokens)
    2. Paste it in the sidebar  
    3. Upload a PDF and ask anything!
    """)
