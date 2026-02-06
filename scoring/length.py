def length_score(student, model_ans):
    ratio = len(student.split()) / max(len(model_ans.split()), 1)
    return min(ratio, 1.0)
