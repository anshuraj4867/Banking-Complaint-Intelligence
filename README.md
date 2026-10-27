
# Banking Complaint Intelligence

### An Automated Text Mining Dashboard for Classifying Customer Complaints

Banking Complaint Intelligence is a machine learning-based application that automatically classifies customer complaints into relevant categories using Natural Language Processing (NLP).

The project uses spaCy, TF-IDF, and Logistic Regression to analyze complaint text and provide predicted categories with confidence scores. It also includes a Streamlit dashboard for single complaint analysis, batch complaint processing, dataset overview, and regulatory references.

This project was developed as an academic project to demonstrate the practical application of text mining and machine learning in the banking domain.

---

##  Project Overview

Banks and financial institutions receive a large number of customer complaints related to payments, credit reporting, loan services, account management, and other banking activities.

Manually reviewing and categorizing these complaints can be time-consuming.

This project provides an automated solution that helps classify customer complaints into predefined categories using machine learning techniques.

### Key Objectives

- Automate the classification of banking and financial complaints.
- Apply NLP techniques to process and analyze complaint text.
- Build a machine learning model for multi-class text classification.
- Develop an interactive dashboard using Streamlit.
- Support single complaint and batch complaint analysis.
- Display model confidence scores and predicted categories.
- Provide relevant regulatory references for informational purposes.

---

##  Features

### 1. Dataset Overview
- Displays the total number of complaints.
- Shows the number of complaint categories.
- Visualizes complaint category distribution.
- Identifies the most frequent complaint category.

### 2. Single Complaint Analysis
- Enter a customer complaint manually.
- Analyze the complaint using the trained model.
- Display the predicted complaint category.
- Show the estimated model confidence.
- Visualize the top predicted categories.

### 3. Batch Complaint Analysis
- Upload a CSV file containing multiple complaints.
- Automatically classify complaints in batches.
- View predicted categories for each complaint.
- Download the classification results.

### 4. Regulatory Reference
- Displays potentially relevant regulatory references.
- Provides information related to complaint categories.
- Includes official reference links.
- Helps users understand possible regulatory context.

### 5. Interactive Dashboard
- Simple and user-friendly interface.
- Interactive visualizations.
- Multiple analysis tabs.
- Dataset and model information.

---

##  Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive web dashboard |
| spaCy | NLP preprocessing |
| Scikit-learn | Machine learning and text classification |
| TF-IDF | Text feature extraction |
| Logistic Regression | Complaint classification |
| Pandas | Dataset processing and analysis |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Joblib | Saving and loading trained models |

---

##  Machine Learning Workflow

The project follows the following workflow:

1. Load the complaint dataset.
2. Inspect and clean the complaint data.
3. Preprocess complaint text using spaCy.
4. Convert complaint text into numerical features using TF-IDF.
5. Train a Logistic Regression classification model.
6. Evaluate the trained model using test data.
7. Save the trained model and TF-IDF vectorizer.
8. Load the saved artifacts into the Streamlit application.
9. Predict complaint categories for new inputs.

### Model Details

- **Algorithm:** Logistic Regression
- **Feature Extraction:** TF-IDF
- **Text Processing:** spaCy
- **Classification Type:** Multi-class classification
- **Number of Categories:** 10
- **Test Accuracy:** 72.17%

The model accuracy was obtained during the project's model evaluation process.

---

##  Project Structure

```text
BankingComplaintDashboard/
│
├── app.py
├── train_model.py
├── prepare_dataset.py
├── inspect_dataset.py
├── create_sample.py
├── regulations.py
│
├── requirement.txt
│
├── data/
│   ├── complaint_data.csv
│   ├── cleaned_complaints.csv
│   └── sample_complaints.csv
│
├── models/
│   ├── complaint_model.joblib
│   ├── tfidf_vectorizer.joblib
│   └── categories.txt
│
└── README.md
```

---

##  Installation and Setup

### Prerequisites

Make sure the following are installed on your system:

- Python 3.10 or compatible version
- pip
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/BankingComplaintDashboard.git
```

### Step 2: Navigate to the Project Directory

```bash
cd BankingComplaintDashboard
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

For Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
python -m pip install -r requirement.txt
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser.

If it does not open automatically, visit:

```text
http://localhost:8501
```

---

##  Model Training

To train the machine learning model again, run:

```bash
python train_model.py
```

The training process includes:

- Loading the complaint dataset.
- Preprocessing complaint text.
- Extracting TF-IDF features.
- Training the Logistic Regression model.
- Evaluating model performance.
- Saving the trained model and vectorizer.

The saved model files are stored in the `models/` directory.

**Note:** Model training requires the appropriate dataset to be available locally.

---

##  Application Testing

The application was tested using the following test cases:

| Test Case | Description | Status |
|---|---|---|
| Test 1 | Single complaint classification | PASS |
| Test 2 | Classification of a different complaint | PASS |
| Test 3 | Batch complaint analysis | PASS |
| Test 4 | Download classification results | PASS |
| Test 5 | Regulatory reference display | PASS |
| Test 6 | Dataset overview | PASS |

All six application tests were completed successfully.

---

##  Application Screenshots

The application includes the following dashboard sections:

### Dataset Overview
Displays complaint statistics and category distribution.

### Single Complaint Analysis
Allows users to enter complaint text and view the predicted category.

### Batch Analysis
Supports processing multiple complaints using a CSV file.

### Regulatory Reference
Displays relevant regulatory information associated with complaint categories.

*Screenshots can be added to this README after uploading them to the repository.*

---

##  Limitations

- The model depends on the quality and representativeness of the training dataset.
- Predictions may not always be correct.
- Some complaints may contain multiple issues that are difficult to classify into a single category.
- Model confidence represents an estimated probability, not a guarantee of correctness.
- Regulatory references are informational and do not establish a legal violation.
- The application is an academic prototype and is not intended to replace professional banking, compliance, or legal review.

---

##  Future Enhancements

Possible future improvements include:

- Improving classification accuracy through advanced NLP models.
- Adding more complaint categories.
- Supporting multilingual complaint classification.
- Integrating explainable AI techniques.
- Adding complaint priority and severity detection.
- Developing real-time complaint monitoring.
- Integrating with banking complaint management systems.

---

##  Academic Project

**Project Title:** An Automated Text Mining Dashboard for Classifying Customer Complaints for Banking Regulations using spaCy and Streamlit

**Domain:** Machine Learning, Natural Language Processing, Text Mining

**Project Type:** Academic Project

---

##  Disclaimer

This project is developed for academic and educational purposes only.

The predictions and regulatory references provided by the application are informational. They should not be treated as professional legal advice, official regulatory decisions, or final determinations of complaint validity.

---

## ⭐ Acknowledgement

This project demonstrates the application of machine learning and natural language processing techniques to a practical problem in the banking and financial services domain.
