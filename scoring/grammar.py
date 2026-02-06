import language_tool_python

tool = language_tool_python.LanguageTool("en-US")

def grammar_score(text):
    errors = len(tool.check(text))
    score = max(0, 1 - errors * 0.02)
    return score, errors
