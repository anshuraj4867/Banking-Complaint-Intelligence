
import pandas as pd
from pathlib import Path

input_file = Path("data/cleaned_complaints.csv")
output_file = Path("data/sample_complaints.csv")

print("Checking input file...")

if not input_file.exists():
    print("ERROR: cleaned_complaints.csv was not found.")
else:
    print("Loading cleaned dataset...")

    df = pd.read_csv(input_file)

    sample = df[["complaint"]].head(100)

    sample.to_csv(output_file, index=False, encoding="utf-8")

    print("Sample created successfully!")
    print("Number of complaints:", len(sample))
    print("Saved to:", output_file.resolve())
