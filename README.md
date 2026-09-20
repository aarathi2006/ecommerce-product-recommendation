# 🛒 Ecommerce Product Recommendation Engine

A machine learning–powered product recommendation web app that suggests relevant products to users based on browsing behaviour, product similarity, and historical ratings.

**Live demo:** https://your-deployment-link.com  
**Built with:** Python · Flask · Scikit-learn · Pandas · NumPy  
**Author:** [Boddu Aarathi](https://github.com/aarathi2006)

---

## 📌 Overview

Modern ecommerce platforms live or die by their ability to surface the *right product to the right user at the right time*. Generic "top sellers" lists no longer cut it — users expect personalised, context-aware suggestions.

This project is a full-stack implementation of a recommendation system that demonstrates:

- **Content-based filtering** — recommend products similar to what a user is currently viewing, using product metadata (name, category, description).
- **Collaborative / rating-based filtering** — recommend products that other users with similar rating patterns have liked.
- **A clean Flask web interface** — search, browse, and receive recommendations in real time.

It's designed as a portfolio piece to show the full pipeline: **raw data → cleaning → feature engineering → similarity modelling → REST interface → front-end delivery**.

---

## ✨ Features

| Feature | Description |
|:---|:---|
| 🔍 **Product search** | Search the catalog by name or category |
| 🎯 **Content-based recommendations** | TF-IDF vectorisation + cosine similarity to find visually/descriptively similar products |
| ⭐ **Rating-based recommendations** | User-item matrix with similarity scoring to surface items liked by similar users |
| 📊 **Trending products** | Pre-computed list of top-performing items by rating volume |
| 🖥️ **Flask web UI** | Server-rendered templates with search, browse, and recommendation views |
| 🧪 **Jupyter notebook** | Full exploratory analysis and model development in `product_recommendation.ipynb` |
| 🌐 **Deployable** | Includes `Procfile` and `requirements.txt` for one-click Render deployment |

---

## 🏗️ Architecture
┌─────────────────────────────────────────────────────────────┐
│ Browser (User) │
│ index.html · main.html · static/img/* │
└──────────────────────────────┬──────────────────────────────┘
│ HTTP
▼
┌─────────────────────────────────────────────────────────────┐
│ Flask Application │
│ app.py │
│ ┌──────────────┬──────────────┬──────────────────────────┐ │
│ │ Routing │ Search API │ Recommendation Engine │ │
│ └──────────────┴──────────────┴──────────────────────────┘ │
└──────────────────────────────┬──────────────────────────────┘
│
┌────────────────┴────────────────┐
▼ ▼
┌─────────────────┐ ┌──────────────────┐
│ Data Layer │ │ Models Layer │
│ clean_data.csv │ │ models/.csv │
│ trending_.csv │ │ similarity mat │
└─────────────────┘ └──────────────────┘

ecommerce-product-recommendation/
│
├── app.py                          # Flask entry point + routes
├── requirements.txt                # Python dependencies
├── Procfile                        # Render/gunicorn startup command
├── README.md                       # This file
├── .gitignore                      # Excludes data, venv, caches
│
├── product_recommendation.ipynb    # Model development + EDA
│
├── clean_data.csv                  # Cleaned product catalog
├── trending_products.csv           # Pre-computed trending list
│
├── models/
│   ├── clean_data.csv              # Model-ready feature matrix
│   └── trending_products.csv       # Cached trending scores
│
├── static/
│   └── img/                        # Product images, assets
│
└── templates/
    ├── index.html                  # Homepage + search
    └── main.html                   # Recommendation results


##Installation
# 1. Clone
git clone https://github.com/aarathi2006/ecommerce-product-recommendation.git
cd ecommerce-product-recommendation

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate           # macOS/Linux
# venv\Scripts\activate            # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py

##Testing
# Home
curl http://localhost:5000/

# Search
curl "http://localhost:5000/search?q=headphones"

# Recommendations for a product
curl http://localhost:5000/recommend/<product_id>

##🔮 Future Improvements
🔄 Retrain models on a scheduled cron job (nightly)

🧠 Add matrix factorisation (SVD, ALS) for better collaborative filtering

🎨 Migrate the front end to React with real-time recommendations as you type

📈 Add A/B testing infrastructure to measure click-through lift

🔐 Add user authentication (JWT + bcrypt)

🐳 Containerise with Docker for portability

📦 Move to PostgreSQL for persistent storage

☁️ Deploy behind a CDN (Cloudflare) for faster static asset delivery

