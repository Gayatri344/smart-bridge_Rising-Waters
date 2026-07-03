from flask import Flask, render_template, request
# Import load from joblib to load the saved model file
from joblib import load
import numpy as np

# Create Flask app and Load our model file.
app = Flask(__name__) # our flask app

# Load model assets
model = load('floods.save')
sc = load('transform.save')

@app.route('/') # rendering the html template
def home():
    return render_template('home.html')

@app.route('/predict') # rendering the html template
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def predict():
    if request.method == 'POST':
        # 1. Capṇture the 5 weather parameters from the form inputs
        features = [
            float(request.form['v1']),
            float(request.form['v2']),
            float(request.form['v3']),
            float(request.form['v4']),
            float(request.form['v5'])
        ]
        
        # 2. Structure as a 2D array and apply the saved StandardScaler (sc)
        final_features = [np.array(features)]
        scaled_features = sc.transform(final_features)
        
        # 3. Pass features to the saved XGBoost model
        prediction = model.predict(scaled_features)
        
        # 4. Redirect the user to the appropriate result page based on output
        if prediction >= 1:
            return render_template('chance.html')
        else:
            return render_template('no_chance.html')
from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.run()
