from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_score(student, model_ans):
    emb1 = model.encode([student])
    emb2 = model.encode([model_ans])
    return cosine_similarity(emb1, emb2)[0][0]
