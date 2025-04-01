import streamlit as st
from typing import Dict, List
import json
import pandas as pd
import plotly.express as px
from pathlib import Path

# Import agents
from agents.web_search import WebSearchAgent
from agents.feature_extraction import FeatureExtractionAgent
from agents.review_analysis import ReviewAnalysisAgent
from agents.comparative_analysis import ComparativeAnalysisAgent
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from agents.recommendation import RecommendationAgent

# Initialize agents
search_agent = WebSearchAgent()  # Will now properly get credentials from .env
feature_agent = FeatureExtractionAgent()
review_agent = ReviewAnalysisAgent()
analysis_agent = ComparativeAnalysisAgent()
recommendation_agent = RecommendationAgent()

# Data storage paths
DATA_DIR = Path("data")
PRODUCTS_FILE = DATA_DIR / "products.json"
REVIEWS_FILE = DATA_DIR / "reviews.json"

def ensure_data_dir():
    """Ensure data directory exists"""
    DATA_DIR.mkdir(exist_ok=True)

def load_data() -> Dict[str, List[Dict]]:
    """Load existing data from files"""
    ensure_data_dir()
    
    data = {"products": [], "reviews": []}
    try:
        if PRODUCTS_FILE.exists():
            with open(PRODUCTS_FILE, "r") as f:
                data["products"] = json.load(f)
        if REVIEWS_FILE.exists():
            with open(REVIEWS_FILE, "r") as f:
                data["reviews"] = json.load(f)
    except json.JSONDecodeError:
        pass
        
    return data

def save_data(products: List[Dict], reviews: List[Dict]):
    """Save data to files"""
    ensure_data_dir()
    
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=2)
    with open(REVIEWS_FILE, "w") as f:
        json.dump(reviews, f, indent=2)

def display_product_details(product: Dict):
    """Display product details section"""
    with st.expander(f"📋 {product['title']} - Details"):
        st.subheader("Specifications")
        if 'specifications' in product:
            specs = pd.DataFrame(
                product['specifications'].items(),
                columns=["Feature", "Value"]
            )
            st.table(specs)
        
        st.subheader("Key Features")
        if 'key_features' in product:
            for feature in product['key_features']:
                st.markdown(f"- {feature}")

def display_review_insights(review_summary: Dict):
    """Display review analysis section"""
    with st.expander("📊 Review Insights"):
        if not review_summary:
            st.warning("No review data available")
            return
            
        st.subheader("Sentiment Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Average Rating", 
                     f"{review_summary.get('average_rating', 0):.1f}/5")
            st.metric("Positive Sentiment", 
                     f"{review_summary.get('positive_percent', 0):.0f}%")
        
        with col2:
            st.metric("Review Count", 
                     review_summary.get('total_reviews', 0))
            st.metric("Average Polarity", 
                     f"{review_summary.get('average_polarity', 0):.2f}")
        
        # Sentiment distribution chart
        if 'sentiment_distribution' in review_summary:
            fig = px.pie(
                names=["Positive", "Neutral", "Negative"],
                values=[
                    review_summary['sentiment_distribution'].get('positive', 0),
                    review_summary['sentiment_distribution'].get('neutral', 0),
                    review_summary['sentiment_distribution'].get('negative', 0)
                ],
                title="Sentiment Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

def display_comparison(products: List[Dict]):
    """Display product comparison section"""
    with st.expander("🔍 Product Comparison"):
        if len(products) < 2:
            st.info("Add more products to enable comparison")
            return
            
        comparison_df = analysis_agent.create_comparison_table(products)
        st.dataframe(comparison_df)

def display_recommendation(recommendation: Dict):
    """Display recommendation section"""
    with st.expander("🏆 Recommendation"):
        if not recommendation or "error" in recommendation:
            st.warning("No recommendation available yet")
            return
            
        primary = recommendation["primary_recommendation"]
        st.subheader(f"Best Choice: {primary['title']}")
        st.write(primary["summary"])
        
        st.subheader("Pros")
        for pro in primary["pros"]:
            st.success(pro)
            
        st.subheader("Cons")
        for con in primary["cons"]:
            st.warning(con)
            
        st.write(primary["final_advice"])
        
        if recommendation.get("alternatives"):
            st.subheader("Alternatives")
            for alt in recommendation["alternatives"]:
                st.markdown(f"**{alt['title']}**")
                st.caption(alt["reason"])
                st.info(f"Key strength: {alt['key_strength']}")

def main():
    """Main Streamlit app"""
    st.set_page_config(page_title="AI Research Assistant", layout="wide")
    st.title("🔍 AI Research Assistant")
    
    # Initialize session state
    if "data" not in st.session_state:
        st.session_state.data = load_data()
    
    # Search bar
    with st.form("search_form"):
        query = st.text_input("Enter product to research:")
        submitted = st.form_submit_button("Search")
        
                if submitted and query:
                    with st.spinner("Researching products..."):
                        try:
                            # Execute full research pipeline
                            st.write("Searching for products...")
                            product_links = search_agent.search_products(query)
                            st.write(f"Found {len(product_links)} product links")
                            
                            products = []
                            reviews = []
                            
                            for i, link in enumerate(product_links[:3]):  # Limit to 3 products
                                st.write(f"Processing product {i+1}: {link}")
                                product = feature_agent.get_product_features(link)
                                if product:
                                    st.write(f"Extracted features for product {i+1}")
                                    product["review_summary"] = review_agent.analyze_reviews(product.get("reviews", []))
                                    products.append(product)
                                    reviews.extend(product.get("reviews", []))
                            
                            # Save and update data
                            st.session_state.data["products"] = products
                            st.session_state.data["reviews"] = reviews
                            save_data(products, reviews)
                            st.success(f"Successfully processed {len(products)} products")
                            
                        except Exception as e:
                            st.error(f"Error during research: {str(e)}")
                            st.exception(e)
    
    # Display results
    if st.session_state.data.get("products"):
        products = st.session_state.data["products"]
        
        # Get analyzed products
        scored_products = analysis_agent.calculate_product_scores(products)
        recommendation = recommendation_agent.generate_recommendation(scored_products)
        
        # Display sections
        for product in scored_products:
            display_product_details(product)
            display_review_insights(product.get("review_summary", {}))
        
        display_comparison(scored_products)
        display_recommendation(recommendation)

if __name__ == "__main__":
    main()
