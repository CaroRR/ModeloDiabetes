from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# CONFIGURA ESTOS:
API_KEY = "ZfygfgZFMRwpsaeAoV2iW0wr5Exhezln229ZhGTM771V"
DEPLOYMENT_ENDPOINT = 'https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/1db21316-2bb8-416d-92fd-b3952016e10a/predictions?version=2021-05-01'

def obtener_token(api_key):
    response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={"apikey": api_key, "grant_type": "urn:ibm:params:oauth:grant-type:apikey"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return response.json()["access_token"]

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None

    if request.method == 'POST':
        datos = [
            float(request.form['pregnancies']),
            float(request.form['glucose']),
            float(request.form['blood_pressure']),
            float(request.form['skin_thickness']),
            float(request.form['insulin']),
            float(request.form['bmi']),
            float(request.form['dpf']),
            float(request.form['age']),
        ]

        input_payload = {
            "input_data": [{
                "fields": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"],
                "values": [datos]
            }]
        }

        token = obtener_token(API_KEY)

        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }

        response = requests.post(DEPLOYMENT_ENDPOINT, json=input_payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            prediction = result['predictions'][0]['values'][0][0]
        else:
            prediction = f"Error: {response.text}"

    return render_template('form.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
