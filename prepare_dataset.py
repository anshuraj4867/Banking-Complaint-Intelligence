
import pandas as pd
from pathlib import Path

INPUT_FILE = "data/complaint_data.csv"
OUTPUT_FILE = "data/cleaned_complaints.csv"

TEXT_COLUMN = "Consumer complaint narrative"
LABEL_COLUMN = "Issue"

MAX_CATEGORIES = 10
MAX_PER_CATEGORY = 2000
CHUNK_SIZE = 20000

print("Preparing a smaller dataset...")

# First pass: count usable complaints in each category
category_counts = {}

for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False):
    chunk = chunk.dropna(subset=[TEXT_COLUMN, LABEL_COLUMN])
    chunk = chunk[chunk[TEXT_COLUMN].str.strip().ne("")]

    counts = chunk[LABEL_COLUMN].value_counts()
    for category, count in counts.items():
        category_counts[category] = (
            category_counts.get(category, 0) + int(count)
        )

selected_categories = [
    category
    for category, count in sorted(
        category_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )[:MAX_CATEGORIES]
]

print("Selected categories:")
for category in selected_categories:
    print("-", category)

# Second pass: collect a limited number per category
collected = {category: [] for category in selected_categories}

for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE, low_memory=False):
    chunk = chunk.dropna(subset=[TEXT_COLUMN, LABEL_COLUMN])
    chunk = chunk[chunk[TEXT_COLUMN].str.strip().ne("")]
    chunk = chunk[chunk[LABEL_COLUMN].isin(selected_categories)]

    for category in selected_categories:
        remaining = MAX_PER_CATEGORY - len(collected[category])

        if remaining > 0:
            rows = chunk[chunk[LABEL_COLUMN] == category]
            if not rows.empty:
                collected[category].extend(
                    rows[[TEXT_COLUMN, LABEL_COLUMN]]
                    .head(remaining)
                    .to_dict("records")
                )

    if all(
        len(rows) >= min(MAX_PER_CATEGORY, category_counts[category])
        for category, rows in collected.items()
    ):
        break

# Combine and save only the required columns
frames = []

for category, records in collected.items():
    if records:
        frames.append(pd.DataFrame(records))

result = pd.concat(frames, ignore_index=True)
result = result.rename(columns={
    TEXT_COLUMN: "complaint",
    LABEL_COLUMN: "category"
})

Path("data").mkdir(exist_ok=True)
result = result.sample(frac=1, random_state=42).reset_index(drop=True)
result.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print("\nDataset preparation complete!")
print("Total records:", len(result))
print("Number of categories:", result["category"].nunique())
print("Saved to:", OUTPUT_FILE)
print("\nRecords per category:")
print(result["category"].value_counts().to_string())
