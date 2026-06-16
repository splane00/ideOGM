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
