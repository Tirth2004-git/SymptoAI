# 🏥 SymptoAI: Disease Prediction from Symptoms

SymptoAI is a comprehensive machine learning project and interactive web portal designed to predict potential health conditions based on user-selected symptoms. Built with a sleek, glassmorphic frontend and a robust Python backend, the system explores and evaluates four distinct machine learning classifiers to determine the most accurate prediction.

---

## 📋 Table of Contents
1. [Architecture & Web App Overview](#-architecture--web-app-overview)
2. [Key Features](#-key-features)
3. [Project Directory Structure](#-project-directory-structure)
4. [Machine Learning Details](#-machine-learning-details)
5. [Dataset Specifications](#-dataset-specifications)
6. [Installation & Environment Setup](#-installation--environment-setup)
7. [How to Run](#-how-to-run)
8. [Configuration Guide (`config.yaml`)](#-configuration-guide-configyaml)
9. [⚠️ Medical Disclaimer](#%EF%B8%8F-medical-disclaimer)

---

## 🌐 Architecture & Web App Overview

SymptoAI bridges the gap between machine learning model evaluation and real-world user interaction through a dual-layered architecture:

1. **The Machine Learning Pipeline (`main.py`)**: Responsible for loading datasets, running data sanity assertions, computing feature correlation, splitting data into training and validation sets, training four separate classifier models, evaluating them with metrics (accuracy, confusion matrix, cross-validation score), and serializing the trained models.
2. **The Flask Web Portal (`app.py`)**: An interactive REST API and frontend server. It loads the pre-trained models on startup and serves a modern, responsive web application where users can search, filter, select symptoms, and send requests to the backend for real-time inference.

---

## ✨ Key Features

### 🖥️ Interactive Web Portal
* **Glassmorphic UI**: Designed using modern glassmorphism styling, clean custom typography, CSS gradients, and fluid micro-animations.
* **Smart Search & Autocomplete**: Quickly search through 132 different symptoms with real-time matching suggestions.
* **System Categorization Filters**: Browse symptoms categorized into systems (e.g., *Skin & Nails*, *Respiratory / Cold*, *Gastrointestinal*, *Brain & Senses*, and more) using active pill filters.
* **On-the-Fly Model Comparison**: Test and compare prediction outputs across four different AI classifiers in real-time.
* **Confidence Metric**: Displays prediction confidence scores based on model class probabilities (for models supporting `predict_proba`).

### ⚙️ Robust Backend & Modeling
* **Multi-Algorithm Evaluation**: Full support for Random Forest, Decision Tree, Naive Bayes (MNB), and Gradient Boosting.
* **Configurable Environment**: Adjust hyper-parameters, data splits, and file paths using a centralized config file (`config.yaml`).
* **CLI Inference Engine**: Simple script (`infer.py`) to run predictions from console/terminal with customized input dictionaries.
* **Jupyter Interactive Playgrounds**: A notebook (`demo.ipynb`) and check-point notebook (`notebook/Disease-Prediction-from-Symptoms-checkpoint.ipynb`) to explore data correlation and tree construction visually.

---

## 📂 Project Directory Structure

```text
├── .github/
│   └── workflows/
│       └── greetings.yml        # GitHub Actions greeting workflow
├── dataset/
│   ├── training_data.csv        # Primary training data (132 symptoms, 4920 entries)
│   └── test_data.csv            # Held-out testing dataset
├── notebook/
│   ├── dataset/
│   │   ├── raw_data.xlsx        # Raw Columbia University KB dataset
│   │   └── cleaned_data.csv     # Cleaned Columbia KB data
│   ├── Disease-Prediction-from-Symptoms-checkpoint.ipynb  # Interactive playground notebook
│   └── tree.dot                 # Decision Tree visualization export
├── saved_model/                 # Target folder for serialized joblib models
│   ├── decision_tree.joblib
│   ├── gradient_boost.joblib
│   ├── mnb.joblib
│   └── random_forest.joblib
├── static/                      # Web portal static assets
│   ├── css/
│   │   └── style.css            # Custom CSS styling (gradients, animations, grid layouts)
│   └── js/
│       └── main.js              # Frontend logic (symptom loading, filtering, search, API request)
├── templates/
│   └── index.html               # Main Flask web portal layout
├── .gitignore                   # Version control exclusions
├── app.py                       # Flask server entrypoint (defines REST API & category mapping)
├── config.yaml                  # Unified project config file
├── demo.ipynb                   # Jupyter notebook for quick testing & visual execution
├── environment.yml              # Conda environment dependency specifier
├── feature_correlation.png      # Generated feature heatmap visualization
├── infer.py                     # CLI quick-inference script
├── main.py                      # Main training pipeline runner
└── requirements.txt             # Pip dependencies file
```

---

## 🧠 Machine Learning Details

### Explored Algorithms

SymptoAI trains and compares four distinct machine learning classifiers:

1. **Random Forest Classifier**: An ensemble classifier using bagging of decision trees. (Recommended model for best overall performance and robustness).
2. **Gradient Boosting Classifier**: An ensemble boosting technique that iteratively constructs trees to minimize prediction residuals.
3. **Multinomial Naive Bayes (MNB)**: A probabilistic classifier based on Bayes' theorem, ideal for binary classification matrices.
4. **Decision Tree Classifier**: An entropy-based decision tree that recursively splits nodes to maximize information gain.

### Data Split & Feature Correlation
* **Validation Split**: Features are split using `validation_size` (default is 33%) set in `config.yaml` to assess accuracy.
* **Correlation Heatmap**: The pipeline computes the Pearson correlation matrix for the symptoms, exporting it automatically as `feature_correlation.png` using Seaborn to visualize symptom co-occurrences.

---

## 📊 Dataset Specifications

### Dataset 1: Kaggle Disease Prediction (Default)
Used with `main.py`, `app.py`, and `infer.py`.
* **Path**: `dataset/training_data.csv` & `dataset/test_data.csv`
* **Features**: 132 binary indicators representing different symptoms (1 if symptom is present, 0 otherwise).
* **Target**: `prognosis` (contains 41 target categories of diseases/conditions).

### Dataset 2: Columbia University KB (Notebook Experiment)
Used inside the Jupyter Notebook.
* **Path**: `notebook/dataset/raw_data.xlsx`
* **Structure**: 3 columns representing `Disease`, `Count of Disease Occurrence`, and `Symptom`.

---

## 🛠️ Installation & Environment Setup

Ensure you have **Python 3.8+** installed. You can set up the project using either `pip` or `conda`.

### Option A: Using pip (Recommended)
1. Navigate to the project root directory:
   ```bash
   cd Disease-Prediction-from-Symptoms-master
   ```
2. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Option B: Using Conda
1. Create the environment from `environment.yml`:
   ```bash
   conda env create -f environment.yml
   ```
2. Activate the newly created environment:
   ```bash
   conda activate MachineLearning
   ```

---

## 🚀 How to Run

Follow these steps to train models and start utilizing the predictions:

### Step 1: Train the Machine Learning Models
You must train the models first to generate the `.joblib` model binaries inside the `saved_model/` folder.
```bash
python main.py
```
This script will:
* Load training and test CSV datasets.
* Compute and save `feature_correlation.png`.
* Train and evaluate all 4 algorithms.
* Print training accuracy, validation predictions, confusion matrices, cross-validation scores, and classification reports.
* Serialize the trained models to the `./saved_model/` directory.

### Step 2: Launch the Flask Web Portal
Start the interactive UI dashboard:
```bash
python app.py
```
* Once started, open your web browser and navigate to: **`http://127.0.0.1:5000/`**
* Search, select symptoms, pick your model, and click **Analyze Symptoms** to get predictions.

### Step 3: Run Command-Line Inference
Run a quick, custom command-line check using the pre-selected symptoms defined in `infer.py`:
```bash
python infer.py
```

### Step 4: Run the Jupyter Notebook
Open the interactive demo inside a Jupyter environment:
```bash
jupyter notebook demo.ipynb
```

---

## ⚙️ Configuration Guide (`config.yaml`)

The project pipeline behaviors can be customized without editing code by modifying `config.yaml`:

```yaml
# Control randomness of the dataset splits
random_state: 101

# Print verbose metrics during training runs (True/False)
verbose: True

# Dataset Paths and validation parameters
dataset:
  training_data_path: './dataset/training_data.csv'
  test_data_path: './dataset/test_data.csv'
  validation_size: 0.33     # Fraction of data reserved for validation (33%)

# Hyper-parameter configurations for classifier engines
model:
  decision_tree:
    criterion: 'entropy'
  random_forest:
    n_estimators: 10
  gradient_boost:
    n_estimators: 150
    criterion: 'friedman_mse'

# Path to save serialized models
model_save_path: './saved_model/'
```

---

## ⚠️ Medical Disclaimer

> [!WARNING]
> SymptoAI is developed for demo, educational, and research purposes only. It is **not** a diagnostic tool, does **not** provide clinical guidance, and should **not** replace a professional consultation with a qualified healthcare practitioner. Always seek the advice of a medical professional for any symptoms or health concerns.
