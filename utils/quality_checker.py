import language_tool_python
import re
import textstat

tool = language_tool_python.LanguageTool('en-US')

WEAK_VERBS = ['helped', 'worked', 'assisted', 'participated', 'contributed', 'supported']

def grammar_check(text):
    matches = tool.check(text)
    results = []
    for match in matches:
        results.append({
            'message': match.message,
            'suggestions': match.replacements,
            'offset': match.offset,
            'error_text': text[match.offset:match.offset + match.errorLength]
        })
    return results

def check_grammar(text):
    matches = tool.check(text)
    grammar_errors = len(matches)
    suggestions = [match.message for match in matches]
    return grammar_errors, suggestions

def check_readability(text):
    flesch_score = textstat.flesch_reading_ease(text)
    grade_level = textstat.text_standard(text, float_output=False)
    return {"flesch_score": flesch_score, "grade_level": grade_level}

def check_passive_voice(text):
    passive_phrases = re.findall(r'\b(is|was|were|be|been|being|are|am)\b\s+\w+ed\b', text, re.IGNORECASE)
    return len(passive_phrases)

def detect_weak_action_verbs(text):
    found = []
    for verb in WEAK_VERBS:
        if re.search(r'\b' + re.escape(verb) + r'\b', text, re.IGNORECASE):
            found.append(verb)
    return found

def detect_quantified_achievements(text):
    matches = re.findall(r'\b\d+[%$]?\b', text)
    return bool(matches)

def check_formatting_consistency(text):
    issues = []
    lines = text.split("\n")
    for line in lines:
        if line.strip():
            if line.isupper():
                continue
            if re.match(r'^[a-z]', line):
                issues.append(f"Line doesn't start with a capital: '{line.strip()}'")
            if re.search(r'\s{2,}', line):
                issues.append(f"Inconsistent spacing in: '{line.strip()}'")
    return issues

def check_resume_length(text):
    word_count = len(text.split())
    if word_count < 300:
        return "⚠️ Resume is too short. Consider adding more content."
    elif word_count > 1000:
        return "⚠️ Resume is too long. Try to condense it to 1–2 pages."
    else:
        return "✅ Resume length looks good."
