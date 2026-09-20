# Ecommerce Product Recommendation

A machine learning web app that suggests products to users based on their preferences and past ratings.

**Live demo:** https://your-deployment-link.com  
**Built with:** Python, Flask, Scikit-learn, Pandas

---

## Features

- Content-based recommendation using product similarity
- Rating-based recommendation using user behaviour
- Interactive Flask interface for browsing and receiving recommendations
- Efficient d
ata pipeline built with Pandas

## How it works

1. User selects a product or enters preferences
2. Engine computes similarity scores (TF-IDF / cosine similarity)
3. Top-N products are returned and displayed in the UI

## Setup

```bash
git clone https://github.com/aarathi2006/ecommerce-product-recommendation.git
cd ecommerce-product-recommendation
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
