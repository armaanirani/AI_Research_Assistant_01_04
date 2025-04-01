import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import json
import os

api_key = os.getenv("GOOGLE_API")
search_engine_id = os.getenv("SEARCH_ENGINE_ID")

class WebSearchAgent:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        
    def search_products(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search for products using Google Custom Search API"""
        params = {
            'q': query,
            'key': self.api_key,
            'cx': search_engine_id,
            'num': num_results
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            results = response.json().get('items', [])
            
            # Filter and format results
            product_links = []
            for item in results:
                if 'link' in item:
                    product_links.append({
                        'title': item.get('title'),
                        'link': item.get('link'),
                        'snippet': item.get('snippet')
                    })
            return product_links
            
        except Exception as e:
            print(f"Error during product search: {e}")
            return []

    def extract_product_details(self, url: str) -> Dict:
        """Extract basic product details from a product page"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Basic extraction - to be customized per site
            title = soup.find('h1').text if soup.find('h1') else ""
            price = soup.find(class_='price').text if soup.find(class_='price') else ""
            
            return {
                'title': title.strip(),
                'price': price.strip(),
                'url': url
            }
        except Exception as e:
            print(f"Error extracting product details: {e}")
            return {}

if __name__ == "__main__":
    # Example usage
    agent = WebSearchAgent(api_key=api_key)
    results = agent.search_products("wireless headphones")
    print(json.dumps(results, indent=2))
