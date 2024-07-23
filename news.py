# news.py

import requests
from ss import key  # Import the API key from ss.py

def fetch_news():
    api_address = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={key}"
    json_data = requests.get(api_address).json()
    
    ar = []
    for i in range(3):
        title = json_data["articles"][i]["title"]
        ar.append(f"Number {i + 1}: {title}.")
    
    return ar
