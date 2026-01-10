# Ghost Demand Detection

This project focuses on identifying "Ghost Demand" (anomalous demand patterns) in e-commerce sales data using machine learning techniques.

## Overview

The primary goal is to perform anomaly detection on sales records to identify unusual fluctuations in demand that might indicate supply chain issues, data errors, or significant market shifts.

## Data Source

The project utilizes the `Amazon Sale Report.csv` dataset, which contains detailed transaction records, including:
- Order IDs
- Dates
- SKU details
- Quantities
- Order Status

## Notebooks

The core analysis and modeling are performed in the following notebook:

### [01_data_exploration.ipynb](notebooks/01_data_exploration.ipynb)
- **Data Loading & Cleaning**: Initial ingestion of the Amazon sales report and basic preprocessing.
- **Aggregation**: Converting order-level data into daily SKU-level demand time series.
- **Feature Engineering**: Creating rolling averages, standard deviations, and volatility ratios to capture demand patterns.
- **Anomaly Detection**: Training an **Isolation Forest** model to detect outliers in the demand signal.
- **Visualization**: Detailed plots and statistical summaries of detected anomalies.

## Getting Started

### Prerequisites

Ensure you have Python installed and the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Project

Open the Jupyter notebook to explore the analysis:

```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```
