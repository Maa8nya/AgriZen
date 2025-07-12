import time
import csv
from flask import Flask, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Global variable to store the crop prices
crop_prices = []

# Function to scrape crop prices
def scrape_crop_prices():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Optional: run the browser in the background without UI

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = 'https://www.ncdex.com/market-watch/live_quotes'
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table'))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        rows = soup.find_all('tr')

        crop_prices_list = []
        for row in rows:
            cells = row.find_all('td')

            if len(cells) > 1:
                crop_name = cells[0].get_text(strip=True)
                price_tag = row.find('li', class_='ltp')

                if price_tag:
                    crop_price = price_tag.get_text(strip=True)
                    if crop_name and crop_price:
                        crop_prices_list.append({'crop': crop_name, 'price': crop_price})

        global crop_prices
        crop_prices = crop_prices_list  # Update the global crop prices

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

# Schedule the scraping function to run every 10 seconds
scheduler = BackgroundScheduler()
scheduler.add_job(func=scrape_crop_prices, trigger='interval', seconds=10)
scheduler.start()

# API route to get crop prices in JSON format
@app.route('/api/crop_prices')
def get_crop_prices():
    return jsonify(crop_prices)

# Route to render the frontend page with crop prices
@app.route('/')
def index():
    return render_template('live_crop_price.html', crop_prices=crop_prices)

if __name__ == '__main__':
    app.run(debug=True)
