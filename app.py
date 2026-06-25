import streamlit as st
import os
import main
from main import generate_ideogram

st.set_page_config(page_title="ideOGM Web", layout="centered")

st.title("IdeOGM")
st.subheader("An open-source Python tool for targeted circular ideogram visualization of structural variants in soft tissue and bone tumors")

uploaded_files = st.file_uploader("Upload one or more OGM CSV files", type="csv", accept_multiple_files=True)

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

    if st.button("Generate Ideogram"):
        with st.spinner('Processing genomic coordinates...'):
            try:
                # 1. Print current working directory to console
                print(f"DEBUG: Working Directory: {os.getcwd()}")
                print(f"DEBUG: Processing files: {saved_files}")
                
                # 2. CALL THE FUNCTION AND CAPTURE ERRORS
                generate_ideogram(input_to_process, output_png)
                
                # 3. Check for the file
                if os.path.exists(output_png):
                    st.image(output_png)
                    # ... add download button ...
                else:
                    st.error("The function finished, but no file was created.")
                    # DEBUG: List what IS in the folder
                    st.write("Files in current directory:", os.listdir(os.getcwd()))
            
            except Exception as e:
                # THIS WILL SHOW YOU THE EXACT PYTHON ERROR
                st.error(f"The generation script failed with this error: {e}")
                import traceback
                st.code(traceback.format_exc())

    

    if st.button("Generate Ideogram"):
        with st.spinner('Processing genomic coordinates...'):
            try:
                # 1. Print current working directory to console
                print(f"DEBUG: Working Directory: {os.getcwd()}")
                
                # 2. CALL THE FUNCTION AND CAPTURE ERRORS
                generate_ideogram(input_path, output_png)
                
                # 3. Check for the file
                if os.path.exists(output_png):
                    st.image(output_png)
                    # ... add download button ...
                else:
                    st.error("The function finished, but no file was created.")
                    # DEBUG: List what IS in the folder
                    st.write("Files in current directory:", os.listdir(os.getcwd()))
            
            except Exception as e:
                # THIS WILL SHOW YOU THE EXACT PYTHON ERROR
                st.error(f"The generation script failed with this error: {e}")
                import traceback
                st.code(traceback.format_exc())