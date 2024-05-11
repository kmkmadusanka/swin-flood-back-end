from flask import Flask, request, jsonify, render_template
import pickle
from pandas import DataFrame
import random
from werkzeug.wrappers import response

app = Flask(__name__)

#Malwathu Model
filename = './Models/MalwathuPrediction.pkl'
model = pickle.load(open(filename, 'rb'))

@app.route('/')
def hello():
    response = {"waterLevel": "test"}
    return jsonify(response)

@app.route('/predict', methods=['POST'])
def predict():
    print("bfr-prediction")
    data = request.get_json(force=True)
    
    Murrunkan = data['murrunkan']
    Pavattakulam = data['pavattakulam']
    Nachchiduva = data['nachchiduva']
    Vavniya = data['vavniya']
    Mannr = data['mannr']
    Apura = data['apura']
   
    int_features = [Murrunkan,Pavattakulam,Nachchiduva,Vavniya,Mannr,Apura]

    df = DataFrame([int_features], columns=['Murrunkan', 'Pavattakulam', 'Nachchiduva', 'Vavniya', 'Mannr','Apura'])

    prediction = model.predict(df)    
    water_level = float(prediction[0])
    print(water_level)    
    flood_risk = "false"
    severity = 0
    
    if water_level < 0.2:
        water_level = 0.566
        
    if water_level > 10:
        water_level = 11.554        
 

    if water_level > 5:
        flood_risk = "true"
        severity = 1

    if water_level > 7:
        severity = 2
        
    if water_level > 8:
        severity = 3    

    response = {"waterLevel": water_level, "floodRisk": flood_risk, "severity": severity}
    

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
