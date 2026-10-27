
from pathlib import Path

import joblib
import pandas as pd
import spacy
import streamlit as st

from regulations import get_regulatory_reference


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Banking Complaint Intelligence",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Banking Complaint Intelligence")
st.caption(
    "Automated Text Mining Dashboard for Classifying Customer Complaints"
)


# ==========================================================
# 2. PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "cleaned_complaints.csv"
MODEL_DIR = BASE_DIR / "models"

MODEL_FILE = MODEL_DIR / "complaint_model.joblib"
VECTORIZER_FILE = MODEL_DIR / "tfidf_vectorizer.joblib"


# ==========================================================
# 3. LOAD MODEL, VECTORIZER AND SPACY
# ==========================================================

@st.cache_resource
def load_resources():
    model = joblib.load(MODEL_FILE)
    vectorizer = joblib.load(VECTORIZER_FILE)

    nlp = spacy.load(
        "en_core_web_sm",
        disable=["parser", "ner"]
    )

    return model, vectorizer, nlp


try:
    model, vectorizer, nlp = load_resources()

except Exception as error:
    st.error(f"Unable to load the trained resources: {error}")
    st.info(
        "Check the models folder and run train_model.py if necessary."
    )
    st.stop()


# ==========================================================
# 4. TEXT PREPROCESSING
# Must match the training preprocessing
# ==========================================================

NEGATIONS = {"no", "not", "never", "n't"}


def preprocess_texts(texts):
    processed_texts = []

    for doc in nlp.pipe(texts, batch_size=128):
        words = []

        for token in doc:
            if not token.is_alpha:
                continue

            if token.is_stop and token.lower_ not in NEGATIONS:
                continue

            lemma = token.lemma_.lower()

            if lemma:
                words.append(lemma)

        processed_texts.append(" ".join(words))

    return processed_texts


# ==========================================================
# 5. DATASET OVERVIEW
# ==========================================================

st.sidebar.header("About this project")

st.sidebar.write(
    "An automated text mining application for classifying "
    "customer complaints using spaCy and machine learning."
)

st.sidebar.write("Model: Logistic Regression")
st.sidebar.write(f"Number of categories: {len(model.classes_)}")

st.sidebar.caption(
    "Academic prototype. Predictions require human review."
)


@st.cache_data
def load_dataset_summary(file_path):
    data = pd.read_csv(
        file_path,
        usecols=["complaint", "category"]
    )

    data = data.dropna(subset=["complaint", "category"])

    data["complaint"] = data["complaint"].astype(str).str.strip()
    data["category"] = data["category"].astype(str).str.strip()

    data = data[
        data["complaint"].ne("")
        & data["category"].ne("")
    ]

    return data


st.subheader("Dataset Overview")

if DATA_FILE.exists():

    try:
        overview_df = load_dataset_summary(str(DATA_FILE))

        category_counts = overview_df["category"].value_counts()

        total_complaints = len(overview_df)
        total_categories = overview_df["category"].nunique()

        most_common_category = (
            category_counts.index[0]
            if not category_counts.empty
            else "Not available"
        )

        col1, col2, col3 = st.columns([1, 1, 2])

        col1.metric(
            "Total Complaints",
            f"{total_complaints:,}"
        )

        col2.metric(
            "Complaint Categories",
            total_categories
        )

        col3.metric(
            "Most Frequent Category",
            most_common_category
        )

        st.subheader("Complaint Category Distribution")

        chart_df = category_counts.rename_axis(
            "Category"
        ).reset_index(name="Number of Complaints")

        st.bar_chart(
            chart_df.set_index("Category"),
            y="Number of Complaints"
        )

    except Exception as error:
        st.warning(f"Could not load dataset analytics: {error}")

else:
    st.warning(
        "Cleaned dataset not found at data/cleaned_complaints.csv."
    )


# ==========================================================
# 6. DASHBOARD TABS
# ==========================================================

tab_single, tab_batch, tab_about = st.tabs(
    [
        "Single Complaint",
        "Batch Analysis",
        "About & Limitations"
    ]
)


# ==========================================================
# 7. SINGLE COMPLAINT CLASSIFICATION
# ==========================================================

with tab_single:

    st.subheader("Classify a Customer Complaint")

    complaint = st.text_area(
        "Enter complaint text",
        placeholder=(
            "Example: I was charged twice for my monthly "
            "loan payment and have not received a refund."
        ),
        height=150,
        key="single_complaint"
    )

    if st.button("Analyze Complaint", type="primary"):

        if not complaint.strip():

            st.warning("Please enter a complaint first.")

        else:

            with st.spinner("Analyzing complaint..."):

                cleaned_text = preprocess_texts([complaint])

                features = vectorizer.transform(cleaned_text)

                prediction = model.predict(features)[0]

                probabilities = model.predict_proba(features)[0]

                confidence = float(probabilities.max())

            st.success("Classification completed!")

            result_col1, result_col2 = st.columns(2)

            with result_col1:
                st.metric(
                    "Predicted Category",
                    prediction
                )

            with result_col2:
                st.metric(
                    "Model Confidence",
                    f"{confidence:.1%}"
                )

            st.caption(
                "Confidence is the model's estimated probability, "
                "not a guarantee that the prediction is correct."
            )

            # ----------------------------------------------
            # TOP FIVE PREDICTED CATEGORIES
            # ----------------------------------------------

            st.subheader("Top Predicted Categories")

            ranking = sorted(
                zip(model.classes_, probabilities),
                key=lambda item: item[1],
                reverse=True
            )[:5]

            ranking_df = pd.DataFrame(
                ranking,
                columns=[
                    "Category",
                    "Estimated Probability"
                ]
            )

            st.bar_chart(
                ranking_df.set_index("Category")
            )

            # ----------------------------------------------
            # REGULATORY REFERENCE
            # ----------------------------------------------

            st.divider()

            st.subheader("Regulatory Reference")

            reference = get_regulatory_reference(prediction)

            if reference:

                st.write(
                    "**Relevant topic:**",
                    reference["topic"]
                )

                st.write(
                    "**Jurisdiction:**",
                    reference["jurisdiction"]
                )

                st.write(
                    "**Reference:**",
                    reference["reference"]
                )

                st.write(reference["explanation"])

                st.link_button(
                    "Open Official Reference",
                    reference["url"]
                )

            else:

                st.info(
                    "No mapped regulatory reference is available "
                    "for this predicted category."
                )

            st.caption(
                "This mapping is informational only. A complaint "
                "category does not establish a regulatory violation. "
                "Applicability depends on the facts and jurisdiction."
            )


# ==========================================================
# 8. BATCH COMPLAINT CLASSIFICATION
# ==========================================================

with tab_batch:

    st.subheader("Analyze Multiple Complaints")

    st.write(
        "Upload a CSV containing a 'complaint' column or a "
        "'Consumer complaint narrative' column."
    )

    uploaded_file = st.file_uploader(
        "Upload complaints CSV",
        type=["csv"],
        key="batch_file"
    )

    if uploaded_file is not None:

        try:

            batch_df = pd.read_csv(uploaded_file)

            possible_columns = [
                "complaint",
                "Consumer complaint narrative"
            ]

            text_column = next(
                (
                    column
                    for column in possible_columns
                    if column in batch_df.columns
                ),
                None
            )

            if text_column is None:

                st.error(
                    "The CSV must contain a 'complaint' or "
                    "'Consumer complaint narrative' column."
                )

            else:

                total_uploaded = len(batch_df)

                st.write(
                    f"Uploaded rows: {total_uploaded:,}"
                )

                MAX_ROWS = 10000

                if total_uploaded > MAX_ROWS:

                    st.warning(
                        f"For this prototype, upload at most "
                        f"{MAX_ROWS:,} rows at a time."
                    )

                else:

                    if st.button("Classify All Complaints"):

                        valid_mask = (
                            batch_df[text_column].notna()
                            & batch_df[text_column]
                            .astype(str)
                            .str.strip()
                            .ne("")
                        )

                        valid_texts = (
                            batch_df.loc[valid_mask, text_column]
                            .astype(str)
                            .tolist()
                        )

                        results = batch_df.copy()

                        results["Predicted Category"] = pd.NA
                        results["Model Confidence"] = pd.NA

                        if valid_texts:

                            with st.spinner(
                                "Classifying complaints..."
                            ):

                                processed_texts = preprocess_texts(
                                    valid_texts
                                )

                                features = vectorizer.transform(
                                    processed_texts
                                )

                                predictions = model.predict(features)

                                probabilities = model.predict_proba(
                                    features
                                )

                                confidences = probabilities.max(axis=1)

                            results.loc[
                                valid_mask,
                                "Predicted Category"
                            ] = predictions

                            results.loc[
                                valid_mask,
                                "Model Confidence"
                            ] = confidences

                            st.success(
                                "Batch classification completed!"
                            )

                            st.metric(
                                "Complaints Classified",
                                len(valid_texts)
                            )

                            st.subheader("Classification Results")

                            st.dataframe(
                                results.head(100),
                                use_container_width=True
                            )

                            st.caption(
                                "The table displays up to 100 rows. "
                                "The downloaded CSV contains all results."
                            )

                            st.subheader(
                                "Predicted Category Distribution"
                            )

                            category_distribution = (
                                results.loc[
                                    valid_mask,
                                    "Predicted Category"
                                ].value_counts()
                            )

                            st.bar_chart(category_distribution)

                        else:

                            st.warning(
                                "No non-empty complaints were found "
                                "in the uploaded file."
                            )

                        csv_data = results.to_csv(
                            index=False
                        ).encode("utf-8-sig")

                        st.download_button(
                            label="Download Results CSV",
                            data=csv_data,
                            file_name="classified_complaints.csv",
                            mime="text/csv"
                        )

        except Exception as error:

            st.error(
                f"Could not process the uploaded CSV: {error}"
            )


# ==========================================================
# 9. ABOUT AND LIMITATIONS
# ==========================================================

with tab_about:

    st.subheader("Project Methodology")

    st.markdown("""
    **Text processing:** spaCy English NLP pipeline

    **Feature extraction:** TF-IDF

    **Classification algorithm:** Logistic Regression

    **Evaluation:** Held-out test data, accuracy, precision,
    recall, F1-score and confusion matrix

    **Training dataset:** Consumer financial complaint data,
    prepared as 19,978 records before the model's train/test split.

    **Previously measured test accuracy:** 72.17%
    """)

    st.subheader("Regulatory Scope")

    st.write(
        "The current dataset contains US consumer financial "
        "complaint categories. The regulatory-reference mapping "
        "uses US consumer-protection resources."
    )

    st.warning(
        "The model does not independently determine whether a "
        "bank or financial institution has violated a regulation. "
        "Predictions and reference mappings require human review. "
        "They should not be used as legal advice or as the sole "
        "basis for regulatory decisions."
    )


# ==========================================================
# 10. FOOTER
# ==========================================================

st.divider()

st.caption(
    "Banking Complaint Intelligence | Academic Project Prototype"
)
