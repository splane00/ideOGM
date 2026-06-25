import pandas as pd
import numpy as np
import random

# Configuration
num_rows = 205
sv_types = ['deletion', 'duplication', 'inversion', 'insertion', 'trans_interchr', 'trans_intrachr']
chroms = list(range(1, 25)) # 1-22, X(23), Y(24)

# Generate data
data = []
for _ in range(num_rows):
    chrom1 = random.choice(chroms)
    chrom2 = random.choice(chroms) if random.random() > 0.7 else chrom1
    start = random.randint(1_000_000, 100_000_000)
    end = start + random.randint(5000, 50_000_000)
    
    # Ensure logical end if it's not a trans-event
    if chrom1 == chrom2 and end > 248_000_000:
        end = 248_000_000
        
    data.append([chrom1, chrom2, start, end, random.choice(sv_types)])

# Create DataFrame
df = pd.DataFrame(data, columns=['RefcontigID1', 'RefcontigID2', 'RefStartPos', 'RefEndPos', 'Type'])

# Save to CSV (adding the required #h prefix for your loader)
df.to_csv("example_data.csv", index=False)

# Re-open and prepend the header comment as required by your load_smap_csv function
with open("example_data.csv", "r") as f:
    content = f.read()
with open("example_data.csv", "w") as f:
    f.write("#h RefcontigID1,RefcontigID2,RefStartPos,RefEndPos,Type\n" + content)

print(f"Successfully generated 200+ rows in example_data.csv")