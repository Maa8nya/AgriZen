from flask import Flask, request, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

# OpenWeatherMap API Key
OPENWEATHER_API_KEY = "91b4965ffd2b70037714d873aae573ba"
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather_data(lat, lon):
    url = f"{OPENWEATHER_BASE_URL}lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting weather data: {response.status_code}")
        return None

def month_number_to_name(month_number):
    return datetime(2020, month_number, 1).strftime('%B')

def get_crop_advice(lat, lon):
    weather_data = get_weather_data(lat, lon)
    if not weather_data:
        return "Could not retrieve weather data."

    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    weather_description = weather_data['weather'][0]['description']

    current_month = datetime.now().month
    sowing_month_name = month_number_to_name(current_month)

    harvest_month = (current_month + 4) % 12  # Simple example, adjust as needed
    if harvest_month == 0: harvest_month = 12
    harvest_month_name = month_number_to_name(harvest_month)

    return f"""
    Dominant Soil Type: Red Loam or Red Sandy Loam

    Best Crops:
    * Finger Millet (Ragi): Tolerates drought conditions and relatively low rainfall.

    Ideal Sowing Time: Mid-June to Early July
    Ideal Harvest Time: October - November
    """

@app.route('/get_advice', methods=['GET'])
def get_advice_endpoint():
    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')

        if not lat or not lon:
            return jsonify({'error': 'Latitude and Longitude are required'}), 400

        lat = float(lat)
        lon = float(lon)

        advice = get_crop_advice(lat, lon)
        return jsonify({'advice': advice})

    except (ValueError, KeyError, TypeError) as e:
        return jsonify({'error': f'Invalid request data: {str(e)}'}), 400

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500
    fy({'error': f'An unexpected error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
