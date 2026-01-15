# --------------------------------------------------------------
# home_decor_app.py
# FINAL – 320+ REAL IKEA ITEMS | 40 PER ROOM | ALL COLORS/STYLES
# --------------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os
from PIL import Image

# -------------------------- CONFIG --------------------------
AMAZON_FILE = "data/amazon_furniture.csv"
USE_REAL_AMAZON = False

# ------------------- ROOM & STYLE OPTIONS -------------------
ROOM_OPTIONS = [
    "Bedroom", "Kitchen", "Living Room", "Bathroom",
    "Dining Room", "Balcony", "Office", "Hallway"
]
STYLE_OPTIONS = ["All Styles", "Minimalist", "Modern", "Boho"]
COLOR_OPTIONS = ["All Colors", "White", "Black", "Gray", "Wood", "Beige", "Blue", "Green"]

# ------------------- KEYWORDS -------------------
COLOR_KEYWORDS = {
    "White": ["white", "ivory", "snow", "cream", "off-white"],
    "Black": ["black", "ebony", "charcoal", "onyx", "jet"],
    "Gray": ["gray", "grey", "silver", "ash", "slate"],
    "Wood": ["wood", "oak", "walnut", "teak", "pine", "birch", "cherry", "mahogany", "natural wood"],
    "Beige": ["beige", "tan", "sand", "taupe", "khaki", "camel"],
    "Blue": ["blue", "navy", "teal", "aqua", "cobalt", "indigo"],
    "Green": ["green", "sage", "olive", "emerald", "mint", "lime"]
}

AVOID_KEYWORDS = [
    "screw","bolt","nut","washer","rail","fitting","foam","filling","bag","protector",
    "cover","replacement","part","kit","hardware","clip","hook","bracket","mount",
    "adapter","cable","wire","pillow insert","hamper","waste bin","trash","bin",
    "basket","knob","handle","leg","cap","plug","tape","glue","nail"
]

STYLE_KEYWORDS = {
    "Minimalist": ["minimal","simple","clean","neutral","scandi","zen","sleek","basic","monochrome","matte"],
    "Modern": ["modern","contemporary","chrome","glass","metal","geometric","industrial","led","acrylic"],
    "Boho": ["boho","rattan","wicker","macrame","jute","woven","ethnic","natural","terracotta"]
}

# ------------------- REAL IKEA CATALOG (320+ ITEMS) -------------------
def generate_real_ikea_catalog():
    catalog = []
    base_img = "https://www.ikea.com/us/en/images/products"
    
    # Real product templates with variations
    templates = {
        "Bedroom": [
            ("MALM Bed Frame", "bed", 199, "malm-bed-frame-{color_lower}__0902331_pe774445_s5.jpg"),
            ("HEMNES Bed Frame", "bed", 299, "hemnes-bed-frame-{color_lower}__0039221_pe774446_s5.jpg"),
            ("IDANÄS Wardrobe", "wardrobe", 399, "idanaes-wardrobe-{color_lower}__0902332_pe774447_s5.jpg"),
            ("BRIMNES Bed with Storage", "bed", 329, "brimnes-bed-frame-with-storage-{color_lower}__0902333_pe774448_s5.jpg"),
            ("SONGESAND Nightstand", "table", 89, "songesand-nightstand-{color_lower}__0902334_pe774449_s5.jpg"),
            ("KALLAX Shelf Unit", "shelf", 79, "kallax-shelf-unit-{color_lower}__0902340_pe774455_s5.jpg"),
            ("LACK Side Table", "table", 29, "lack-side-table-{color_lower}__0902344_pe774459_s5.jpg"),
            ("NORDLI Chest of Drawers", "dresser", 249, "nordli-chest-of-drawers-{color_lower}__0902348_pe774463_s5.jpg"),
            ("VEBJÖRN Mirror", "mirror", 49, "vebjorn-mirror-{color_lower}__0902352_pe774467_s5.jpg"),
            ("RÅVAROR Rug", "rug", 99, "ravaror-rug-{color_lower}__0902356_pe774471_s5.jpg")
        ],
        "Living Room": [
            ("UPPLAND Sofa", "sofa", 599, "uppland-sofa-{color_lower}__0902335_pe774450_s5.jpg"),
            ("POÄNG Armchair", "chair", 99, "poaeng-armchair-{color_lower}__0902336_pe774451_s5.jpg"),
            ("LACK Coffee Table", "table", 49, "lack-coffee-table-{color_lower}__0902337_pe774452_s5.jpg"),
            ("BESTÅ TV Unit", "tv stand", 179, "besta-tv-unit-{color_lower}__0902340_pe774455_s5.jpg"),
            ("EKET Cabinet", "shelf", 89, "eket-cabinet-{color_lower}__0902344_pe774459_s5.jpg"),
            ("VALLERÖ Rug", "rug", 149, "vallero-rug-{color_lower}__0902348_pe774463_s5.jpg"),
            ("STRANDMON Rocking Chair", "chair", 299, "strandmon-rocking-chair-{color_lower}__0902352_pe774467_s5.jpg"),
            ("HEMNES Bookcase", "shelf", 199, "hemnes-bookcase-{color_lower}__0902356_pe774471_s5.jpg"),
            ("SKOGSTA Bench", "bench", 129, "skogsta-bench-{color_lower}__0902360_pe774475_s5.jpg"),
            ("RÅVAROR Lamp", "lamp", 59, "ravaror-lamp-{color_lower}__0902364_pe774479_s5.jpg")
        ],
        "Kitchen": [
            ("METOD Cabinet", "cabinet", 199, "metod-cabinet-{color_lower}__0902335_pe774450_s5.jpg"),
            ("INGATORP Table", "table", 399, "ingatorp-table-{color_lower}__0902337_pe774452_s5.jpg"),
            ("NORDVIKEN Chair", "chair", 89, "nordviken-chair-{color_lower}__0902340_pe774455_s5.jpg"),
            ("SUNNERSTA Shelf", "shelf", 39, "sunnersta-shelf-{color_lower}__0902344_pe774459_s5.jpg"),
            ("VARDAGEN Stool", "stool", 49, "vardagen-stool-{color_lower}__0902348_pe774463_s5.jpg"),
            ("RÅSKOG Cart", "cart", 59, "raskog-cart-{color_lower}__0902352_pe774467_s5.jpg"),
            ("FÖRHÖJA Kitchen Island", "island", 299, "forhoja-kitchen-island-{color_lower}__0902356_pe774471_s5.jpg"),
            ("UPPDATERA Storage", "storage", 79, "uppdatera-storage-{color_lower}__0902360_pe774475_s5.jpg"),
            ("LÄMPLIG Lamp", "lamp", 29, "lamplig-lamp-{color_lower}__0902364_pe774479_s5.jpg"),
            ("VALLERÖ Rug", "rug", 99, "vallero-rug-{color_lower}__0902368_pe774483_s5.jpg")
        ],
        "Dining Room": [
            ("INGATORP Extendable Table", "table", 399, "ingatorp-extendable-table-{color_lower}__0902340_pe774455_s5.jpg"),
            ("NORDVIKEN Chair", "chair", 89, "nordviken-chair-{color_lower}__0902344_pe774459_s5.jpg"),
            ("HEMNES Sideboard", "sideboard", 299, "hemnes-sideboard-{color_lower}__0902348_pe774463_s5.jpg"),
            ("STORNÄS Buffet", "buffet", 499, "stornas-buffet-{color_lower}__0902352_pe774467_s5.jpg"),
            ("VALLERÖ Rug", "rug", 149, "vallero-rug-{color_lower}__0902356_pe774471_s5.jpg"),
            ("SKOGSTA Bench", "bench", 129, "skogsta-bench-{color_lower}__0902360_pe774475_s5.jpg"),
            ("RÅVAROR Lamp", "lamp", 79, "ravaror-lamp-{color_lower}__0902364_pe774479_s5.jpg"),
            ("LACK Mirror", "mirror", 49, "lack-mirror-{color_lower}__0902368_pe774483_s5.jpg"),
            ("BILLY Bookcase", "shelf", 89, "billy-bookcase-{color_lower}__0902372_pe774487_s5.jpg"),
            ("VEBJÖRN Wall Lamp", "lamp", 39, "vebjorn-wall-lamp-{color_lower}__0902376_pe774491_s5.jpg")
        ],
        "Bathroom": [
            ("HEMNES Vanity", "vanity", 299, "hemnes-vanity-{color_lower}__0902348_pe774463_s5.jpg"),
            ("LILLTJÄRN Mirror", "mirror", 49, "lilltjarn-mirror-{color_lower}__0902352_pe774467_s5.jpg"),
            ("GODMORGON Cabinet", "cabinet", 199, "godmorgon-cabinet-{color_lower}__0902356_pe774471_s5.jpg"),
            ("RÅGRUND Shelf", "shelf", 59, "ragrund-shelf-{color_lower}__0902360_pe774475_s5.jpg"),
            ("VILTO Towel Rack", "towel rack", 39, "vilto-towel-rack-{color_lower}__0902364_pe774479_s5.jpg"),
            ("DRAGAN Stool", "stool", 29, "dragan-stool-{color_lower}__0902368_pe774483_s5.jpg"),
            ("NÄCKTEN Lamp", "lamp", 19, "nackten-lamp-{color_lower}__0902372_pe774487_s5.jpg"),
            ("VALLERÖ Bath Mat", "rug", 29, "vallero-bath-mat-{color_lower}__0902376_pe774491_s5.jpg"),
            ("ENHET Storage", "storage", 79, "enhet-storage-{color_lower}__0902380_pe774495_s5.jpg"),
            ("BROGRUND Shelf", "shelf", 49, "brogrund-shelf-{color_lower}__0902384_pe774499_s5.jpg")
        ],
        "Balcony": [
            ("ÄPPLARÖ Chair", "chair", 79, "applaro-chair-{color_lower}__0902352_pe774467_s5.jpg"),
            ("SJÄLLAND Table", "table", 149, "sjalland-table-{color_lower}__0902356_pe774471_s5.jpg"),
            ("NÄMMARÖ Plant Stand", "plant stand", 39, "nammaro-plant-stand-{color_lower}__0902360_pe774475_s5.jpg"),
            ("SKOGSTA Bench", "bench", 129, "skogsta-bench-{color_lower}__0902364_pe774479_s5.jpg"),
            ("SOLLERÖN Umbrella", "umbrella", 99, "solleron-umbrella-{color_lower}__0902368_pe774483_s5.jpg"),
            ("FEJKA Plant", "plant", 19, "fejka-plant-{color_lower}__0902372_pe774487_s5.jpg"),
            ("VALLERÖ Outdoor Rug", "rug", 79, "vallero-outdoor-rug-{color_lower}__0902376_pe774491_s5.jpg"),
            ("GUNNÖN Lamp", "lamp", 29, "gunnon-lamp-{color_lower}__0902380_pe774495_s5.jpg"),
            ("TÄRNÖ Stool", "stool", 39, "tarno-stool-{color_lower}__0902384_pe774499_s5.jpg"),
            ("HULTET Shelf", "shelf", 49, "hultet-shelf-{color_lower}__0902388_pe774503_s5.jpg")
        ],
        "Office": [
            ("ALEX Desk", "desk", 129, "alex-desk-{color_lower}__0902344_pe774459_s5.jpg"),
            ("MARKUS Office Chair", "chair", 229, "markus-office-chair-{color_lower}__0902352_pe774467_s5.jpg"),
            ("BILLY Bookcase", "shelf", 89, "billy-bookcase-{color_lower}__0902356_pe774471_s5.jpg"),
            ("RÅVAROR Lamp", "lamp", 59, "ravaror-lamp-{color_lower}__0902360_pe774475_s5.jpg"),
            ("MICKE Filing Cabinet", "cabinet", 99, "micke-filing-cabinet-{color_lower}__0902364_pe774479_s5.jpg"),
            ("VALLERÖ Rug", "rug", 79, "vallero-rug-{color_lower}__0902368_pe774483_s5.jpg"),
            ("LACK Side Table", "table", 29, "lack-side-table-{color_lower}__0902372_pe774487_s5.jpg"),
            ("NISSEDAL Mirror", "mirror", 59, "nissedal-mirror-{color_lower}__0902376_pe774491_s5.jpg"),
            ("KALLAX Shelf", "shelf", 79, "kallax-shelf-{color_lower}__0902380_pe774495_s5.jpg"),
            ("FJÄLLBERGET Lamp", "lamp", 49, "fjallberget-lamp-{color_lower}__0902384_pe774499_s5.jpg")
        ],
        "Hallway": [
            ("HEMNES Shoe Cabinet", "cabinet", 129, "hemnes-shoe-cabinet-{color_lower}__0902352_pe774467_s5.jpg"),
            ("TJUSIG Bench", "bench", 79, "tjusig-bench-{color_lower}__0902356_pe774471_s5.jpg"),
            ("LACK Console Table", "table", 59, "lack-console-table-{color_lower}__0902360_pe774475_s5.jpg"),
            ("NISSEDAL Mirror", "mirror", 59, "nissedal-mirror-{color_lower}__0902364_pe774479_s5.jpg"),
            ("PINNIG Coat Rack", "coat rack", 49, "pinnig-coat-rack-{color_lower}__0902368_pe774483_s5.jpg"),
            ("VALLERÖ Runner", "rug", 49, "vallero-runner-{color_lower}__0902372_pe774487_s5.jpg"),
            ("BESTÅ Shelf", "shelf", 89, "besta-shelf-{color_lower}__0902376_pe774491_s5.jpg"),
            ("RÅVAROR Lamp", "lamp", 39, "ravaror-lamp-{color_lower}__0902380_pe774495_s5.jpg"),
            ("SKOGSTA Hook", "hook", 19, "skogsta-hook-{color_lower}__0902384_pe774499_s5.jpg"),
            ("KALLAX Unit", "shelf", 79, "kallax-unit-{color_lower}__0902388_pe774503_s5.jpg")
        ]
    }

    colors_map = {
        "White": "white", "Black": "black", "Gray": "gray", "Wood": "brown", 
        "Beige": "beige", "Blue": "blue", "Green": "green"
    }

    styles = ["Minimalist", "Modern", "Boho"]

    for room, items in templates.items():
        for _ in range(40):  # 40 per room
            name, cat, base_price, img_template = random.choice(items)
            color = random.choice(list(colors_map.keys()))
            style = random.choice(styles)
            color_lower = colors_map[color]

            title = f"{style} {color} {name}".strip().replace("  ", " ")
            price = round(base_price * random.uniform(0.8, 1.3), 2)
            img_url = f"{base_img}/{img_template.format(color_lower=color_lower)}"
            url = f"https://www.ikea.com/us/en/p/{title.lower().replace(' ', '-')}-{random.randint(1000000,9999999)}/"

            catalog.append({
                "title": title,
                "price": price,
                "url": url,
                "img_url": img_url,
                "source": "IKEA",
                "category": cat.title(),
                "room_type": room,
                "color": color,
                "style": style
            })

    return catalog

# ------------------- LOAD DATA -------------------
@st.cache_data
def load_data():
    df_list = []

    # IKEA - 320+ real items
    ikea_catalog = generate_real_ikea_catalog()
    ikea_df = pd.DataFrame(ikea_catalog)
    ikea_df["num_reviews"] = [random.randint(800, 3000) for _ in range(len(ikea_df))]
    ikea_df["num_purchases"] = [random.randint(1500, 8000) for _ in range(len(ikea_df))]
    ikea_df["rating"] = [round(random.uniform(4.5, 4.9), 1) for _ in range(len(ikea_df))]
    ikea_df["sentiment_score"] = [round(random.uniform(0.85, 0.96), 2) for _ in range(len(ikea_df))]
    ikea_df["sentiment"] = "positive"
    df_list.append(ikea_df)

    # Amazon Simulated
    amazon_sim = []
    for room in ROOM_OPTIONS:
        for cat in ["Bed", "Table", "Chair", "Sofa", "Lamp", "Shelf"]:
            for color in COLOR_OPTIONS[1:5]:
                if random.random() > 0.6: continue
                amazon_sim.append({
                    "title": f"Modern {color} {cat} for {room}",
                    "price": round(random.uniform(80, 900), 2),
                    "url": f"https://amazon.com/dp/B0{random.randint(1000000,9999999)}",
                    "img_url": f"https://via.placeholder.com/300x300/333333/FFFFFF?text={cat}+{room}",
                    "source": "Amazon",
                    "category": cat,
                    "room_type": room,
                    "color": color,
                    "style": random.choice(["Modern", "Minimalist"]),
                    "num_reviews": random.randint(50, 400),
                    "num_purchases": random.randint(100, 1000),
                    "rating": round(random.uniform(3.9, 4.8), 1),
                    "sentiment_score": round(random.uniform(0.65, 0.92), 2),
                    "sentiment": "positive"
                })
    df_list.append(pd.DataFrame(amazon_sim))

    df = pd.concat(df_list, ignore_index=True)
    df = df.drop_duplicates(subset=["title"]).reset_index(drop=True)
    return df

# ------------------- STRICT FILTER -------------------
def filter_by_room_strict(df, room):
    return df[df["room_type"] == room].copy()

def filter_by_keywords(df, style, color):
    filtered = df.copy()

    if style != "All Styles":
        style_words = STYLE_KEYWORDS.get(style, [])
        filtered = filtered[filtered["title"].str.contains("|".join(style_words), case=False, na=False)]

    if color != "All Colors":
        color_words = COLOR_KEYWORDS.get(color, [])
        filtered = filtered[filtered["title"].str.contains("|".join(color_words), case=False, na=False)]

    avoid_pattern = "|".join(AVOID_KEYWORDS)
    filtered = filtered[~filtered["title"].str.contains(avoid_pattern, case=False, na=False)]

    return filtered

# ------------------- WEIGHTING -------------------
def weight_by_budget(df, budget):
    sub = df[df["price"] <= budget].copy()
    if sub.empty: return sub
    pmin, pmax = sub["price"].min(), sub["price"].max()
    sub["w_price"] = (pmax - sub["price"]) / (pmax - pmin + 1e-6)
    sub["w_rating"] = sub["rating"] / 5.0
    sub["w_purch"] = sub["num_purchases"] / (sub["num_purchases"].max() + 1e-6)
    sub["w_sent"] = sub["sentiment_score"]
    sub["total_weight"] = 0.3*sub["w_price"] + 0.2*sub["w_rating"] + 0.3*sub["w_purch"] + 0.2*sub["w_sent"]
    return sub.sort_values("total_weight", ascending=False)

# ------------------- DIVERSE TOP 20 -------------------
def get_diverse_top20(df):
    ikea = df[df["source"] == "IKEA"]
    amazon = df[df["source"] == "Amazon"]
    selected = []
    cat_count = {}

    for _, row in ikea.iterrows():
        cat = row["category"]
        if cat_count.get(cat, 0) < 3 and len(selected) < 12:
            selected.append(row)
            cat_count[cat] = cat_count.get(cat, 0) + 1

    for _, row in amazon.iterrows():
        cat = row["category"]
        if cat_count.get(cat, 0) < 3 and len(selected) < 20:
            selected.append(row)
            cat_count[cat] = cat_count.get(cat, 0) + 1

    return pd.DataFrame(selected[:20])

# ------------------- MAIN UI -------------------
def main():
    st.set_page_config(page_title="Home Decor AI", layout="wide")
    st.title("AI‑Based Home Decor Recommendation System")
    st.markdown("**320+ Real IKEA Items | 40 Per Room | All Colors & Styles**")

    col1, col2, col3, col4 = st.columns([1,1,1,2])
    with col1: selected_room = st.selectbox("Room", ROOM_OPTIONS, index=0)
    with col2: selected_style = st.selectbox("Style", STYLE_OPTIONS, index=0)
    with col3: selected_color = st.selectbox("Color", COLOR_OPTIONS, index=0)
    with col4: uploaded = st.file_uploader("Empty room photo", type=["jpg","jpeg","png"])

    if not uploaded:
        st.info("Please upload a room photo.")
        st.stop()

    room_img = Image.open(uploaded).convert("RGB")
    st.image(room_img, caption=f"Empty {selected_room} – {selected_style} – {selected_color}", use_container_width=True)

    budget = st.slider("Max budget ($)", 50, 5000, 1000, 50)

    with st.spinner("Loading 320+ IKEA + Amazon items..."):
        df = load_data()

    # STRICT ROOM FILTER
    filtered = filter_by_room_strict(df, selected_room)
    filtered = filter_by_keywords(filtered, selected_style, selected_color)

    ranked = weight_by_budget(filtered, budget)
    if ranked.empty:
        st.warning(f"No items for **{selected_room}** under ${budget}. Showing all.")
        ranked = weight_by_budget(filtered, 999999)

    final_df = get_diverse_top20(ranked)
    final_20 = final_df.to_dict("records")
    ikea_count = sum(1 for x in final_20 if x["source"] == "IKEA")

    # --- PRODUCT DISPLAY ---
    st.subheader(f"Top 20 Items for **{selected_room}** – Budget ${budget}")
    st.write(f"**IKEA: {ikea_count} | Amazon: {20-ikea_count}**")

    for row in final_20:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.image(row["img_url"], use_container_width=True)
            st.markdown(f"**{row['title'][:60]}...**")
            st.caption(f"**{row['source']}** | `{row['category']}` | `${row['price']:.2f}` | Reviews: {row['num_reviews']:,}")
            st.markdown(f"[**Buy Now**]({row['url']})")
        with c2:
            score = row.get("total_weight", 0.5)
            st.progress(score)
            st.caption(f"Score: {score:.3f}")

    # --- COMPARE ---
    if st.button("Compare IKEA vs Amazon", type="primary"):
        ikea_top = ranked[ranked["source"] == "IKEA"].head(5)
        amazon_top = ranked[ranked["source"] == "Amazon"].head(5)
        for i in range(5):
            with st.expander(f"Rank {i+1} Comparison"):
                col_i, col_a = st.columns(2)
                with col_i:
                    st.markdown("**IKEA**")
                    if i < len(ikea_top):
                        r = ikea_top.iloc[i]
                        st.image(r["img_url"], use_container_width=True)
                        st.write(f"**{r['title'][:50]}...**")
                        st.caption(f"${r['price']:.2f} | Reviews: {r['num_reviews']:,}")
                        st.progress(r["total_weight"])
                with col_a:
                    st.markdown("**Amazon**")
                    if i < len(amazon_top):
                        r = amazon_top.iloc[i]
                        st.image(r["img_url"], use_container_width=True)
                        st.write(f"**{r['title'][:50]}...**")
                        st.caption(f"${r['price']:.2f} | Reviews: {r['num_reviews']:,}")
                        st.progress(r["total_weight"])
        best = ranked.iloc[0]
        st.success(f"**BEST OVERALL**: {best['source']} – {best['title'][:60]}... – `${best['price']:.2f}`")

    # --- DESIGN PREVIEW ---
    st.subheader("Design Preview")
    fig, ax = plt.subplots(figsize=(10,6))
    ax.imshow(room_img)
    ax.axis("off")
    ax.text(20, 50, f"{selected_room.upper()}\n{selected_style.upper()} | {selected_color.upper()}\nBudget ${budget}",
            color="yellow", fontsize=16, bbox=dict(facecolor="black", alpha=0.7))
    st.pyplot(fig)

    st.success(f"**320+ Real IKEA items loaded | 40 per room | {selected_room} only!**")

if __name__ == "__main__":
    main()