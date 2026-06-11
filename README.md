# 🦈 Shark Attack Predictive Pipeline: End-to-End Data Science System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Machine Learning](https://img.shields.io/badge/ML-Random%20Forest-green)](https://scikit-learn.org/)
[![Database](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)](https://www.sqlite.org/)

A professional-grade Data Science pipeline analyzing over **150 years of global shark attack data**. This project demonstrates a complete engineering lifecycle: from raw data ingestion and cleaning to predictive modeling and deployment via an interactive dashboard.

## 🚀 Overview

The **Shark Attack Predictive Pipeline** is not just a analysis script; it’s a robust system designed to handle messy historical data and provide actionable safety insights. By utilizing a **Random Forest Fatality Predictor**, the system estimates the likelihood of a fatal outcome based on geographical, temporal, and activity-based features.

## ✨ Key Features

- **End-to-End Pipeline**: Automates data ingestion (`ingest_data.py`), cleaning (`convert_data.py`), and visualization.
- **Predictive Engine**: A trained Random Forest model (`fatality_predictor.pkl`) that predicts incident outcomes with high accuracy.
- **SQL Backend**: Stores processed data in a structured SQLite database (`master_sharks.db`) for high-performance querying.
- **Interactive Dashboard**: A Streamlit-based web application (`app.py`) for real-time data exploration and prediction.
- **Scalable Architecture**: Modular Python scripts for each stage of the data lifecycle.

## 🛠 Tech Stack

- **Language**: Python
- **Libraries**: Pandas, Scikit-learn, Streamlit, Matplotlib, Seaborn
- **Storage**: SQLite3
- **Tools**: Pickle (Model Serialization)

## 📁 Repository Structure

```
├── global shark attacks/
│   ├── app.py                  # Streamlit Dashboard
│   ├── master_pipeline.py      # Core orchestration script
│   ├── ingest_data.py          # Data acquisition logic
│   ├── convert_data.py         # Data cleaning & transformation
│   ├── predict_fatality.py     # Inference engine
│   ├── fatality_predictor.pkl  # Trained ML Model
│   ├── master_sharks.db        # SQLite Database
│   └── requirements.txt        # Dependencies
└── README.md
```

## ⚙️ Installation & Usage

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/carnoba/shark-attack-predictive-pipeline.git
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r "global shark attacks/requirements.txt"
   ```
3. **Run the Dashboard**:
   ```bash
   streamlit run "global shark attacks/app.py"
   ```

## 📊 Results & Performance

The pipeline processes thousands of records, providing insights into:
- Peak attack months/seasons globally.
- Highest-risk activities (Surfing, Swimming, etc.).
- Regional fatality distributions.

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the model or add new features, please fork the repository and create a pull request.

## ⭐ Show your support

If you find this project interesting, please give it a **Star**! It helps others discover the work.

---
**Maintained by [Carnoba](https://github.com/carnoba)**

#Tags
#DataScience #MachineLearning #Python #Streamlit #SharkAttacks #PredictiveModeling #DataEngineering #RandomForest #Analytics
