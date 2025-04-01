from typing import List, Dict
from dataclasses import dataclass
import textwrap

@dataclass
class RecommendationConfig:
    max_alternatives: int = 3
    max_pros_cons: int = 3
    wrap_width: int = 80

class RecommendationAgent:
    def __init__(self, config: RecommendationConfig = None):
        self.config = config or RecommendationConfig()

    def generate_recommendation(self, top_products: List[Dict]) -> Dict:
        """Generate recommendation report for top products"""
        if not top_products:
            return {"error": "No products to recommend"}
            
        primary = top_products[0]
        alternatives = top_products[1:self.config.max_alternatives+1]
        
        return {
            "primary_recommendation": self._format_primary(primary),
            "alternatives": [self._format_alternative(p) for p in alternatives],
            "comparison_highlights": self._generate_comparison_highlights(top_products)
        }

    def _format_primary(self, product: Dict) -> Dict:
        """Format the primary recommendation"""
        pros = self._extract_pros(product)
        cons = self._extract_cons(product)
        
        return {
            "title": product.get('title', 'Unknown Product'),
            "summary": textwrap.fill(
                f"We recommend {product.get('title', 'this product')} as your best option. "
                f"It scores {product.get('score', 0):.2f}/1.0 overall, with strong performance in "
                f"{self._highlight_strengths(product)}.",
                width=self.config.wrap_width
            ),
            "pros": [textwrap.fill(p, width=self.config.wrap_width) for p in pros],
            "cons": [textwrap.fill(c, width=self.config.wrap_width) for c in cons],
            "final_advice": textwrap.fill(
                self._generate_final_advice(product, pros, cons),
                width=self.config.wrap_width
            )
        }

    def _format_alternative(self, product: Dict) -> Dict:
        """Format an alternative recommendation"""
        return {
            "title": product.get('title', 'Unknown Product'),
            "reason": textwrap.fill(
                f"Good alternative with score {product.get('score', 0):.2f}/1.0. "
                f"Consider this if {self._get_alternative_reason(product)}.",
                width=self.config.wrap_width
            ),
            "key_strength": self._get_key_strength(product)
        }

    def _extract_pros(self, product: Dict) -> List[str]:
        """Extract pros from product data"""
        pros = []
        if product.get('normalized_sentiment', 0) > 0.7:
            pros.append("Highly rated by customers")
        if product.get('normalized_price', 0) > 0.8:
            pros.append("Excellent value for money")
        if len(product.get('key_features', [])) > 5:
            pros.append("Rich feature set")
        return pros[:self.config.max_pros_cons]

    def _extract_cons(self, product: Dict) -> List[str]:
        """Extract cons from product data"""
        cons = []
        if product.get('normalized_sentiment', 0) < 0.3:
            cons.append("Mixed customer reviews")
        if product.get('normalized_price', 0) < 0.3:
            cons.append("Premium pricing")
        return cons[:self.config.max_pros_cons]

    def _highlight_strengths(self, product: Dict) -> str:
        """Highlight the product's main strengths"""
        strengths = []
        if product.get('normalized_features', 0) > 0.8:
            strengths.append("features")
        if product.get('normalized_sentiment', 0) > 0.8:
            strengths.append("customer satisfaction")
        if product.get('normalized_price', 0) > 0.8:
            strengths.append("value")
        return ", ".join(strengths) or "multiple categories"

    def _get_alternative_reason(self, product: Dict) -> str:
        """Get reason why this is a good alternative"""
        if product.get('normalized_price', 0) > 0.7:
            return "you're looking for better value"
        if product.get('normalized_features', 0) > 0.7:
            return "you need specific features"
        return "the primary recommendation doesn't meet your needs"

    def _get_key_strength(self, product: Dict) -> str:
        """Get the alternative's key strength"""
        if product.get('normalized_sentiment', 0) > 0.7:
            return "Customer satisfaction"
        if product.get('normalized_features', 0) > 0.7:
            return "Feature set"
        return "Overall balance"

    def _generate_comparison_highlights(self, products: List[Dict]) -> str:
        """Generate comparison highlights text"""
        if len(products) < 2:
            return ""
            
        best_price = min(products, key=lambda x: float(x.get('price', '99999').replace('$', '').replace(',', '')))
        best_sentiment = max(products, key=lambda x: x.get('review_summary', {}).get('average_polarity', 0))
        
        highlights = [
            f"- {best_price.get('title')} has the best price at {best_price.get('price')}",
            f"- {best_sentiment.get('title')} has the most positive reviews"
        ]
        
        return "\n".join(highlights)

    def _generate_final_advice(self, product: Dict, pros: List[str], cons: List[str]) -> str:
        """Generate final advice section"""
        advice = [f"Final advice on {product.get('title')}:"]
        
        if pros:
            advice.append("Strengths:")
            advice.extend(f"✓ {p}" for p in pros)
            
        if cons:
            advice.append("Considerations:")
            advice.extend(f"⚠ {c}" for c in cons)
            
        return "\n".join(advice)

if __name__ == "__main__":
    agent = RecommendationAgent()
    
    test_products = [
        {
            'title': 'Premium Headphones',
            'price': '$299.99',
            'score': 0.85,
            'normalized_sentiment': 0.9,
            'normalized_price': 0.6,
            'normalized_features': 0.95,
            'key_features': ['noise cancelling', 'wireless', '30h battery'],
            'review_summary': {'average_polarity': 0.85}
        },
        {
            'title': 'Budget Headphones',
            'price': '$49.99',
            'score': 0.75,
            'normalized_sentiment': 0.7,
            'normalized_price': 0.9,
            'normalized_features': 0.6,
            'review_summary': {'average_polarity': 0.7}
        }
    ]
    
    recommendation = agent.generate_recommendation(test_products)
    print(recommendation)
