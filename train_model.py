
import os
import re
import joblib
import pandas as pd
import spacy

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# --------------------------------------------------
# 1. Configuration
# --------------------------------------------------

DATA_FILE = "data/cleaned_complaints.csv"
MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)

print("Loading cleaned complaint dataset...")

df = pd.read_csv(DATA_FILE)

df = df.dropna(subset=["complaint", "category"])
df["complaint"] = df["complaint"].astype(str).str.strip()
df["category"] = df["category"].astype(str).str.strip()

df = df[
    df["complaint"].ne("") &
    df["category"].ne("")
].copy()

# Remove exact duplicate text/category pairs
df = df.drop_duplicates(subset=["complaint", "category"])

print("Usable records:", len(df))
print("Categories:", df["category"].nunique())

X = df["complaint"]
y = df["category"]

# --------------------------------------------------
# 2. Split data before fitting the model
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))

# --------------------------------------------------
# 3. Load spaCy English model
# --------------------------------------------------

print("\nLoading spaCy model...")

nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# Preserve negation words because they can change meaning.
NEGATIONS = {"no", "not", "never", "n't"}

def preprocess_texts(texts):
    processed = []

    for doc in nlp.pipe(
        texts,
        batch_size=128
    ):
        words = []

        for token in doc:
            if token.is_alpha:
                if token.is_stop and token.lower_ not in NEGATIONS:
                    continue

                lemma = token.lemma_.lower()

                if lemma:
                    words.append(lemma)

        processed.append(" ".join(words))

    return processed

print("Preprocessing training complaints...")
X_train_processed = preprocess_texts(X_train.tolist())

print("Preprocessing testing complaints...")
X_test_processed = preprocess_texts(X_test.tolist())

# --------------------------------------------------
# 4. Convert text into TF-IDF features
# --------------------------------------------------

print("\nBuilding TF-IDF features...")

vectorizer = TfidfVectorizer(
    max_features=30000,
    ngram_range=(1, 2),
    min_df=2,
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(X_train_processed)
X_test_tfidf = vectorizer.transform(X_test_processed)

# --------------------------------------------------
# 5. Train classifier
# --------------------------------------------------

print("\nTraining Logistic Regression model...")

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X_train_tfidf, y_train)

# --------------------------------------------------
# 6. Evaluate model
# --------------------------------------------------

print("\nEvaluating model...")

y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)

print(f"\nTest accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")

print("\nClassification report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

print("\nConfusion matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred,
        labels=model.classes_
    )
)

# --------------------------------------------------
# 7. Save model artifacts
# --------------------------------------------------

joblib.dump(vectorizer, os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib"))
joblib.dump(model, os.path.join(MODEL_DIR, "complaint_model.joblib"))

# Save category names for reference
with open(
    os.path.join(MODEL_DIR, "categories.txt"),
    "w",
    encoding="utf-8"
) as file:
    file.write("\n".join(model.classes_))

print("\nTraining complete!")
print("Saved model to:", MODEL_DIR)
print("Saved vectorizer to:", MODEL_DIR)
