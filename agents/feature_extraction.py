from bs4 import BeautifulSoup
import requests
from typing import Dict, List
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

class FeatureExtractionAgent:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.spec_patterns = {
            'brand': r'(brand|manufacturer|made by|by)\s*[:]?\s*([^\n<]+)',
            'model': r'(model|item)\s*(number|no)?\s*[:]?\s*([^\n<]+)',
            'weight': r'(weight)\s*[:]?\s*([^\n<]+)',
            'dimensions': r'(dimensions?|size)\s*[:]?\s*([^\n<]+)'
        }

    def extract_specifications(self, url: str) -> Dict:
        """Extract product specifications from a product page"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find specification tables/sections
            specs = {}
            for name, pattern in self.spec_patterns.items():
                matches = re.findall(pattern, response.text, re.IGNORECASE)
                if matches:
                    specs[name] = matches[0][-1].strip()
            
            return specs
            
        except Exception as e:
            print(f"Error extracting specifications: {e}")
            return {}

    def analyze_description(self, text: str) -> List[str]:
        """Analyze product description to extract key features"""
        try:
            # Clean and tokenize text
            text = text.lower()
            tokens = word_tokenize(text)
            tokens = [word for word in tokens if word not in self.stop_words]
            tokens = [word for word in tokens if word not in string.punctuation]
            
            # Extract meaningful keywords (simplified)
            keywords = []
            for word in tokens:
                if len(word) > 3 and word.isalpha():
                    keywords.append(word)
                    
            return list(set(keywords))[:10]  # Return top 10 unique keywords
            
        except Exception as e:
            print(f"Error analyzing description: {e}")
            return []

    def get_product_features(self, url: str) -> Dict:
        """Get all product features including specs and key description points"""
        specs = self.extract_specifications(url)
        
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            description = soup.find('meta', attrs={'name': 'description'})
            description = description['content'] if description else ""
            
            key_features = self.analyze_description(description)
            
            return {
                'specifications': specs,
                'key_features': key_features,
                'description_summary': description[:200] + "..." if description else ""
            }
            
        except Exception as e:
            print(f"Error getting product features: {e}")
            return {}

if __name__ == "__main__":
    agent = FeatureExtractionAgent()
    features = agent.get_product_features("https://example.com/product")
    print(features)
