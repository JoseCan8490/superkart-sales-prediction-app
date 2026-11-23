from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load the best-performing pipeline
MODEL_PATH = "backend_files/superkart_sales_predictor_model.joblib"
model = joblib.load(MODEL_PATH)

# Basic HTML layout for our web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SuperKart Sales Predictor (Flask)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f7f6; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h2 { color: #333; text-align: center; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; background: #e2f0d9; border: 1px solid #95c17e; border-radius: 4px; text-align: center; font-size: 18px; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🛒 SuperKart Store Sales Predictor</h2>
        <form id="predictionForm">
            <div class="form-group">
                <label>Product Weight (g):</label>
                <input type="number" name="Product_Weight" step="0.01" value="12.65" required>
            </div>
            <div class="form-group">
                <label>Product Display Allocated Area:</label>
                <input type="number" name="Product_Allocated_Area" step="0.001" value="0.068" required>
            </div>
            <div class="form-group">
                <label>Product Maximum Retail Price (MRP):</label>
                <input type="number" name="Product_MRP" step="0.1" value="147.0" required>
            </div>
            <div class="form-group">
                <label>Product Sugar Content:</label>
                <select name="Product_Sugar_Content">
                    <option value="Low Sugar">Low Sugar</option>
                    <option value="Regular">Regular</option>
                    <option value="No Sugar">No Sugar</option>
                </select>
            </div>
            <div class="form-group">
                <label>Product Category:</label>
                <select name="Product_Type">
                    <option value="Fruits and Vegetables">Fruits and Vegetables</option>
                    <option value="Snack Foods">Snack Foods</option>
                    <option value="Frozen Foods">Frozen Foods</option>
                    <option value="Dairy">Dairy</option>
                    <option value="Household">Household</option>
                </select>
            </div>
            <div class="form-group">
                <label>Store ID:</label>
                <select name="Store_Id">
                    <option value="OUT004">OUT004</option>
                    <option value="OUT001">OUT001</option>
                    <option value="OUT003">OUT003</option>
                    <option value="OUT002">OUT002</option>
                </select>
            </div>
            <div class="form-group">
                <label>Store Size:</label>
                <select name="Store_Size">
                    <option value="Medium">Medium</option>
                    <option value="High">High</option>
                    <option value="Small">Small</option>
                </select>
            </div>
            <div class="form-group">
                <label>Store Location City Type:</label>
                <select name="Store_Location_City_Type">
                    <option value="Tier 2">Tier 2</option>
                    <option value="Tier 1">Tier 1</option>
                    <option value="Tier 3">Tier 3</option>
                </select>
            </div>
            <div class="form-group">
                <label>Store Type:</label>
                <select name="Store_Type">
                    <option value="Supermarket Type2">Supermarket Type2</option>
                    <option value="Supermarket Type1">Supermarket Type1</option>
                    <option value="Departmental Store">Departmental Store</option>
                    <option value="Food Mart">Food Mart</option>
                </select>
            </div>
            <div class="form-group">
                <label>Store Establishment Year:</label>
                <input type="number" name="Store_Establishment_Year" value="2009" required>
            </div>
            <button type="submit">🎯 Predict Total Store Sales</button>
        </form>
        <div class="result" id="resultDiv"></div>
    </div>

    <script>
        document.getElementById('predictionForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = isNaN(value) || value === '' ? value : parseFloat(value);
            });
            
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();
            const resultDiv = document.getElementById('resultDiv');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = `<strong>Estimated Product Store Sales:</strong><br><span style="font-size: 24px;">$${result.prediction.toFixed(2)}</span>`;
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    req_data = request.get_json()
    input_df = pd.DataFrame([req_data])
    
    # Generate prediction using our pipeline
    pred = model.predict(input_df)[0]
    return jsonify({'prediction': float(pred)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
