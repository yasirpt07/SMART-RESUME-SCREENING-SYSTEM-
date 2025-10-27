from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load Pre-Trained Bert Model
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    return model.encode([text])

def semantic_match(resume_text,job_Desc):
    resume_vec = embed_text(resume_text)
    job_vec = embed_text(job_Desc)

    similarity = cosine_similarity(resume_vec,job_vec)[0][0]
    score = round(similarity*100,2)
    return score
