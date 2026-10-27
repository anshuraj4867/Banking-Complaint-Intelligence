
import pandas as pd

FILE_PATH = "data/complaint_data.csv"
TEXT_COLUMN = "Consumer complaint narrative"
LABEL_COLUMN = "Issue"

total_rows = 0
usable_rows = 0
category_counts = {}

print("Inspecting complaint dataset...")
print("File:", FILE_PATH)

for chunk in pd.read_csv(FILE_PATH, chunksize=20000, low_memory=False):
    total_rows += len(chunk)

    # Remove rows without complaint text or category
    chunk = chunk.dropna(subset=[TEXT_COLUMN, LABEL_COLUMN])

    # Remove empty complaint text
    chunk = chunk[chunk[TEXT_COLUMN].str.strip().ne("")]

    usable_rows += len(chunk)

    counts = chunk[LABEL_COLUMN].value_counts()
    for category, count in counts.items():
        category_counts[category] = (
            category_counts.get(category, 0) + int(count)
        )

print("\n--- DATASET SUMMARY ---")
print("Total rows:", total_rows)
print("Usable complaints:", usable_rows)
print("Number of categories:", len(category_counts))

print("\nTop 15 complaint categories:")
for category, count in sorted(
    category_counts.items(),
    key=lambda item: item[1],
    reverse=True
)[:15]:
    print(f"{category}: {count}")
