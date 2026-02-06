from sklearn.feature_extraction.text import TfidfVectorizer

def keyword_score(student, model_ans):
    # Handle empty or very short text
    if not student.strip() or not model_ans.strip():
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf = vectorizer.fit_transform([model_ans, student])

        # SAFE cosine similarity computation
        sim_matrix = (tfidf @ tfidf.T).toarray()
        score = sim_matrix[0][1]

        return min(float(score), 1.0)

    except ValueError:
        # Handles empty vocabulary case
        return 0.0
