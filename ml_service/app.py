# En app.py
from flask import Flask, request, jsonify
from ml_model import load_model, prepare_data, make_prediction

app = Flask(__name__)
model = load_model()

@app.route('/predict', methods=['GET'])
def predict():
    data = request.json
    prepared_data = prepare_data(data)
    prediction = make_prediction(model, prepared_data)
    print("Prediction: ", prediction)
    return jsonify(prediction=prediction)
