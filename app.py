import streamlit as st
import os
# Import your ideOGM generation function here
# from your_script import generate_ideogram 

st.set_page_config(page_title="ideOGM Web", layout="centered")

st.title("🧬 ideOGM")
st.subheader("Targeted Circular Ideogram Generator")

st.markdown("""
Upload your filtered OGM CSV file to instantly generate a 
publication-ready circular ideogram. This tool is designed to 
bridge the gap between raw tabular data and high-resolution 
visual reporting.
""")

# File uploader
uploaded_file = st.file_uploader("Upload your OGM CSV file", type="csv")

if uploaded_file is not None:
    # Save to a temporary file for processing
    temp_filename = "temp_input.csv"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    output_filename = "ideOGM_plot.png"
    
    if st.button("Generate Ideogram"):
        with st.spinner('Processing genomic coordinates...'):
            try:
                # Call your core function
                # generate_ideogram(temp_filename, output_filename)
                
                # Placeholder for your actual plot display
                st.image(output_filename, caption="Generated ideOGM Visualization")
                
                # Provide a download button
                with open(output_filename, "rb") as file:
                    st.download_button(
                        label="Download PNG",
                        data=file,
                        file_name="ideOGM_plot.png",
                        mime="image/png"
                    )
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")