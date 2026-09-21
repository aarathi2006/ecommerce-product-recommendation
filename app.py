from flask import Flask, request, render_template
import pandas as pd
import random
import os
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────
# STEP 1: Load data ONCE at startup (not on every request)
# ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

trending_products = pd.read_csv(os.path.join(BASE_DIR, "models", "trending_products.csv"))
train_data = pd.read_csv(os.path.join(BASE_DIR, "models", "clean_data.csv"))

# ─────────────────────────────────────────────────────────────
# STEP 2: Compute TF-IDF matrix ONCE at startup
# This is the heavy operation. Doing it per-request kills the worker.
# ─────────────────────────────────────────────────────────────
print("[startup] Building TF-IDF matrix...")
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(train_data['Tags'])
print(f"[startup] TF-IDF matrix shape: {tfidf_matrix.shape}")

# ─────────────────────────────────────────────────────────────
# STEP 3: Compute cosine similarity ONCE at startup
# For 5,000 products this is a 5000x5000 matrix (~200MB).
# Doing this once is fine. Doing it per-request is what caused the 502.
# ─────────────────────────────────────────────────────────────
print("[startup] Computing cosine similarity...")
cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
print(f"[startup] Cosine similarity matrix shape: {cosine_sim_matrix.shape}")

# Pre-compute a lowercase name index for faster matching
_name_lower = train_data['Name'].str.lower()
print("[startup] Ready.")


# ─────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────
def truncate(text, length):
    if len(text) > length:
        return text[:length] + "..."
    return text


def find_best_match(train_data, item_name):
    item_name = item_name.lower().strip()
    matches = train_data[_name_lower.str.contains(item_name, na=False)]
    if not matches.empty:
        return matches.iloc[0]['Name']

    all_names = train_data['Name'].tolist()
    closest = difflib.get_close_matches(item_name, all_names, n=1, cutoff=0.4)
    return closest[0] if closest else None


def content_based_recommendations(item_name, top_n=10):
    """Uses the pre-computed cosine_sim_matrix. Fast and memory-safe."""
    matched_name = find_best_match(train_data, item_name)

    if not matched_name:
        print(f"[recommend] No close match found for '{item_name}'")
        return pd.DataFrame()

    item_matches = train_data[train_data['Name'] == matched_name]
    if item_matches.empty:
        return pd.DataFrame()

    item_index = item_matches.index[0]

    # Use the pre-computed similarity matrix — just index into it
    similar_items = list(enumerate(cosine_sim_matrix[item_index]))
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)
    top_similar_items = similar_items[1:top_n + 1]

    recommended_items_indices = [x[0] for x in top_similar_items]
    return train_data.iloc[recommended_items_indices][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]


# ─────────────────────────────────────────────────────────────
# Image URLs and pricing
# ─────────────────────────────────────────────────────────────
trending_products_img = [
    "static/img/download (1).jpeg",
    "static/img/download.jpeg",
    "static/img/gold-3184583_640.jpg",
    "static/img/images (1).jpeg",
    "static/img/images (2).jpeg",
    "static/img/images (3).jpeg",
    "static/img/product-jpeg-500x500.webp",
    "static/img/images.jpeg"
]

PRICE_OPTIONS = [259, 529, 800, 489, 529, 699, 999, 399]


# ─────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    imgs = [random.choice(trending_products_img) for _ in range(len(trending_products))]
    return render_template(
        'index.html',
        trending_products=trending_products.head(8),
        truncate=truncate,
        trending_products_img_urls=imgs,
        random_price=random.choice(PRICE_OPTIONS)
    )


@app.route("/main")
def main():
    return render_template('main.html', content_based_rec=None, message=None)


@app.route("/index")
def indexredirect():
    imgs = [random.choice(trending_products_img) for _ in range(len(trending_products))]
    return render_template(
        'index.html',
        trending_products=trending_products.head(8),
        truncate=truncate,
        trending_products_img_urls=imgs,
        random_price=random.choice(PRICE_OPTIONS)
    )


@app.route("/recommendations", methods=['POST', 'GET'])
def recommendations():
    content_based_rec = None
    message = None

    if request.method == 'POST':
        prod = request.form.get('prod', '').strip()
        nbr_raw = request.form.get('nbr', '5')

        if not prod:
            message = "Please enter a product name."
        else:
            try:
                nbr = int(nbr_raw)
                nbr = max(1, min(nbr, 20))  # clamp between 1 and 20
            except (ValueError, TypeError):
                nbr = 5

            content_based_rec = content_based_recommendations(prod, top_n=nbr)

            if content_based_rec is None or content_based_rec.empty:
                message = f"No recommendations available for '{prod}'."
                content_based_rec = None

    return render_template('main.html', content_based_rec=content_based_rec, message=message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)

