from flask import Flask, render_template, request
import requests
from locations import countries

app = Flask(__name__)

# Replace 'your_api_key' with your own actual API key from NewsAPI providing platfrom
API_KEY = 'your_api_key'
url = 'https://newsapi.org/v2/top-headlines'

@app.route('/', methods=['GET', 'POST'])
def index():
    region = request.form.get('region', 'all')  # Default to 'all' (All Countries) if no region selected
    country = request.form.get('country', 'all')  # Default to 'all' (All Countries) if no country selected
    
    try:
        if region != 'all':
            response = requests.get(url, params={'apiKey': API_KEY, 'country': region})
        elif country != 'all':
            response = requests.get(url, params={'apiKey': API_KEY, 'country': country})
        else:
            response = requests.get(url, params={'apiKey': API_KEY})
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        articles = data.get('articles', [])
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e}"
    except requests.exceptions.RequestException as e:
        return f"Request exception occurred: {e}"
    except ValueError as e:
        return f"Value error occurred: {e}"
    
    return render_template('index.html', articles=articles, region=region, countries=countries)

if __name__ == '__main__':
    app.run(debug=True)
