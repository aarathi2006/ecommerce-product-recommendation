from flask import Flask, request, render_template
import pandas as pd 
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

app = Flask(__name__)

# Load the files
trending_products = pd.read_csv("models/trending_products.csv")
train_data = pd.read_csv("models/clean_data.csv")

# Function to reduce the product name
def truncate(text, length):
    if len(text) > length:
        return text[:length] + "..."
    else:
        return text

# Function to find closest product match (substring or fuzzy)
def find_best_match(train_data, item_name):
    item_name = item_name.lower().strip()
    
    # Case-insensitive substring search
    matches = train_data[train_data['Name'].str.lower().str.contains(item_name)]
    
    if not matches.empty:
        return matches.iloc[0]['Name']  # return first matched product name
    
    # Fallback to fuzzy matching if no substring match found
    all_names = train_data['Name'].tolist()
    closest = difflib.get_close_matches(item_name, all_names, n=1, cutoff=0.4)
    return closest[0] if closest else None

# Recommendation function
def content_based_recommendations(train_data, item_name, top_n=10):
    matched_name = find_best_match(train_data, item_name)
    
    if not matched_name:
        print(f"No close match found for '{item_name}'")
        return pd.DataFrame()
    
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['Tags'])
    cosine_similarity_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)
    
    item_index = train_data[train_data['Name'] == matched_name].index[0]
    similar_items = list(enumerate(cosine_similarity_content[item_index]))
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)
    top_similar_items = similar_items[1:top_n + 1]
    
    recommended_items_indices = [x[0] for x in top_similar_items]
    recommended_items_details = train_data.iloc[recommended_items_indices][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]
    return recommended_items_details

# List of image URLs
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

# Route for index.html
@app.route("/")
def index():
    trending_products_img_urls = [random.choice(trending_products_img) for _ in range(len(trending_products))]
    price = [259, 529, 800, 489, 529, 699, 999, 399]
    return render_template(
        'index.html',
        trending_products=trending_products.head(8),
        truncate=truncate,
        trending_products_img_urls=trending_products_img_urls,
        random_price=random.choice(price)
    )

# Route for main.html with default variables
@app.route("/main")
def main():
    return render_template('main.html', content_based_rec=None, message=None)

# Redirect to index
@app.route("/index")
def indexredirect():
    trending_products_img_urls = [random.choice(trending_products_img) for _ in range(len(trending_products))]
    price = [259, 529, 800, 489, 529, 699, 999, 399]
    return render_template(
        'index.html',
        trending_products=trending_products.head(8),
        truncate=truncate,
        trending_products_img_urls=trending_products_img_urls,
        random_price=random.choice(price)
    )

# Recommendations route
@app.route("/recommendations", methods=['POST', 'GET'])
def recommendations():
    content_based_rec = None
    message = None
    
    if request.method == 'POST':
        prod = request.form.get('prod')
        nbr = int(request.form.get('nbr'))
        content_based_rec = content_based_recommendations(train_data, prod, top_n=nbr)
        
        if content_based_rec.empty:
            message = f"No recommendations available for '{prod}'."
            content_based_rec = None
    
    return render_template('main.html', content_based_rec=content_based_rec, message=message)

if __name__ == '__main__':
    app.run(debug=True)
