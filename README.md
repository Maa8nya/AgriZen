# 🌾 AgriZen – Smart Agriculture Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey.svg)](https://flask.palletsprojects.com/)

A farmer-centric web application designed to bridge the technology gap in rural agriculture by providing real-time market intelligence and resource optimization tools.

## 🌟 Key Features

| Feature | Description | Technology Used |
|---------|------------|-----------------|
| 📊 Live Market Prices | Real-time crop price tracking across regional markets | BeautifulSoup, REST APIs |
| ⛅ Weather Forecast | Hyper-local weather predictions for farming planning | OpenWeatherMap API |
| 🔄 FarmShare | Equipment rental marketplace for farmers | Flask, SQLite |
| 🌐 Multilingual | Kannada/English support for regional accessibility | Google Translate API |


## 🛠️ Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Responsive Design (Mobile-first approach)
- Chart.js for data visualization

**Backend:**
- Python 3.8+
- Flask web framework
- SQLite (Development), PostgreSQL (Production)

**APIs & Services:**
- OpenWeatherMap API
- Google Translate APIgit status
- Agricultural Market Data APIs.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation
```bash
# Clone the repository
git clone https://github.com/maanya-aithal/agrizen.git

# Navigate to project directory
cd agrizen

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
