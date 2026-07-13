from flask import Flask, render_template_string, request
import joblib  # Alternatively: import pickle as pkl
import numpy as np
import os

print("Current directory:", os.getcwd())
print("Files:", os.listdir())

app = Flask(__name__)

# ---------------------------------------------------------
# 1. Load the Machine Learning Model
# ---------------------------------------------------------
try:
    # Ensure 'credit_card_model.pkl' is in the same directory as this script
    model = joblib.load('credit_card_model.pkl')
except Exception as e:
    print(f"Warning: Model file could not be loaded ({e}). Running in simulation mode.")
    model = None

# ---------------------------------------------------------
# 2. Categorical Encoders (Match your training preprocessing)
# ---------------------------------------------------------
INCOME_TYPE_MAP = {
    'Working': 0,
    'Commercial Associate': 1,
    'Pensioner': 2
}

EDUCATION_TYPE_MAP = {
    'Graduate': 0,
    'Post Graduate': 1,
    'High School': 2
}

# ---------------------------------------------------------
# 3. Monolithic Embedded HTML Templates
# ---------------------------------------------------------
# Global CSS styles applied across all templates
COMMON_STYLE = """
<style>
    body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f7f6; padding: 40px; text-align: center; color: #333; }
    .card, .container, .result-card { background: white; max-width: 550px; margin: auto; padding: 35px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: left; }
    h2 { margin-top: 0; color: #007BFF; text-align: center; }
    .btn { display: block; text-align: center; padding: 12px; background: #007BFF; color: white; text-decoration: none; border-radius: 4px; font-weight: bold; margin-top: 20px; border: none; width: 100%; cursor: pointer; font-size: 16px; }
    .btn:hover { background: #0056b3; }
    .input-box { margin-bottom: 20px; display: flex; flex-direction: column; }
    label { margin-bottom: 8px; font-weight: bold; color: #444; }
    input, select { padding: 11px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; width: 100%; box-sizing: border-box; }
    .Approved { color: #28a745; font-size: 26px; font-weight: bold; text-align: center; margin: 20px 0; }
    .Rejected { color: #dc3545; font-size: 26px; font-weight: bold; text-align: center; margin: 20px 0; }
    .btn-back { display: inline-block; margin-top: 25px; text-decoration: none; color: #007BFF; font-weight: bold; }
</style>
"""

HOME_HTML = COMMON_STYLE + """
<div class="card">
    <h2>Credit Card Approval Prediction</h2>
    <p>Welcome! This intelligence system evaluates prospective credit line risks instantly based on core demographics and incoming application statements.</p>
    <a href="/predict" class="btn">Access Prediction Form</a>
</div>
"""

INDEX_HTML = COMMON_STYLE + """
<div class="container">
    <h2>Application Evaluation Form</h2>
    <form action="/predict" method="POST">
        
        <div class="input-box">
            <label>Applicant Name</label>
            <input type="text" name="applicant_name" placeholder="Enter applicant name" required>
        </div>

        <div class="input-box">
            <label>Income Type</label>
            <select name="income_type" required>
                <option value="Working">Working</option>
                <option value="Commercial Associate">Commercial Associate</option>
                <option value="Pensioner">Pensioner</option>
            </select>
        </div>

        <div class="input-box">
            <label>Education Type</label>
            <select name="education_type" required>
                <option value="Graduate">Graduate</option>
                <option value="Post Graduate">Post Graduate</option>
                <option value="High School">High School</option>
            </select>
        </div>

        <div class="input-box">
            <label>Annual Income</label>
            <input type="number" name="annual_income" placeholder="Enter income" step="any" required>
        </div>

        <button type="submit" class="btn" style="background: #28a745;">Submit Application</button>
    </form>
</div>
"""

RESULT_HTML = COMMON_STYLE + """
<div class="result-card">
    <h2>Evaluation Result</h2>
    <p>Applicant Profile: <strong>{{ name }}</strong></p>
    <p style="text-align: center; margin-bottom: 5px;">Decision Strategy Status:</p>
    <div class="{{ result }}">{{ result }}</div>
    <div style="text-align: center;">
        <a href="/predict" class="btn-back">← Evaluate Another Applicant</a>
    </div>
</div>
"""

# ---------------------------------------------------------
# 4. Endpoints Routing
# ---------------------------------------------------------

@app.route('/')
def home():
    return render_template_string(HOME_HTML)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Safely pull structured arguments matching our template definitions
        applicant_name = request.form.get('applicant_name', 'Applicant')
        income_type_raw = request.form.get('income_type')
        education_type_raw = request.form.get('education_type')
        annual_income_raw = request.form.get('annual_income')

        try:
            # Match layout tokens directly into numerical encoders
            income_encoded = INCOME_TYPE_MAP.get(income_type_raw, 0)
            education_encoded = EDUCATION_TYPE_MAP.get(education_type_raw, 0)
            annual_income = float(annual_income_raw) if annual_income_raw else 0.0

            # Direct formatting configuration for arrays fed down to structural predictors
            features = np.array([[income_encoded, education_encoded, annual_income]])

            if model:
                # Execution layer mapping (Assuming 1 = Approved, 0 = Rejected)
                prediction = model.predict(features)[0]
                status = "Approved" if prediction == 1 else "Rejected"
            else:
                status = "Approved (Simulation)"

            return render_template_string(RESULT_HTML, name=applicant_name, result=status)

        except Exception as e:
            return f"An error occurred while compiling your prediction: {str(e)}"

    return render_template_string(INDEX_HTML)


if __name__ == '__main__':
    app.run(debug=True)