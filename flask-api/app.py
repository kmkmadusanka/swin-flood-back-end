from flask import Flask, request, jsonify, render_template
import pickle
from pandas import DataFrame
from supervised.automl import AutoML
import joblib
from werkzeug.wrappers import response

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random

app = Flask(__name__)

#Malwathu Model
malwathu_model = AutoML(
    results_path="./Models/Coastal Location Model Production/")

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict/coastal/attraction', methods=['POST'])
def predict():

    data = (request.get_json(force=True))
    star_grade = data['starGrade']
    city_center = data['cityCenter']
    private_beach = data['privateBeach']
    beach_type = data['beachType']
    lat = data['lat']
    long = data['long']
    no_of_restaurants = data['restaurants']
    no_of_cafes = data['cafes']
    no_of_atms = data['atms']
    attraction_1 = data['attraction1']
    attraction_2 = data['attraction2']

    int_features = [star_grade, city_center, private_beach, beach_type, lat, long,
                    no_of_restaurants, no_of_cafes, no_of_atms, attraction_1, attraction_2]

    df = DataFrame([int_features], columns=['star_grade', 'city_center', 'private_beach', 'beach_type',
                   'lat', 'long', 'no_of_restaurants', 'no_of_cafes', 'no_of_atms', 'attraction_1', 'attraction_2'])

    prediction = attraction_coastal_model.predict(df)

    location_rating = (round(prediction[0], 1))

    scoreCard = 1 + 99 * (location_rating - 6.0) / (10 - 6.0)
    scoreCard = round(scoreCard, 2)

    response = {"rating": location_rating, "scoreCard": scoreCard}

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
