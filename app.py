from flask import Flask, render_template, request
from joblib import load
import numpy as np
import os

# Create Flask App
app = Flask(__name__)

# Load Model and Scaler
model = load("floods.save")
sc = load("transform.save")


# Home Page
@app.route("/")
def home():
    return render_template("home.html")


# Prediction Page
@app.route("/predict")
def index():
    return render_template("index.html")


# Prediction Logic
@app.route("/submit", methods=["POST"])
def predict():

    try:
        features = [
            float(request.form["v1"]),
            float(request.form["v2"]),
            float(request.form["v3"]),
            float(request.form["v4"]),
            float(request.form["v5"])
        ]

        # Convert to NumPy array
        final_features = np.array([features])

        # Scale the input
        scaled_features = sc.transform(final_features)

        # Predict
        prediction = model.predict(scaled_features)

        # Display Result
        if prediction[0] >= 1:
            return render_template("chance.html")
        else:
            return render_template("no_chance.html")

    except Exception as e:
        return f"Error: {e}"


# Run Flask App
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
