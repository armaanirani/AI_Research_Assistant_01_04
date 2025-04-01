from typing import List, Dict
import re
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon', quiet=True)

class ReviewAnalysisAgent:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()
        self.clean_patterns = [
            r'<[^>]+>',  # HTML tags
            r'http\S+',  # URLs
            r'\@\w+',    # Mentions
            r'\#\w+',    # Hashtags
            r'\d+',      # Numbers
        ]

    def clean_review_text(self, text: str) -> str:
        """Clean review text by removing unwanted patterns"""
        for pattern in self.clean_patterns:
            text = re.sub(pattern, '', text)
        return text.strip()

    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of a single review"""
        cleaned_text = self.clean_review_text(text)
        
        # Using VADER
        vader_scores = self.sid.polarity_scores(cleaned_text)
        
        # Using TextBlob
        blob = TextBlob(cleaned_text)
        blob_sentiment = blob.sentiment
        
        return {
            'vader': {
                'compound': vader_scores['compound'],
                'positive': vader_scores['pos'],
                'negative': vader_scores['neg'],
                'neutral': vader_scores['neu']
            },
            'textblob': {
                'polarity': blob_sentiment.polarity,
                'subjectivity': blob_sentiment.subjectivity
            },
            'text': cleaned_text
        }

    def analyze_reviews(self, reviews: List[str]) -> Dict:
        """Analyze a batch of reviews and return aggregated sentiment"""
        if not reviews:
            return {}
            
        results = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for review in reviews:
            analysis = self.analyze_sentiment(review)
            results.append(analysis)
            
            # Classify based on VADER compound score
            if analysis['vader']['compound'] >= 0.05:
                positive_count += 1
            elif analysis['vader']['compound'] <= -0.05:
                negative_count += 1
            else:
                neutral_count += 1
                
        total = len(reviews)
        return {
            'reviews': results,
            'summary': {
                'total_reviews': total,
                'positive_percent': (positive_count / total) * 100,
                'negative_percent': (negative_count / total) * 100,
                'neutral_percent': (neutral_count / total) * 100,
                'average_polarity': sum(r['textblob']['polarity'] for r in results) / total,
                'average_subjectivity': sum(r['textblob']['subjectivity'] for r in results) / total
            },
            'common_themes': self.extract_common_themes([r['text'] for r in results])
        }

    def extract_common_themes(self, reviews: List[str]) -> List[str]:
        """Extract common themes from reviews using simple frequency analysis"""
        from collections import Counter
        words = []
        
        for review in reviews:
            tokens = review.lower().split()
            tokens = [word for word in tokens if len(word) > 3 and word.isalpha()]
            words.extend(tokens)
            
        word_counts = Counter(words)
        return [word for word, count in word_counts.most_common(5)]

if __name__ == "__main__":
    agent = ReviewAnalysisAgent()
    test_reviews = [
        "This product is amazing! Works perfectly and exceeded my expectations.",
        "Terrible quality. Broke after just two days of use.",
        "It's okay for the price, but nothing special."
    ]
    results = agent.analyze_reviews(test_reviews)
    print(results)
