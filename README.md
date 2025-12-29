This is a professional, industry-standard **README.md** file. It covers everything from the system architecture to the step-by-step setup instructions. You can copy the content below and save it as `README.md` in your project's root directory.

---

# 🛡️ Movie Spoiler Detection: End-to-End MLOps Pipeline

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

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/spoiler-detection-mlops.git
cd spoiler-detection-mlops

```

### 3. Project Structure Setup

Before running the system, ensure you have your local model and data files in the correct directories:

* Place your pre-trained model files in the `./models/` folder.
* Place your raw data (e.g., `data.json`) in the `./data/` folder.

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

One of the core features of this project is the **Performance & Drift** tab on the dashboard. It calculates accuracy by comparing `ground_truth` labels with `model_predictions` in real-time.

* **Drift Detection:** If the accuracy drops over time (visualized in a line chart), it signals that the model needs retraining due to changing data patterns.
* **Error Analysis:** A Confusion Matrix is generated automatically to identify if the model is producing more False Positives (Clean reviews marked as Spoiler) or False Negatives.

 
* **Model Link**
https://drive.google.com/drive/u/1/folders/1eKVN1KP_Q1IPNz32PXhHc5QA39kBo8wc

* **Data Link**
https://drive.google.com/drive/u/1/folders/1LEFazU-hQv9QyN6ikHidbBcJpmLlFpgJ

---

