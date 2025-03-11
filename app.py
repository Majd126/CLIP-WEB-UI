from flask import Flask, render_template, request, redirect, url_for
import torch
import clip
import numpy as np
import pickle
import os
from PIL import Image

# Initialize Flask app
app = Flask(__name__)

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Load precomputed embeddings
with open("embeddings/embeddings.pkl", "rb") as f:
    embeddings = pickle.load(f)

# Function to encode text query
def encode_text(query):
    text_input = clip.tokenize([query]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text_input)
    return text_features.cpu().numpy()

# Function to encode image query
def encode_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
    return image_features.cpu().numpy()

# Function to compute cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b))

# Function to search for images
def search_images(query, similarity_threshold=0.0):
    # Encode query (text or image)
    if isinstance(query, str):  # Text query
        query_features = encode_text(query)
    else:  # Image query
        query_features = encode_image(query)
    
    # Compute similarities
    similarities = {}
    for image_path, image_features in embeddings.items():
        sim = cosine_similarity(query_features, image_features)
        similarities[image_path] = sim[0][0]
    
    # Filter by similarity threshold
    filtered_images = [(path, sim) for path, sim in similarities.items() if sim >= similarity_threshold]
    
    # Sort by similarity (no top_k limit)
    sorted_images = sorted(filtered_images, key=lambda x: x[1], reverse=True)
    
    return sorted_images

# Route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        similarity_threshold = float(request.form.get("similarity_threshold", 0.0))
        if "query" in request.form:  # Text search
            query = request.form["query"]
            results = search_images(query, similarity_threshold=similarity_threshold)
            return render_template("index.html", query=query, results=results, similarity_threshold=similarity_threshold)
        elif "image" in request.files:  # Image search
            image_file = request.files["image"]
            if image_file.filename != "":
                # Save the uploaded image temporarily
                upload_path = os.path.join("static", "uploads", image_file.filename)
                os.makedirs(os.path.dirname(upload_path), exist_ok=True)
                image_file.save(upload_path)
                
                # Perform image-to-image search
                results = search_images(upload_path, similarity_threshold=similarity_threshold)
                
                # Delete the uploaded image after processing
                os.remove(upload_path)
                
                return render_template("index.html", query=None, results=results, similarity_threshold=similarity_threshold)
    return render_template("index.html", query=None, results=None, similarity_threshold=0.0)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)