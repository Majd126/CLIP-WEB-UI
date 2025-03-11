import os
import torch
import clip
from PIL import Image
import numpy as np
import pickle
from tqdm import tqdm

# Load CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Paths
image_folder = "static/images"  # Images are now in the static/images folder
embeddings_folder = "embeddings"
os.makedirs(embeddings_folder, exist_ok=True)

# Function to compute embeddings for a single image
def compute_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
    return image_features.cpu().numpy()

# Compute embeddings for all images
image_paths = [os.path.join(image_folder, fname) for fname in os.listdir(image_folder)]
embeddings = {}

for image_path in tqdm(image_paths, desc="Computing embeddings"):
    # Store the relative path from the static folder
    relative_path = os.path.relpath(image_path, start="static")
    # Replace backslashes with forward slashes for compatibility
    relative_path = relative_path.replace("\\", "/")
    
    # Compute the embedding
    embedding = compute_embedding(image_path)
    embeddings[relative_path] = embedding

# Save embeddings to disk
with open(os.path.join(embeddings_folder, "embeddings.pkl"), "wb") as f:
    pickle.dump(embeddings, f)

print("Embeddings computed and saved with correct paths.")