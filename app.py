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
        input_to_process = uploaded_files[0].name
        with open(input_to_process, "wb") as f:
            f.write(uploaded_files[0].getbuffer())
    else:
        # Default fallback
        input_to_process = "example_data.csv"
        if os.path.exists(input_to_process):
            st.info("No file uploaded. Displaying default example_data.csv.")
        else:
            st.error("Default 'example_data.csv' not found. Please upload a file.")
            input_to_process = None

    # 2. Process and Display
    if input_to_process and st.button("Generate Ideogram", key="gen_btn"):
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