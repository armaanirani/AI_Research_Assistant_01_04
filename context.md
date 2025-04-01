# AI Research Assistant - Multi-Agent System

## Overview
This AI-powered research assistant is a multi-agent system designed to conduct in-depth product research. It can:
- Search for products on the web.
- Extract and analyze key product details.
- Collect and summarize user reviews.
- Compare products based on various factors.
- Provide a final recommendation based on collected insights.
- Be deployed using Streamlit for an interactive user experience.

## Implementation Flow

### 1. **User Input & Query Processing**
- The user enters a product query in the Streamlit interface.
- The query is analyzed, and the system determines the research scope (e.g., product category, price range, features of interest).

### 2. **Multi-Agent Task Distribution**
The system consists of multiple agents, each responsible for different tasks:

#### **Agent 1: Web Search & Product Discovery**
- Conducts web searches for relevant products using search APIs.
- Extracts links to product listings and specifications.
- Filters results based on relevance and credibility.

#### **Agent 2: Product Understanding & Feature Extraction**
- Visits product pages and extracts key attributes such as specifications, price, brand, etc.
- Uses NLP to analyze product descriptions and highlight unique selling points.

#### **Agent 3: Review Analysis & Sentiment Extraction**
- Collects and processes product reviews from different sources.
- Performs sentiment analysis to identify common praises and complaints.
- Highlights patterns in customer feedback (e.g., durability issues, performance concerns).

#### **Agent 4: Comparative Analysis & Ranking**
- Compares multiple products based on collected data.
- Scores products based on price, features, and user sentiment.
- Provides a ranked list of best options.

#### **Agent 5: Recommendation Engine**
- Synthesizes all insights to generate a final recommendation.
- Presents key reasons for the recommended product.
- Suggests alternatives if preferences differ.

### 3. **Data Presentation in Streamlit**
The research findings are displayed in an interactive UI with the following components:
- **Search Bar:** Allows users to enter their query.
- **Product Details Section:** Displays summarized specifications of top products.
- **Review Insights:** Shows common themes in user reviews with sentiment graphs.
- **Comparison Table:** Provides a structured comparison of products.
- **Final Recommendation:** Highlights the best choice and reasons behind it.

## Implementation Steps

### 1. **Set Up Streamlit**
```bash
pip install streamlit
```
Create a basic Streamlit app:
```python
import streamlit as st

def main():
    st.title("AI Research Assistant")
    query = st.text_input("Enter product name:")
    if query:
        st.write(f"Searching for: {query}")

if __name__ == "__main__":
    main()
```
Run with:
```bash
streamlit run app.py
```

### 2. **Integrate Web Search API**
- Use `Google Search API` to fetch product listings.
- Extract relevant product links for further analysis.

### 3. **Extract and Process Product Details**
- Use `BeautifulSoup` or `Scrapy` to scrape product information.
- Implement NLP techniques to summarize key product descriptions.

### 4. **Analyze Reviews**
- Scrape and clean user reviews.
- Perform sentiment analysis using `VADER` or `TextBlob`.

### 5. **Build Comparative Analysis & Recommendation Logic**
- Store extracted data in a structured format (Pandas DataFrame).
- Rank products using weighted scoring based on extracted insights.

### 6. **Enhance Streamlit UI**
- Use Streamlit components like `st.dataframe`, `st.plotly_chart`, and `st.markdown` for better presentation.

## Folder and File Structure
```
ai_research_assistant/
│── app.py                   # Main Streamlit app
│── requirements.txt         # Dependencies
│── config.py                # Configuration settings
│
├── agents/                  # Multi-agent system
│   ├── web_search.py        # Web search and product discovery
│   ├── feature_extraction.py # Product details extraction
│   ├── review_analysis.py   # Sentiment analysis of reviews
│   ├── comparative_analysis.py # Comparison and ranking logic
│   ├── recommendation.py    # Final recommendation engine
│
├── data/                    # Storage for extracted data
│   ├── products.json        # Fetched product details
│   ├── reviews.json         # Collected user reviews
│
├── utils/                   # Helper functions
│   ├── scraper.py           # Web scraping utilities
│   ├── nlp_utils.py         # NLP processing utilities
│   ├── data_processing.py   # Data cleaning and transformation
│
└── assets/                  # Static assets (e.g., images, icons)
```

## Conclusion
This structured approach ensures that the AI Research Assistant provides thorough product insights, comparisons, and recommendations interactively using Streamlit. The modular, multi-agent design allows for scalability and improvement over time.

