import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import json
import os

class WebSearchAgent:
    def __init__(self, api_key: str = None, search_engine_id: str = None):
        """Initialize with either direct credentials or read from environment variables"""
        self.api_key = api_key or os.getenv("GOOGLE_API")
        self.search_engine_id = search_engine_id or os.getenv("SEARCH_ENGINE_ID")
        self.base_url = "https://www.googleapis.com/customsearch/v1"
        
        if not self.api_key or not self.search_engine_id:
            raise ValueError("Missing required API credentials. Please provide both API key and Search Engine ID")
        
    def search_products(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search for products using Google Custom Search API"""
            
        params = {
            'q': query,
            'key': self.api_key,
            'cx': self.search_engine_id,
            'num': num_results
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            
            # Check for API-specific errors
            if response.status_code == 403:
                error_data = response.json()
                print(f"API Error: {error_data.get('error', {}).get('message', 'Forbidden')}")
                print("Possible causes:")
                print("- Invalid API key or Search Engine ID")
                print("- API not enabled in Google Cloud Console")
                print("- Exceeded daily quota")
                return []
                
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
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            return []
        except json.JSONDecodeError:
            print("Error: Invalid API response format")
            return []
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
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
