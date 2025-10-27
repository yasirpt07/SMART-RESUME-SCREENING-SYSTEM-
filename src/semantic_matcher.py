from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    return model.encode([text])

def semantic_match(resume_text, job_desc):
    resume_vec = embed_text(resume_text)
    job_vec = embed_text(job_desc)
    similarity = cosine_similarity(resume_vec, job_vec)[0][0]
    return round(similarity * 100, 2)
