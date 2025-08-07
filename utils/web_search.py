import requests
from config.config import SERPAPI_KEY

def search_web(query):
    url = f"https://serpapi.com/search.json?q={query}&api_key={SERPAPI_KEY}"
    try:
        response = requests.get(url)
        results = response.json()
        return results["organic_results"][0]["snippet"]
    except Exception as e:
        return f"Web search error: {str(e)}"
