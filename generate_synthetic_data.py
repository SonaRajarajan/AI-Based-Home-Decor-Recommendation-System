# generate_synthetic_data.py
import pandas as pd
import numpy as np
import random
import json
import os
import re

np.random.seed(42)
random.seed(42)

INPUT_DIR = "data"
OUTPUT_DIR = "data/synthetic_enhanced"
os.makedirs(OUTPUT_DIR, exist_ok=True)

REVIEW_TEMPLATES = [
    "Love this {product}! Super sturdy and stylish.",
    "Great value for money. Easy to assemble. Looks perfect in my {room}.",
    "Perfect fit! Durable and elegant. 5 stars!",
    "Assembly was tricky, but worth it. Good quality.",
    "Color not as expected. Otherwise fine.",
    "Best purchase! Transformed my {room}.",
    "Overpriced for the quality.",
    "Amazing! Will buy again.",
    "Fell apart after a week. Poor quality.",
    "Exactly what I needed. Highly recommend."
]
ROOMS = ["bedroom", "kitchen", "living room", "bathroom", "office", "hallway", "balcony"]

def clean_price(val):
    if pd.isna(val): return np.nan
    s = re.sub(r"[^\d.]", "", str(val))
    return float(s) if s else np.nan

def generate_enhanced_csv(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Warning: {input_file} not found.")
        return
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} rows from {input_file}")

    # Clean price
    df["price"] = df["price"].apply(clean_price)
    df = df.dropna(subset=["title", "name"])  # Ensure title/name exists

    # Add synthetic columns
    df["num_reviews"] = np.random.randint(10, 1000, size=len(df))
    df["num_purchases"] = np.random.randint(50, 5000, size=len(df))

    reviews_list = []
    for i in range(len(df)):
        product = df["title"].iloc[i].split()[0] if "title" in df.columns else df["name"].iloc[i].split()[0]
        room = random.choice(ROOMS)
        reviews = [t.format(product=product, room=room) for t in random.sample(REVIEW_TEMPLATES, 3)]
        reviews_list.append(json.dumps(reviews))
    df["review_text"] = reviews_list

    df.to_csv(output_file, index=False)
    print(f"Enhanced → {output_file}")

# Run
generate_enhanced_csv("data/amazon_furniture.csv", f"{OUTPUT_DIR}/amazon_enhanced.csv")
generate_enhanced_csv("data/ikea_furniture.csv", f"{OUTPUT_DIR}/ikea_enhanced.csv")
print("Synthetic columns added!")