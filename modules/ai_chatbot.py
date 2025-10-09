import streamlit as st
import PyPDF2
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def chunk_text(text, chunk_size=500):
    text = text.replace("\n", " ")  
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def build_index(chunks, model):
    embeddings = model.encode(chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype('float32'))
    return index, embeddings

def search_answer(question, index, chunks, model):
    q_emb = model.encode([question])
    D, I = index.search(np.array(q_emb).astype('float32'), k=1)
    return chunks[I[0][0]]

def run():
    st.title("🤖 AI Farming Chatbot (PDF-based)")
    st.write("Upload a farming-related PDF and ask questions about crops, soil, irrigation, and best practices.")

    uploaded_file = st.file_uploader("Upload Farming PDF", type=["pdf"])
    if uploaded_file is not None:
        @st.cache_resource
        def load_model():
            return SentenceTransformer('all-MiniLM-L6-v2')
        
        model = load_model()

        text = extract_text_from_pdf(uploaded_file)
        chunks = chunk_text(text)
        index, _ = build_index(chunks, model)
        st.success(f"PDF loaded with {len(chunks)} text chunks. You can now ask questions.")

        user_question = st.text_input("💬 Ask your question:")
        if st.button("Get Answer") and user_question.strip() != "":
            answer = search_answer(user_question, index, chunks, model)
            st.chat_message("user").write(user_question)
            st.chat_message("assistant").write(answer)
