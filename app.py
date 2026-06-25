import streamlit as st
import os
import main
from main import generate_ideogram

st.set_page_config(page_title="ideOGM Web", layout="centered")

st.title("IdeOGM: An open-source Python tool for targeted circular ideogram visualization of structural variants in soft tissue and bone tumors")
st.subheader("Circular Ideogram Generator for OGM Data")

uploaded_file = st.file_uploader("Upload your OGM CSV file", type="csv")

if uploaded_file is not None:
    # Use the filename provided by the uploader
    # We save it to the current working directory
    input_path = uploaded_file.name
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Define output path in the same directory
    output_png = "ideOGM_plot.png"
    
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