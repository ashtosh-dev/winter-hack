# 🛡️ GHOST-SHIELD AI

**GHOST-SHIELD AI** is an intelligent supply-chain monitoring system designed to detect "Ghost Demand"—anomalous spikes in demand forecasts that don't translate to real sales—preventing invisible losses, reducing waste, and optimizing production costs.

## 🚀 Key Features

- **Anomaly Detection**: Uses **Isolation Forest** to identify abnormal demand patterns and forecast errors.
- **Production Optimization**: Leverages **Google OR-Tools** to prescribe production cuts that minimize overproduction costs and waste.
- **Interactive Dashboard**: A **Streamlit**-based cockpit for real-time monitoring of SKU-level alerts and global savings.
- **Cloud scale**: Integrated with **Google BigQuery** for scalable data processing and storage.
- **Explainability**: provides clear reasoning for every alert triggered (volatility, forecast spikes, etc.).

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Machine Learning**: Scikit-learn (Isolation Forest)
- **Mathematical Optimization**: Google OR-Tools (Linear Programming)
- **Data Warehousing**: Google BigQuery
- **Data Engineering**: Pandas, NumPy
- **Visualization**: Plotly Express

## 📂 Project Structure

```text
├── app.py              # Main Streamlit Dashboard
├── src/                # Core Logic Modules
│   ├── ml_model.py      # Ghost demand detection (Isolation Forest)
│   ├── optimization.py  # Production cut optimization (OR-Tools)
│   ├── explainability.py # Alert reasoning logic
│   ├── feature_engineering.py # Rolling stats and volatility metrics
│   └── data_cleaning.py  # Data preprocessing
├── notebooks/          # Exploratory Data Analysis & Research
├── data/               # Local data assets
├── requirements.txt    # Project dependencies
└── .env                # Environment variables
```

## ⚙️ Setup & Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ashtosh-dev/winter-hack.git
   cd winter-hack
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   - Create a `.env` file or set environment variables for Google Cloud credentials.
   - Ensure you have a service account JSON with access to BigQuery.

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## 📊 How it Works

1. **Data Ingestion**: Sales and forecast data are pulled from BigQuery.
2. **Feature Engineering**: The system calculates rolling means, standard deviations, and volatility ratios to capture the "rhythm" of demand.
3. **Detection**: The `ml_model` identifies records where the forecast deviates significantly from historical patterns without corresponding sales support.
4. **Optimization**: For every "Ghost" case, the `optimization` engine calculates the most cost-effective production reduction.
5. **Visualization**: All metrics are aggregated into the dashboard for executive and operational review.

---
*Developed during Winter Hackathon.*
