import streamlit as st
import os
import main
from main import generate_ideogram

st.set_page_config(page_title="ideOGM Web", layout="centered")

st.title("IdeOGM")
st.subheader("An open-source Python tool for targeted circular ideogram visualization of structural variants in soft tissue and bone tumors")

uploaded_files = st.file_uploader("Upload one or more OGM CSV files", type="csv", accept_multiple_files=True)

min_length = st.slider("Minimum Variant Length (bp)", 1000, 100000, 5000)
assembly = st.selectbox("Genome Assembly", ["GRCh37", "GRCh38"])


if uploaded_files:
    # Save all uploaded files to the current working directory
    saved_files = []
    for uploaded_file in uploaded_files:
        input_path = uploaded_file.name
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_files.append(input_path)
    
    # Define output path
    input_to_process = saved_files[0] if len(saved_files) == 1 else os.getcwd()
    output_png = "ideOGM_plot.png"

    # THIS IS THE ONLY BUTTON CALL YOU NEED
    if st.button("Generate Ideogram", key="gen_ideogram_btn"):        
        with st.spinner('Processing genomic coordinates...'):
            try:
                # 1. Print current working directory to console
                print(f"DEBUG: Working Directory: {os.getcwd()}")
                print(f"DEBUG: Processing files: {saved_files}")
                
                # 2. CALL THE FUNCTION AND CAPTURE ERRORS
                generate_ideogram(input_to_process, output_png, min_length=min_length, assembly=assembly)
                
                # 3. Check for the file
                if os.path.exists(output_png):
                    st.image(output_png)
                else:
                    st.error("The function finished, but no file was created.")
                    st.write("Files in current directory:", os.listdir(os.getcwd()))
                
            
            except Exception as e:
                # THIS WILL SHOW YOU THE EXACT PYTHON ERROR
                st.error(f"The generation script failed with this error: {e}")
                import traceback
                st.code(traceback.format_exc())