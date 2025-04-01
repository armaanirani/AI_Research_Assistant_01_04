from typing import List, Dict
import pandas as pd
from dataclasses import dataclass
import numpy as np

@dataclass
class ProductScoreWeights:
    price: float = 0.3
    features: float = 0.25
    sentiment: float = 0.25
    popularity: float = 0.2

class ComparativeAnalysisAgent:
    def __init__(self, weights: ProductScoreWeights = None):
        self.weights = weights or ProductScoreWeights()
        
    def normalize_scores(self, values: List[float]) -> List[float]:
        """Normalize values to 0-1 scale for comparison"""
        if not values:
            return []
            
        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val
        
        if range_val == 0:
            return [0.5 for _ in values]
            
        return [(val - min_val) / range_val for val in values]

    def calculate_product_scores(self, products: List[Dict]) -> List[Dict]:
        """Calculate composite scores for each product"""
        if not products:
            return []
            
        # Extract relevant data
        prices = [float(p.get('price', 0).replace('$', '').replace(',', '')) 
                 if isinstance(p.get('price'), str) 
                 else float(p.get('price', 0)) 
                 for p in products]
        feature_counts = [len(p.get('key_features', [])) for p in products]
        sentiment_scores = [p.get('review_summary', {}).get('average_polarity', 0) 
                          for p in products]
        
        # Normalize scores
        norm_prices = self.normalize_scores([-p for p in prices])  # Lower price is better
        norm_features = self.normalize_scores(feature_counts)
        norm_sentiment = self.normalize_scores(sentiment_scores)
        
        # Calculate weighted scores
        scored_products = []
        for i, product in enumerate(products):
            score = (
                self.weights.price * norm_prices[i] +
                self.weights.features * norm_features[i] +
                self.weights.sentiment * norm_sentiment[i]
            )
            
            scored_products.append({
                **product,
                'score': round(score, 2),
                'normalized_price': round(norm_prices[i], 2),
                'normalized_features': round(norm_features[i], 2),
                'normalized_sentiment': round(norm_sentiment[i], 2)
            })
            
        return sorted(scored_products, key=lambda x: x['score'], reverse=True)

    def create_comparison_table(self, products: List[Dict]) -> pd.DataFrame:
        """Create a comparison table from scored products"""
        if not products:
            return pd.DataFrame()
            
        # Extract comparison attributes
        comparison_data = []
        for product in products:
            comparison_data.append({
                'Product': product.get('title', 'N/A'),
                'Brand': product.get('specifications', {}).get('brand', 'N/A'),
                'Price': product.get('price', 'N/A'),
                'Key Features': ', '.join(product.get('key_features', [])[:3]),
                'Sentiment Score': product.get('review_summary', {}).get('average_polarity', 0),
                'Overall Score': product.get('score', 0)
            })
            
        return pd.DataFrame(comparison_data)

    def get_top_products(self, products: List[Dict], top_n: int = 3) -> List[Dict]:
        """Get top N products based on scores"""
        scored = self.calculate_product_scores(products)
        return scored[:top_n]

if __name__ == "__main__":
    agent = ComparativeAnalysisAgent()
    
    test_products = [
        {
            'title': 'Product A',
            'price': '$99.99',
            'key_features': ['wireless', 'noise cancelling', 'long battery'],
            'review_summary': {'average_polarity': 0.8}
        },
        {
            'title': 'Product B',
            'price': '$149.99',
            'key_features': ['bluetooth', 'comfortable', 'microphone'],
            'review_summary': {'average_polarity': 0.6}
        }
    ]
    
    results = agent.calculate_product_scores(test_products)
    print(results)
