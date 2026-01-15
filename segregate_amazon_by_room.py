# segregate_amazon_by_room.py
import pandas as pd
import os
import re
import numpy as np

AMAZON_CSV   = "data/amazon_furniture.csv"
OUTPUT_DIR   = "data/amazon_by_room"

# ------------------------------------------------------------------
#  Same keyword map as IKEA
# ------------------------------------------------------------------
KEYWORD_TO_ROOM = {
    "bed": "Bedroom", "mattress": "Bedroom", "nightstand": "Bedroom",
    "night stand": "Bedroom", "dresser": "Bedroom", "wardrobe": "Bedroom",
    "lamp": "Bedroom", "headboard": "Bedroom", "pillow": "Bedroom",
    "duvet": "Bedroom", "bed frame": "Bedroom", "curtain": "Bedroom",

    "stove": "Kitchen", "oven": "Kitchen", "refrigerator": "Kitchen",
    "fridge": "Kitchen", "cabinet": "Kitchen", "table": "Kitchen",
    "chair": "Kitchen", "island": "Kitchen", "microwave": "Kitchen",
    "shelf": "Kitchen", "spice rack": "Kitchen",

    "sofa": "Living Room", "couch": "Living Room", "coffee table": "Living Room",
    "tv stand": "Living Room", "shelf": "Living Room", "rug": "Living Room",
    "armchair": "Living Room", "ottoman": "Living Room", "lamp": "Living Room",
    "curtain": "Living Room", "bookshelf": "Living Room",

    "vanity": "Bathroom", "mirror": "Bathroom", "towel rack": "Bathroom",
    "shelf": "Bathroom", "cabinet": "Bathroom",

    "dining table": "Dining Room", "dining chair": "Dining Room",
    "sideboard": "Dining Room", "buffet": "Dining Room",

    "outdoor": "Balcony", "balcony": "Balcony", "plant": "Balcony",
    "umbrella": "Balcony", "bench": "Balcony", "patio": "Balcony",

    "desk": "Office", "office chair": "Office", "bookshelf": "Office",
    "lamp": "Office",

    "console": "Hallway", "mirror": "Hallway", "coat": "Hallway",
    "bench": "Hallway", "shoe rack": "Hallway", "entryway": "Hallway"
}

def assign_room(title: str) -> str:
    t = str(title).lower()
    for kw, room in KEYWORD_TO_ROOM.items():
        if kw in t:
            return room
    return "General"

# ------------------------------------------------------------------
def main():
    if not os.path.exists(AMAZON_CSV):
        print(f"Error: {AMAZON_CSV} not found!")
        return

    df = pd.read_csv(AMAZON_CSV)
    print(f"Loaded {len(df)} Amazon rows")

    # Normalise columns
    df = df.rename(columns={
        "title": "title", "url": "url", "primary_image": "img_url",
        "price": "price", "sales_rank": "sales_rank"
    }, errors="ignore")

    # Clean price (Amazon sometimes has "$12.34" or "12.34")
    def clean_price(v):
        if pd.isna(v): return np.nan
        s = re.sub(r"[^\d.]", "", str(v))
        return float(s) if s else np.nan
    df["price"] = df["price"].apply(clean_price)

    df["room_type"] = df["title"].apply(assign_room)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    summary = {}
    for room, group in df.groupby("room_type"):
        safe = room.replace(" ", "_")
        out = f"{OUTPUT_DIR}/{safe}.csv"
        group.to_csv(out, index=False)
        summary[room] = len(group)
        print(f"   {len(group):4} → {out}")

    print("\nRoom summary:")
    for r, c in sorted(summary.items(), key=lambda x: x[1], reverse=True):
        print(f"  {r:12}: {c}")

    print(f"\nAll done → {OUTPUT_DIR}")

if __name__ == "__main__":
    main()