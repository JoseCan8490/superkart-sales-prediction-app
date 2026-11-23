# 🛒 SuperKart Store Sales Predictor

This repository contains an end-to-end Machine Learning web application designed to predict total product sales at various SuperKart stores. 

## 🌟 Project Highlights
- **Highly Accurate Model**: Features a pre-trained **Random Forest Regressor** pipeline standardizing and predicting sales with over **92.9% R-squared accuracy** on test data.
- **Two Interactive User Interfaces**:
  1. **Streamlit Application** (`app.py`): Beautiful, user-friendly interactive sliders & inputs.
  2. **Flask Web API** (`app_flask.py`): Lightweight web form and production-grade API endpoint.
- **Containerized Deployment**: Fully configured with a root-level `Dockerfile` for universal staging.

--- 

## 🛠️ Project Structure
```bash
├── app.py                      # Streamlit application
├── app_flask.py                # Flask Web application & API alternative
├── Dockerfile                  # Production container configuration
└── backend_files/
    ├── requirements.txt        # Exact dependencies matching active environment
    └── superkart_sales_predictor_model.joblib # Serialized Random Forest pipeline
```

--- 

## 🚀 Getting Started Locally

### Method A: Running with Docker (Recommended)
Build and run the containerized app instantly on any machine running **Docker Desktop**:
```bash
# 1. Build the Docker image
docker build -t superkart-sales-app .

# 2. Run the application
docker run -d -p 8501:8501 --name superkart_container superkart-sales-app
```
Visit `http://localhost:8501` to access your Streamlit interface!

### Method B: Running via Python Environment
```bash
# 1. Install dependencies
pip install -r backend_files/requirements.txt

# 2a. Run the Streamlit App
streamlit run app.py

# 2b. Run the Flask App
python app_flask.py
```
