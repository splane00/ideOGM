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
    st.write("""Optical Genome Mapping (OGM) has significantly advanced cytogenomics by enabling high-resolution detection of complex structural variants (SVs) and copy number variants (CNVs) across large eukaryotic genomes (MD Anderson Cancer Center, 2026; Yang, 2020). This capability is exceptionally vital in musculoskeletal oncology, as soft tissue and bone tumors frequently present with chaotic genomic landscapes, diagnostic fusions, and localized amplicons (MD Anderson Cancer Center, 2026). While native vendor platforms, such as Bionano Access and VIA software, offer automated, whole-genome circular visualizations, these enterprise-level tools lack the flexibility to easily isolate customized, publication-ready sub-plots directly from filtered tabular text files without relying on proprietary server environments (Bionano Genomics, n.d.; Technical Multi-Domain Analysis, n.d.).
\nIdeOGM was developed with the Cancer Cytogenetics Laboratory at Johns Hopkins School of Medicine for a 2026 publication, “Beyond the Fusion: Genomic Complexity in 103 Fusion-Driven Sarcomas Analyzed by Cytogenetics and Optical Genome Mapping” (Zou et al., 2026). IdeOGM directly parses the downstream, filtered .csv datasets exported from standard OGM analysis pipelines. It automatically extracts critical metrics, including chromosomal breakpoint coordinates, SV classifications, and copy number states, to instantly generate high-resolution, customizable circular ideograms (Bionano Genomics, 2021; Technical Multi-Domain Analysis, n.d.).
\nBy decoupling genomic visualization from vendor-locked server infrastructure, IdeOGM facilitates the rapid, reproducible, and publication-ready visual reporting of critical diagnostic variants (Technical Multi-Domain Analysis, n.d.)
\nIdeOGM is written in Python and is freely available on GitHub at https://github.com/splane00/IdeOGM under the open-source MIT License.
    """)