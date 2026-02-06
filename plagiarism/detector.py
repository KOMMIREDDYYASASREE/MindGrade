from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def plagiarism_score(text1, text2):
    # Handle empty or very short text
    if not text1.strip() or not text2.strip():
        return 0.0

    try:
        vectorizer = CountVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform([text1, text2])
        score = cosine_similarity(vectors)[0][1]
        return round(score, 2)

    except ValueError:
        # Handles empty vocabulary case
        return 0.0
