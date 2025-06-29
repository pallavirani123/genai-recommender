import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

from sentence_transformers import SentenceTransformer
import numpy as np

# Load from local path
model_path = "C:/Users/palla/Desktop/huggingfacedownload/all-MiniLM-L6-v2"
model = SentenceTransformer(model_path)

def get_query_embedding(query: str) -> np.ndarray:
    return model.encode(query, convert_to_numpy=True)

# Cosine similarity function
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
