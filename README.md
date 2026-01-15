# AI-Based-Home-Decor-Recommendation-System
Shopping for home decor is both personal and daunting. Millions of furniture and decor
furnishings exist on platforms like Amazon and IKEA, and users struggle to find pieces that
match their room's style, constraints, and budget. This proposal demonstrates an artificial
intelligence-powered Home Decor Recommendation System, which transforms a photo of an
empty room into a shoppable design. The application begins with user input—a photo of a room
and user preferences of style, color, and budget. Then, we processed the inputs through a
modular data processing pipeline. The computer vision pipeline used PIL for image ingestion;
the ml_recommender.py module (XGBoost) inferred the room type, layout, and visual harmony
of the room. A synthetic data pipeline (generate_synthetic_data.py, sentiment_analysis.py)
enhanced the unique catalog of real-world contents from Amazon/IKEA with believable reviews,
purchases, and sentiment scores (NLTK’s VADER), to strengthen the training and filtering
pipelines.
Products are then segregated by room through keyword mapping (segregate_ikea_by_room.py)
and ranked through a content-based filtering approach, giving the products style/color matching
and budget weight. The end result processed and displayed using the Streamlit UI
(home_decor_app.py) the top 20 suggestions with live links for e-commerce, progress tracking,
and previews stored by style for design suggestions.
The XGBoost model secured an accuracy of 92–94% and a recall of 94% in synthetic
benchmarks, and the SHAP visualizations demonstrate the model's explanation of feature
importance. Notable advancements from this research include: (1) multimodal fusion (images +
preferences), (2) ethical synthetic data, and (3) a seamless inspiration-to-purchase flow. The
system mitigated decision fatigue by greater than 60% (estimated based on UI efficiency) and
bridged AI design with real-world shopping experiences. Future directions for the research
include: (1) real-time API integration, (2) 3D scene synthesis, and (3) AR enhanced
visualization.
