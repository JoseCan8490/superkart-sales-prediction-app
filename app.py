import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Configure page styling and title
st.set_page_config(page_title="SuperKart Sales Predictor", layout="centered")

st.title("🛒 SuperKart Store Sales Predictor")
st.write("This interactive web application predicts the total store sales of a product based on its attributes and the store profiles using our best-performing machine learning model.")

# Step 1: Load the pre-trained pipeline
@st.cache_resource
def load_model():
    # Using our serialized Base Random Forest pipeline
    return joblib.load("backend_files/superkart_sales_predictor_model.joblib")

try:
    model = load_model()
    st.success("Model loaded successfully!")
except Exception as e:
    st.error(f"Error loading the model. Please check the file path. Details: {e}")
    st.stop()

st.markdown("### Enter Product and Store Details:")

# Step 2: Set up form / sliders / inputs based on dataset metadata
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Product Properties**")
    product_weight = st.slider("Product Weight (g)", min_value=4.0, max_value=22.0, value=12.65, step=0.1)
    product_allocated_area = st.slider("Product Display Allocated Area", min_value=0.004, max_value=0.3, value=0.068, step=0.001)
    product_mrp = st.slider("Product Maximum Retail Price (MRP)", min_value=31.0, max_value=266.0, value=147.0, step=0.1)
    product_sugar_content = st.selectbox(
        "Product Sugar Content",
        options=["Low Sugar", "Regular", "No Sugar"]
    )
    product_type = st.selectbox(
        "Product Category",
        options=[
            "Fruits and Vegetables", "Snack Foods", "Frozen Foods", "Dairy", 
            "Household", "Baking Goods", "Canned", "Health and Hygiene", 
            "Meat", "Soft Drinks", "Breads", "Hard Drinks", "Others", 
            "Starchy Foods", "Breakfast", "Seafood"
        ]
    )

with col2:
    st.markdown("**Store Profile**")
    store_id = st.selectbox(
        "Store ID",
        options=["OUT004", "OUT001", "OUT003", "OUT002"]
    )
    store_size = st.selectbox(
        "Store Size",
        options=["Medium", "High", "Small"]
    )
    store_location_city_type = st.selectbox(
        "Store Location City Type",
        options=["Tier 2", "Tier 1", "Tier 3"]
    )
    store_type = st.selectbox(
        "Store Type",
        options=["Supermarket Type2", "Supermarket Type1", "Departmental Store", "Food Mart"]
    )
    store_establishment_year = st.slider(
        "Store Establishment Year", 
        min_value=1987, 
        max_value=2009, 
        value=2009, 
        step=1
    )

# Step 3: Package inputs into a DataFrame matching our features list
input_data = pd.DataFrame({
    'Product_Weight': [product_weight],
    'Product_Allocated_Area': [product_allocated_area],
    'Product_MRP': [product_mrp],
    'Store_Establishment_Year': [store_establishment_year],
    'Product_Sugar_Content': [product_sugar_content],
    'Product_Type': [product_type],
    'Store_Id': [store_id],
    'Store_Size': [store_size],
    'Store_Location_City_Type': [store_location_city_type],
    'Store_Type': [store_type]
})

# Step 4: Make prediction
if st.button("🎯 Predict Total Store Sales", use_container_width=True):
    prediction = model.predict(input_data)[0]
    st.markdown("--- ")
    st.subheader(f"Estimated Product Store Sales:")
    st.title(f"${prediction:,.2f}")
