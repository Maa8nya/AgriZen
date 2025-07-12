from flask import Flask, request, jsonify
from datetime import datetime
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# OpenWeatherMap API Key
OPENWEATHER_API_KEY = "91b4965ffd2b70037714d873aae573ba"
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather_data(lat, lon):
    try:
        url = f"{OPENWEATHER_BASE_URL}lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting weather data: {str(e)}")
        return None

def month_number_to_name(month_number):
    return datetime(2020, month_number, 1).strftime('%B')

def get_crop_advice(lat, lon):
    weather_data = get_weather_data(lat, lon)
    if not weather_data:
        return "Could not retrieve weather data for your location."

    try:
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather_desc = weather_data['weather'][0]['description']
        location = weather_data.get('name', 'your area')
        
        current_month = datetime.now().month
        sowing_month_name = month_number_to_name(current_month)
        harvest_month = (current_month + 4) % 12 or 12
        harvest_month_name = month_number_to_name(harvest_month)

        # Crop recommendations based on temperature ranges
        if temp > 30:
            crops = ["Pearl Millet (Bajra)", "Sorghum (Jowar)", "Cluster Beans"]
        elif temp > 20:
            crops = ["Maize", "Groundnut", "Soybean", "Cotton"]
        else:
            crops = ["Wheat", "Barley", "Mustard", "Chickpea"]

        advice = {
            "location": location,
            "weather": {
                "description": weather_desc,
                "temperature": temp,
                "humidity": humidity
            },
            "recommended_crops": crops,
            "planting_schedule": {
                "sowing_month": sowing_month_name,
                "harvest_month": harvest_month_name
            },
            "soil_type": "Red Loam or Red Sandy Loam",
            "recommendations": [
                "Conduct soil testing every 2-3 years",
                "Apply organic compost to improve soil structure",
                "Practice crop rotation to maintain soil health"
            ]
        }
        return advice

    except KeyError as e:
        print(f"Missing key in weather data: {str(e)}")
        return None

@app.route('/get_advice', methods=['POST'])
def get_advice_endpoint():
    try:
        data = request.get_json()
        lat = data.get('lat')
        lon = data.get('lon')

        if None in [lat, lon]:
            return jsonify({'error': 'Latitude and longitude are required'}), 400

        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return jsonify({'error': 'Invalid latitude or longitude format'}), 400

        advice = get_crop_advice(lat, lon)
        if not advice:
            return jsonify({'error': 'Could not generate agricultural advice'}), 500

        return jsonify(advice)

    except Exception as e:
        print(f"Error in /get_advice: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)