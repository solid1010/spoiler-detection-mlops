

# 🛡️ Spoiler Detection on IMDB Reviews: End-to-End MLOps Pipeline

This project implements a fully automated **MLOps pipeline** designed to detect spoilers in movie reviews. It leverages a containerized architecture to handle data ingestion, model inference, and real-time performance monitoring.

## 🚀 Key Features

* **Automated Data Ingestion:** Uses Apache Airflow to simulate real-time data traffic from a local JSON source.
* **Containerized Microservices:** Every component (Database, Orchestrator, Dashboard) runs in an isolated Docker container.
* **Real-Time Monitoring:** A Streamlit dashboard tracks **Model Drift**, accuracy, and spoiler density.
* **Scalable Architecture:** Designed with industry-standard tools for easy deployment and scaling.

---

## 🛠️ Tech Stack

* **Orchestration:** [Apache Airflow](https://airflow.apache.org/)
* **Database:** [PostgreSQL](https://www.postgresql.org/)
* **Dashboard:** [Streamlit](https://streamlit.io/)
* **Model:** [Hugging Face Transformers](https://huggingface.co/) (DistilBERT)
* **Versioning & Tracking:** [DVC](https://dvc.org/) (Data/Model) & [MLflow](https://mlflow.org/) (Experiments)
* **Containerization:** [Docker](https://www.docker.com/) & Docker Compose
* **Language:** Python 3.8+

---

## 📐 System Architecture



The system consists of three main services connected via a dedicated Docker network:

1. **PostgreSQL:** The central repository for storing reviews, actual labels, and model predictions.
2. **Airflow:** The "brain" of the project. It schedules the simulator script and triggers the inference model.
3. **Streamlit:** The "Command Center" that visualizes performance metrics and allows for live inference testing.

---

## 🏁 Getting Started (Step-by-Step)

### 1. Prerequisites

Ensure you have the following installed:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* Git
* DVC (Data Version Control)

### 2. Clone the Repository

```bash
git clone [https://github.com/solid1010/spoiler-detection-mlops.git](https://github.com/solid1010/spoiler-detection-mlops.git)
cd spoiler-detection-mlops

```

### 3. Data & Model Management (DVC)

This project uses **DVC** to manage large datasets and model artifacts. To pull the required data and model files from the remote storage (Google Drive), run:

```bash
dvc pull

```

> **Note:** This step will populate the `./data/` and `./models/` (or `mlruns`) directories. Ensure you have the necessary access permissions for the DVC remote.

### 4. Build and Launch

Run the following command to build the images and start all services:

```bash
docker-compose up -d --build

```

### 5. Accessing the Services

Once the containers are running, you can access the interfaces via your browser:

* **Apache Airflow (Scheduler):** `http://localhost:8080` (Default Login: `airflow` / `airflow`)
* **Streamlit Dashboard:** `http://localhost:8501`

---

## 📊 Monitoring & Model Drift

The **Performance & Drift** tab on the dashboard calculates accuracy by comparing `ground_truth` labels with `model_predictions` in real-time.

* **Drift Detection:** Visualizes accuracy over time to signal when the model needs retraining due to changing data patterns.
* **Error Analysis:** Automatically generates a Confusion Matrix to identify False Positives and False Negatives.

---

## 🔗 Project Assets (Manual Access)

* **Model Storage:** [Google Drive Link](https://drive.google.com/drive/u/1/folders/1eKVN1KP_Q1IPNz32PXhHc5QA39kBo8wc)
* **Dataset Source:** [Google Drive Link](https://drive.google.com/drive/u/1/folders/1LEFazU-hQv9QyN6ikHidbBcJpmLlFpgJ)


