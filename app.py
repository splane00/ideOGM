import streamlit as st
import os
from main import generate_ideogram

st.set_page_config(page_title="ideOGM Web", layout="centered")

# --- TOP MENU ---
col1, col2 = st.columns([1, 5])
if 'page' not in st.session_state:
    st.session_state.page = "Generator"
with col1:
    if st.button("About"): st.session_state.page = "About"
    if st.button("Generator"): st.session_state.page = "Generator"

st.divider()

if st.session_state.page == "Generator":
    st.title("IdeOGM")
    
    uploaded_files = st.file_uploader("Upload OGM CSV files", type="csv", accept_multiple_files=True)
    
    # 1. Determine input file path
    if uploaded_files:
    # If user uploads files, use the first one
        input_to_process = uploaded_files[0].name
        with open(input_to_process, "wb") as f:
            f.write(uploaded_files[0].getbuffer())
    else:
        # FALLBACK: If nothing uploaded, use the example file included in the repo
        example_path = "example_data.csv"
        if os.path.exists(example_path):
            input_to_process = example_path
            st.info("No file uploaded. Processing default example_data.csv.")
        else:
            st.warning("Please upload a CSV file to begin.")
            input_to_process = None

    # Proceed with generation
    if input_to_process and st.button("Generate Ideogram", key="gen_ideogram_btn"):
        with st.spinner('Processing...'):
            try:
                generate_ideogram(input_to_process, "ideOGM_plot.png")
                if os.path.exists("ideOGM_plot.png"):
                    st.image("ideOGM_plot.png")
            except Exception as e:
                st.error(f"Error: {e}")

elif st.session_state.page == "About":
    st.title("About IdeOGM")
    st.write("Information about your tool...")