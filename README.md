# IdeOGM

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

**IdeOGM** is an open-source Python visualization suite designed for the rapid and customizable generation of high-resolution circular ideograms directly from Bionano Optical Genome Mapping (OGM) SMAP tabular data exports. 

The software bridges the gap between text-heavy genomic variant outputs and intuitive, publication-ready infographics. Built to support dual modalities, it offers a robust command-line interface for automated bioinformatics pipelines alongside a clean graphical user interface (GUI) optimized for cytogeneticists, clinical trial coordinators, and wet-lab researchers.

---

## Features

- **Dual Modality Execution:** Switches between a point-and-click GUI and an advanced command-line utility.
- **Robust Multi-File Batching:** Recursively processes single `.csv` outputs or entire directories, automatically aggregating multi-sample sets.
- **Fault-Tolerant SMAP Parsing:** Automatically inspects formatting, identifies missing metadata headers, and isolates/logs unparseable logs or system configuration files without throwing fatal crashes.
- **Automatic Type Standardization:** Normalizes complex structural variant calling schemas (`deletion_nbase`, `duplication_split`, `translocation_interchr`, etc.) into cleanly categorized color spaces.
- **Flexible Dynamic Layouts:** Adjusts output canvases automatically, mapping radial text and chord curves safely to maintain exact legend proportions across wide datasets.

---

## Installation & Requirements

IdeOGM relies entirely on core Python analytical modules and standard data-science dependencies. 

1. Ensure Python 3.8 or higher is installed on your local operating system.
2. Install the necessary baseline requirements via standard Python package managers:

```bash
pip install pandas matplotlib numpy
```

## Usage Workflow
**Interactive Graphical Interface (GUI)**
To execute the interactive standalone workflow suite, simply run the main pipeline runner without appending trail arguments:  
```bash
python main.py
```  
A native system pop-up window will initialize. Users can seamlessly click "Process Single File" or "Process Folder (Batch)" to browse to their workspace using native system file managers (Finder/Explorer). Once compiled, a success message details the absolute directory path where your finalized image is saved.Modality 2: Command Line Interface (CLI)For high-throughput compute servers and automation scripts, supply positional arguments via the terminal:Batch Process an Entire Folder Directory:
```Bash
python main.py path/to/smap_exports/
```  
(Processes all match-eligible files in the folder and saves a unified canvas named combined_sv_ideogram.png directly inside the input target folder).    
    
**Process an Isolated Case-Study File**  
```Bash
python main.py path/to/sample_patient_data.csv
```

**Customizing the Publication File Name**  
To stream the finished figure canvas into a separate assets directory or supply specific figure nomenclature, use the -o or --output flag:
```Bash
python main.py path/to/smap_exports/ -o clinical_trials/output/Figure_1_Sarcoma_Case.png
```
**Expected Data Input Format**  
IdeOGM is custom-built to interpret Bionano Access workflow sheets and native structural variant framework schemas. It scans rows for standard header prefixes (#h) and parses the following explicit spatial vectors:  
- RefcontigID1 / RefcontigID2 (Chromosome origins)  
- RefStartPos / RefEndPos (Base pair positioning coordinates)  
- Type (Structural variant categorization)

**Visual Mapping Configuration**  
Variants are plotted relative to a canonical hg38 reference architecture, applying continuous radial calculation algorithms to represent mutations accurately. Variants within an intra-chromosomal locus are represented as high-contrast structural bands (alpha=0.8), whereas distant segment rearrangements or inter-chromosomal links are projected across an interior spanning chord ribbon grid (alpha=0.4):
| Structural Variant | Visual Color |
| :---: | :---: |
| Deletion | Red |
| Insertion | Light Green |
| Duplication | Orange |
| INTERchromosomal translocation | Light Blue |
| INTRAchromosomal translocation | Dark Blue |

**Packaging Standalone Applications**  
To convert this visual environment into an autonomous, double-clickable app package (.app or .exe) for distribute-ready lab sharing, utilize PyInstaller. To bypass potential segmentation faults caused by extraneous machine-learning bindings on large data-science environments, explicitly exclude redundant packages during execution:  
```Bash
pip install pyinstaller
pyinstaller --onefile --windowed --exclude-module tensorflow --exclude-module PySide6 --exclude-module PyQt5 --name IdeOGM path/to/main.py
```
Your ready-to-use desktop client will compile natively within the generated dist/ subfolder.  
  
## License & Academic Reference  
This software architecture is made available under the open-source MIT License. Feel free to use, modify, and distribute it in academic and commercial environments. If this visualization suite proves beneficial to your peer-reviewed publications or research pipelines, please attribute the work by citing the repository codebase or the corresponding communication manuscript.
