# 🛒 Ecommerce Product Recommendation Engine

An end-to-end machine learning web application that recommends products to users based on **content similarity** and **collaborative rating patterns**. Built with Python, Flask, and Scikit-learn, deployed on Render.

**Live demo:** https://ecommerce-recommender-0zkb.onrender.com  
**Author:** [Boddu Aarathi](https://github.com/aarathi2006)  
**Stack:** Python 3.10 · Flask · Scikit-learn · Pandas · NumPy · Jinja2



## 📌 Overview

This project is a working ecommerce product recommendation engine that suggests relevant products to users through two complementary strategies:

1. **Content-based filtering** — "You're looking at this, here are similar items."
2. **Collaborative filtering** — "Users like you also liked these items."

It's served through a Flask web application with server-rendered templates, and it's deployed to production on Render with Gunicorn as the WSGI server.

**Why I built this:** Recommendation systems are one of the highest-impact applications of machine learning in industry — Amazon attributes ~35% of revenue to its recommendation engine, and Netflix reports that 80% of watched content comes from recommendations. This project was my way of building that pipeline from scratch: raw data → cleaning → feature engineering → similarity modelling → REST interface → deployed product.

It's not a notebook full of cells. It's a **deployable application** with a clean separation between the ML layer, the application layer, and the presentation layer.

---

## 🧩 The Problem

An ecommerce site with 5,000+ products faces a discovery problem:

- **Too much choice** → users get overwhelmed and bounce.
- **Generic "top sellers"** → no personalisation, low engagement.
- **Manual curation** → doesn't scale beyond a few dozen products.

Users need a system that:

1. **Understands context** — what they're currently browsing.
2. **Learns preferences** — what they've rated or bought before.
3. **Surfaces relevant items** — the next most likely product they'd engage with.
4. **Does it fast** — within a page load.

This project implements exactly that.

---

## 🎯 Why Recommendation Systems Matter

| Metric | Impact |
|:---|:---|
| **Conversion rate** | Personalised recommendations can increase conversions by 10–30% |
| **Average order value** | Cross-sell recommendations lift basket size by 20%+ |
| **Retention** | Users who engage with recommendations return 2–3× more often |
| **Cold-start mitigation** | Content-based recommendations work even with zero user history |
| **Long-tail discovery** | Surfaces niche products that would otherwise never appear |

A simple recommender can move the needle more than a fancy deep learning model that never ships. This project ships.

---

## ✨ Features

### Core Recommendation Features

| Feature | Type | Description |
|:---|:---|:---|
| **Similar products** | Content-based | When viewing a product, see N similar items ranked by description similarity |
| **Personalised picks** | Collaborative | Recommendations for a logged-in user based on their rating history |
| **Trending now** | Popularity-based | Pre-computed top products by weighted rating × review count |
| **Search** | Keyword | Full-text search across product names and categories |
| **Category browse** | Filter | Browse all products within a category |

### Application Features

| Feature | Description |
|:---|:---|
| **Responsive UI** | Works on desktop and mobile |
| **Product cards** | Image, name, price, rating, category |
| **Fast page loads** | Server-rendered HTML via Jinja2, no client-side JS frameworks |
| **Graceful fallback** | If recommendations fail, the UI degrades to trending products |

### Engineering Features

| Feature | Description |
|:---|:---|
| **Clean separation** | ML logic lives in `models/`, web logic in `app.py`, templates in `templates/` |
| **Configurable** | Number of recommendations, similarity metric — all parameterised |
| **Deployable** | Procfile, requirements.txt, and Docker-ready structure |
| **Reproducible** | All data transformations documented in `product_recommendation.ipynb` |

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

# Home
curl http://localhost:5000/

# Search
curl "http://localhost:5000/search?q=headphones"

# Recommendations for a product
curl http://localhost:5000/recommend/<product_id>
