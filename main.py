# !usr/bin/env python3

import os
import glob
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import sys
import tkinter as tk
from tkinter import filedialog, messagebox


# 1. hg38 Chromosome Configuration
chrom_sizes = {
    1: 248956422, 2: 242193529, 3: 198295559, 4: 190214555, 5: 181538259,
    6: 170805979, 7: 159345973, 8: 145138636, 9: 138394717, 10: 133797422,
    11: 135086622, 12: 133275309, 13: 114364328, 14: 107043718, 15: 101991189,
    16: 90338345, 17: 83257020, 18: 80373285, 19: 58617616, 20: 64444167,
    21: 46709983, 22: 50818468, 23: 156040895, 24: 57227415
}
chrom_names = {i: f"chr{i}" if i <= 22 else ("chrX" if i==23 else "chrY") for i in chrom_sizes}

# Coordinate Mapping Setup
gap = 50_000_000 
total_len = sum(chrom_sizes.values()) + gap * len(chrom_sizes)
offsets = {i: sum(list(chrom_sizes.values())[:i-1]) + (i-1)*gap for i in sorted(chrom_sizes.keys())}

def get_theta(chrom, pos):
    if pd.isna(chrom) or chrom not in offsets or pd.isna(pos):
        return None
    return 2 * np.pi * (offsets[int(chrom)] + max(0, pos)) / total_len

# 2. Function to safely load SMAP files
def load_smap_csv(path):
    header_idx = 0
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for i, line in enumerate(f):
            if line.startswith('#h'):
                header_idx = i
                break
                
    df = pd.read_csv(path, skiprows=header_idx, low_memory=False).iloc[1:]
    df.columns = [c.strip().replace('#h ', '') for c in df.columns]
    
    required_columns = ['RefcontigID1', 'RefcontigID2', 'RefStartPos', 'RefEndPos', 'Type']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        print(f"\n[SKIPPED] Incompatible file layout: '{os.path.basename(path)}' (Missing columns: {missing})")
        return pd.DataFrame(columns=required_columns)

    mapping = {'X': 23, 'Y': 24, 'x': 23, 'y': 24}
    for col in ['RefcontigID1', 'RefcontigID2']:
        df[col] = df[col].apply(lambda x: mapping.get(str(x).upper(), x))
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['RefStartPos'] = pd.to_numeric(df['RefStartPos'], errors='coerce')
    df['RefEndPos'] = pd.to_numeric(df['RefEndPos'], errors='coerce')
    
    # Type Standardizations
    df['Type'] = df['Type'].replace({
        'deletion_nbase': 'deletion', 'duplication_inverted': 'duplication',
        'duplication_split': 'duplication', 'insertion_nbase': 'insertion',
        'inversion_paired': 'inversion', 'inversion_partial': 'inversion',
        'translocation_interchr': 'trans_interchr', 'trans_interchr_common': 'trans_interchr',
        'trans_interchr_segdupe': 'trans_interchr', 'translocation_intrachr': 'trans_intrachr',
        'trans_intrachr_common': 'trans_intrachr', 'trans_intrachr_segdupe': 'trans_intrachr'
    })
    df = df[~df['Type'].apply(lambda x: str(x).strip().isdigit() if pd.notna(x) else False)]
    return df[required_columns]

# 3. Main Plotting Logic Execution
def generate_ideogram(input_path, output_filename=None):
    if os.path.isdir(input_path):
        all_files = glob.glob(os.path.join(input_path, "*.csv"))
        files_to_process = [f for f in all_files if 'combined' not in f and 'ideogram' not in f]
        if not output_filename:
            output_filename = os.path.join(input_path, "ogm_ideogram.png")
        if not files_to_process:
            print(f"Error: The directory '{input_path}' contains no CSV files.")
            return
    elif os.path.isfile(input_path):
        files_to_process = [input_path]
        if not output_filename:
            output_filename = os.path.splitext(input_path)[0] + "_ideogram.png"
    else:
        print(f"Error: Path '{input_path}' not found.")
        return

    print(f"Found {len(files_to_process)} target CSV data files. Initializing parsing pipeline...")
    
    parsed_dfs = []
    for idx, f in enumerate(files_to_process, 1):
        print(f"   [{idx}/{len(files_to_process)}] Processing: {os.path.basename(f)}", end='\r')
        parsed_dfs.append(load_smap_csv(f))
    print(f"\nData extraction complete. Aggregating records into visualization engine...")
    
    combined_df = pd.concat(parsed_dfs)
    if combined_df.empty:
        print("Warning: No valid structural variants loaded. Image generation stopped.")
        return

    fig = plt.figure(figsize=(14, 14))
    ax = fig.add_subplot(111, polar=True)
    
    type_color_map = {
        'deletion': 'red', 'insertion': 'lightgreen', 'inversion': 'blue',
        'duplication': 'orange', 'trans_interchr': 'lightblue', 'trans_intrachr': 'darkblue'
    }

    all_types_found = sorted(combined_df['Type'].dropna().unique())
    known_types = [t for t in type_color_map.keys() if t in all_types_found]

    # Chromosome Labels
    for chrom, size in chrom_sizes.items():
        t0, t1 = get_theta(chrom, 0), get_theta(chrom, size)
        if t0 is not None and t1 is not None:
            mid_t = (t0 + t1) / 2
            rot = np.degrees(mid_t) - 90
            if 90 < rot < 270: rot += 180
            ax.text(mid_t, 1.15, chrom_names[chrom], rotation=rot, ha='center', va='center', fontsize=16)

    # Chromosome Outlines
    for chrom, size in chrom_sizes.items():
        t0, t1 = get_theta(chrom, 0), get_theta(chrom, size)
        if t0 is not None and t1 is not None:
            # Draw outer boundary arc
            t_range = np.linspace(t0, t1, 100)
            ax.plot(t_range, np.ones_like(t_range) * 1.05, color='black', lw=1, alpha=0.8)
            # Draw inner boundary arc
            ax.plot(t_range, np.ones_like(t_range) * 0.94, color='black', lw=1, alpha=0.8)
            # Draw left boundary line
            ax.plot([t0, t0], [0.94, 1.05], color='black', lw=1, alpha=0.8)
            # Draw right boundary line
            ax.plot([t1, t1], [0.94, 1.05], color='black', lw=1, alpha=0.8)

    # Plot SVs
    for _, row in combined_df.iterrows():
        t1 = get_theta(row['RefcontigID1'], row['RefStartPos'])
        c2 = row['RefcontigID2'] if row['RefcontigID2'] != -1 else row['RefcontigID1']
        p2 = row['RefEndPos'] if row['RefEndPos'] != -1 else row['RefStartPos']
        t2 = get_theta(c2, p2)
        if t1 is None or t2 is None: continue
        
        color = type_color_map.get(row['Type'], 'gray')
        
        if row['RefcontigID1'] != c2 or abs(p2 - row['RefStartPos']) > 10_000_000:
            ts = np.linspace(t1, t2, 100)
            if abs(t1 - t2) > np.pi:
                if t1 < t2: ts = np.linspace(t1, t2 - 2*np.pi, 100) % (2*np.pi)
                else: ts = np.linspace(t1, t2 + 2*np.pi, 100) % (2*np.pi)
            dist = min(abs(t1-t2), 2*np.pi - abs(t1-t2))
            start_r = 0.95
            r_min = start_r - (0.8 * dist / np.pi)
            rs = start_r - (start_r - r_min) * np.sin(np.linspace(0, np.pi, 100))
            ax.plot(ts, rs, color=color, alpha=0.4, lw=1.5)
        else:
            t_start, t_end = min(t1, t2), max(t1, t2)
            if t_end - t_start < 0.005: 
                t_mid = (t_start + t_end) / 2
                t_start, t_end = t_mid - 0.0025, t_mid + 0.0025
            t_range = np.linspace(t_start, t_end, 10)
            ax.fill_between(t_range, 0.96, 1.04, color=color, alpha=0.8)

    legend_elements = [Line2D([0], [0], color=type_color_map[t], lw=8, label=t) for t in known_types]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.45, 1.1), title="Structural Variants", fontsize=14, title_fontsize=16, frameon=True, borderpad=1)

    # Clean borders axis clean-up
    ax.set_axis_off()
    
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"\nHigh-resolution circular ideogram saved to:\n   {os.path.abspath(output_filename)}")

def run_gui_mode():
    """Launches a visual window for users who don't want to use the terminal."""
    root = tk.Tk()
    root.title("IdeOGM - Circular Ideogram Generator")
    root.geometry("500x260")
    root.resizable(False, False)
    
    # Simple formatting styles
    bg_color = "#f5f5f5"
    root.configure(bg=bg_color)
    
    # Title Label
    tk.Label(
        root, text="IdeOGM Visualization Tool", 
        font=("Helvetica", 16, "bold"), bg=bg_color, fg="#333333"
    ).pack(pady=15)
    
    tk.Label(
        root, text="Select an OGM data file or folder to generate your circular ideogram plot.",
        font=("Helvetica", 10), bg=bg_color, fg="#666666", wraplength=400, justify="center"
    ).pack(pady=5)

    def select_file():
        file_path = filedialog.askopenfilename(
            title="Select Bionano OGM CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if file_path:
            process_gui_request(file_path)

    def select_folder():
        folder_path = filedialog.askdirectory(title="Select Folder Container")
        if folder_path:
            process_gui_request(folder_path)

    def process_gui_request(target_path):
        root.withdraw() # Hide main frame during rendering
        try:
            # Reuses your core plotting logic seamlessly
            generate_ideogram(target_path)
            messagebox.showinfo("Success!", f"Visualization complete!\n\nYour file has been generated and saved to the same folder as your input data.")
        except Exception as e:
            messagebox.showerror("Error Encountered", f"An execution failure occurred:\n{str(e)}")
        finally:
            root.destroy() # Safely close app loop

    # Interactive Action Buttons
    btn_frame = tk.Frame(root, bg=bg_color)
    btn_frame.pack(pady=20)
    
    tk.Button(
        btn_frame, text="📁 Process Single File", font=("Helvetica", 11),
        command=select_file, width=18, height=2, bg="#e1e1e1"
    ).grid(row=0, column=0, padx=10)
    
    tk.Button(
        btn_frame, text="📂 Process Folder (Batch)", font=("Helvetica", 11),
        command=select_folder, width=18, height=2, bg="#e1e1e1"
    ).grid(row=0, column=1, padx=10)

    # Footer attribution text
    tk.Label(
        root, text="MIT Open Source License",
        font=("Helvetica", 8, "italic"), bg=bg_color, fg="#999999"
    ).pack(side="bottom", pady=10)

    root.mainloop()

# 4. Smart Argument Entry Logic
if __name__ == "__main__":
    # If the user did not pass arguments, automatically show the visual window!
    if len(sys.argv) == 1:
        run_gui_mode()
    else:
        # Standard CLI path for power users and server execution scripts
        parser = argparse.ArgumentParser(description="IdeOGM Tabular Data Visualization Engine")
        parser.add_argument("input", type=str, help="Path to file or folder.")
        parser.add_argument("-o", "--output", type=str, default=None, help="Output destination image path.")
        args = parser.parse_args()
        generate_ideogram(args.input, args.output)