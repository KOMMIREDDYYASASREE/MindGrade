from scoring.semantic import semantic_score
from scoring.keyword import keyword_score
from scoring.grammar import grammar_score
from scoring.length import length_score

def calculate_score(student, model_ans, max_marks):
    sem = semantic_score(student, model_ans)
    key = keyword_score(student, model_ans)
    gram, errors = grammar_score(student)
    length = length_score(student, model_ans)

    final = (
        sem * 0.5 +
        key * 0.2 +
        gram * 0.15 +
        length * 0.1
    )

    score = round(final * max_marks, 2)

    explanation = {
        "Semantic Similarity": round(sem, 2),
        "Keyword Match": round(key, 2),
        "Grammar Score": round(gram, 2),
        "Grammar Errors": errors,
        "Length Score": round(length, 2)
    }

    return min(score, max_marks), explanation
