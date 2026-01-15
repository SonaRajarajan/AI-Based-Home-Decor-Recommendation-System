# sentiment_analysis.py
# VADER (Valence Aware Dictionary and sEntiment Reasoner)
import pandas as pd
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import numpy as np

nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()

INPUT_DIR = "data/synthetic_enhanced"
OUTPUT_DIR = "data/synthetic_final"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def add_sentiment(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Warning: {input_file} not found.")
        return
    df = pd.read_csv(input_file)
    print(f"Analyzing {len(df)} products: {os.path.basename(input_file)}")

    scores = []
    sentiments = []
    for _, row in df.iterrows():
        reviews = json.loads(row["review_text"])
        compounds = [sia.polarity_scores(r)["compound"] for r in reviews]
        avg = np.mean(compounds)
        sentiment = "positive" if avg >= 0.05 else ("negative" if avg <= -0.05 else "neutral")
        scores.append(avg)
        sentiments.append(sentiment)

    df["sentiment_score"] = scores
    df["sentiment"] = sentiments

    df.to_csv(output_file, index=False)
    print(f"Saved → {output_file}")

# Run
add_sentiment(f"{INPUT_DIR}/amazon_enhanced.csv", f"{OUTPUT_DIR}/amazon_final.csv")
add_sentiment(f"{INPUT_DIR}/ikea_enhanced.csv", f"{OUTPUT_DIR}/ikea_final.csv")
print("Sentiment analysis complete!")