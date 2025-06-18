import streamlit as st

def render_doc_upload_screen():
    st.markdown("## 📄 Document Upload")
    uploaded_files = st.file_uploader("Upload schema or policy documents", accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            st.success(f"Uploaded: {file.name}")
            # Future: Save to /data/docs + embed
