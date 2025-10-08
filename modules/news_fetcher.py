import os
from pathlib import Path
import streamlit as st
import pandas as pd
import base64

UPLOAD_DIR = Path("uploaded_papers")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  

METADATA_FILE = Path("data/research_papers.csv")
METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)  

def save_uploaded_file(uploaded_file):
    file_path = UPLOAD_DIR / uploaded_file.name
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(file_path), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def add_paper_metadata(title, topic, uploader_name, filename):
    try:
        df = pd.read_csv(METADATA_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Title", "Topic", "Uploader", "Filename"])

    new_entry = pd.DataFrame([[title, topic, uploader_name, filename]], columns=df.columns)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(METADATA_FILE, index=False)

def list_uploaded_papers():
    if not METADATA_FILE.exists():
        return []
    df = pd.read_csv(METADATA_FILE)
    return df.to_dict(orient="records")

def embed_pdf(file_path: Path):
    if not file_path.exists():
        st.error(f"File not found: {file_path.name}")
        return
    with open(str(file_path), "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    st.markdown(
        f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>',
        unsafe_allow_html=True
    )

def show_news_and_research():
    st.subheader("📚 Agri Research Paper Portal")
    st.write("Upload and read research papers directly here. No external links required.")

    with st.expander("➕ Add New Research Paper"):
        uploader_name = st.text_input("👤 Your Name")
        title = st.text_input("Paper Title")
        topic = st.text_input("Topic")
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

        if st.button("Save Paper"):
            if uploader_name and title and topic and uploaded_file:
                file_path = save_uploaded_file(uploaded_file)
                add_paper_metadata(title, topic, uploader_name, uploaded_file.name)
                st.success(f"'{title}' by {uploader_name} added successfully!")
            else:
                st.warning("Please fill all fields and upload a PDF.")

    st.markdown("---")
    st.markdown("### Available Research Papers")

    papers = list_uploaded_papers()
    if not papers:
        st.info("No papers uploaded yet.")
    else:
        for paper in papers:
            with st.container():
                st.markdown(f"""
<div style="background: linear-gradient(135deg, #f0f9ff, #e0f7e9); 
            padding: 15px; border-radius: 12px; margin-bottom: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
    <h3 style="color:#2b7a0b; margin-bottom: 5px;">{paper['Title']}</h3>
    <p style="margin:0; color: #007bff;"><strong>Topic:</strong> {paper['Topic']}</p>
    <p style="margin:0; color: #007bff;"><strong>Uploader:</strong> {paper['Uploader']}</p>
</div>
""", unsafe_allow_html=True)


                file_path = UPLOAD_DIR / paper["Filename"]
                embed_pdf(file_path)
