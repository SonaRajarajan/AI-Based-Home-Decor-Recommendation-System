# segregate_ikea_by_room.py
# Splits IKEA CSV into one file per room (Bedroom, Kitchen, …)
# Works exactly like the Amazon splitter you already love.

import pandas as pd
import os
import re

# ----------------------------------------------------------------------
IKEA_CSV   = "data/ikea_furniture.csv"
OUTPUT_DIR = "data/ikea_by_room"
# ----------------------------------------------------------------------


# --------------------------------------------------------------
# 1. Keyword → room (used on *title*)
# --------------------------------------------------------------
TITLE_KEYWORD_TO_ROOM = {
    # Bedroom
    "bed": "Bedroom", "mattress": "Bedroom", "nightstand": "Bedroom",
    "night stand": "Bedroom", "dresser": "Bedroom", "wardrobe": "Bedroom",
    "lamp": "Bedroom", "headboard": "Bedroom", "pillow": "Bedroom",
    "duvet": "Bedroom", "bed frame": "Bedroom", "curtain": "Bedroom",

    # Kitchen
    "stove": "Kitchen", "oven": "Kitchen", "refrigerator": "Kitchen",
    "fridge": "Kitchen", "cabinet": "Kitchen", "table": "Kitchen",
    "chair": "Kitchen", "island": "Kitchen", "microwave": "Kitchen",
    "shelf": "Kitchen", "spice rack": "Kitchen",

    # Living Room
    "sofa": "Living Room", "couch": "Living Room", "coffee table": "Living Room",
    "tv stand": "Living Room", "shelf": "Living Room", "rug": "Living Room",
    "armchair": "Living Room", "ottoman": "Living Room", "lamp": "Living Room",
    "curtain": "Living Room", "bookshelf": "Living Room",

    # Bathroom
    "vanity": "Bathroom", "mirror": "Bathroom", "towel rack": "Bathroom",
    "shelf": "Bathroom", "cabinet": "Bathroom",

    # Dining Room
    "dining table": "Dining Room", "dining chair": "Dining Room",
    "sideboard": "Dining Room", "buffet": "Dining Room",

    # Balcony / Outdoor
    "outdoor": "Balcony", "balcony": "Balcony", "plant": "Balcony",
    "umbrella": "Balcony", "bench": "Balcony", "patio": "Balcony",

    # Office
    "desk": "Office", "office chair": "Office", "bookshelf": "Office",
    "lamp": "Office",

    # Hallway
    "console": "Hallway", "mirror": "Hallway", "coat": "Hallway",
    "bench": "Hallway", "shoe rack": "Hallway", "entryway": "Hallway"
}


# --------------------------------------------------------------
# 2. IKEA **category** → room (the real source of truth)
# --------------------------------------------------------------
CATEGORY_TO_ROOM = {
    # ---- Bedroom -------------------------------------------------
    "Beds": "Bedroom",
    "Mattresses": "Bedroom",
    "Nightstands": "Bedroom",
    "Dressers & chest of drawers": "Bedroom",
    "Wardrobes": "Bedroom",
    "Bedroom storage": "Bedroom",
    "Bedroom textiles": "Bedroom",

    # ---- Kitchen -------------------------------------------------
    "Kitchen cabinets": "Kitchen",
    "Kitchen worktops": "Kitchen",
    "Kitchen sinks & taps": "Kitchen",
    "Kitchen appliances": "Kitchen",
    "Kitchen islands & trolleys": "Kitchen",
    "Kitchen tables & chairs": "Kitchen",

    # ---- Living Room ---------------------------------------------
    "Sofas & sectionals": "Living Room",
    "Armchairs & chaise longues": "Living Room",
    "TV & media furniture": "Living Room",
    "Coffee & side tables": "Living Room",
    "Bookcases & shelving units": "Living Room",
    "Rugs": "Living Room",

    # ---- Bathroom ------------------------------------------------
    "Bathroom furniture": "Bathroom",
    "Bathroom storage": "Bathroom",
    "Bathroom textiles": "Bathroom",

    # ---- Dining --------------------------------------------------
    "Dining tables": "Dining Room",
    "Dining chairs": "Dining Room",
    "Dining sets": "Dining Room",
    "Sideboards & buffet tables": "Dining Room",

    # ---- Outdoor / Balcony ---------------------------------------
    "Outdoor furniture": "Balcony",
    "Balcony furniture": "Balcony",
    "Garden tables": "Balcony",
    "Garden chairs": "Balcony",

    # ---- Office --------------------------------------------------
    "Desks & computer desks": "Office",
    "Office chairs": "Office",
    "Office storage": "Office",

    # ---- Hallway -------------------------------------------------
    "Hallway furniture": "Hallway",
    "Shoe cabinets": "Hallway",
    "Coat racks & stands": "Hallway",
    "Console tables": "Hallway"
}


# --------------------------------------------------------------
def assign_room(row) -> str:
    """Return the room name for a single product row."""
    # 1. Try title first
    title = str(row.get("title") or row.get("name") or "").lower()
    for kw, room in TITLE_KEYWORD_TO_ROOM.items():
        if kw in title:
            return room

    # 2. Try category column (IKEA's official room)
    cat = str(row.get("category") or "").strip()
    if cat in CATEGORY_TO_ROOM:
        return CATEGORY_TO_ROOM[cat]

    # 3. Fallback
    return "General"


# --------------------------------------------------------------
def main():
    if not os.path.exists(IKEA_CSV):
        print(f"Error: {IKEA_CSV} not found!")
        return

    df = pd.read_csv(IKEA_CSV)
    print(f"Loaded {len(df):,} IKEA rows")

    # Normalise column names (keep everything, just add room_type)
    df = df.rename(columns={
        "name": "title", "link": "url", "image": "img_url"
    }, errors="ignore")

    # ------------------------------------------------------------------
    # Add the room column
    # ------------------------------------------------------------------
    df["room_type"] = df.apply(assign_room, axis=1)

    # ------------------------------------------------------------------
    # Write one CSV per room
    # ------------------------------------------------------------------
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    summary = {}
    for room, group in df.groupby("room_type"):
        safe_name = room.replace(" ", "_")
        out_path  = f"{OUTPUT_DIR}/{safe_name}.csv"
        group.to_csv(out_path, index=False)
        summary[room] = len(group)
        print(f"   {len(group):4,} → {out_path}")

    # ------------------------------------------------------------------
    # Pretty summary
    # ------------------------------------------------------------------
    print("\nRoom summary:")
    for r, c in sorted(summary.items(), key=lambda x: x[1], reverse=True):
        print(f"  {r:12}: {c:,}")

    print(f"\nAll done → {OUTPUT_DIR}")


if __name__ == "__main__":
    main()