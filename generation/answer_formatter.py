import re

# ----------------------------
# GENERAL ANSWER
# ----------------------------

def format_answer(sentences, max_sentences=6):
    if not sentences:
        return None
    return " ".join(sentences[:max_sentences])


# ----------------------------
# DEFINITION
# ----------------------------

def format_definition(sentences):
    if not sentences:
        return None

    # First sentence is the definition
    definition = sentences[0]

    # Optional supporting sentence
    support = sentences[1] if len(sentences) > 1 else ""

    if support:
        return f"{definition} {support}"
    return definition


# ----------------------------
# EXPLANATION
# ----------------------------

def format_explanation(sentences, max_sentences=8):
    if not sentences:
        return None
    return " ".join(sentences[:max_sentences])


# ----------------------------
# ENTITY CLAUSE EXTRACTION
# ----------------------------

def extract_entity_clause(sentence, entity):
    entity = entity.lower()
    sentence_l = sentence.lower()

    if entity not in sentence_l:
        return None

    words = sentence.split()
    for i, w in enumerate(words):
        if entity in w.lower():
            start = max(0, i - 4)
            end = min(len(words), i + 8)
            return " ".join(words[start:end])

    return None


# ----------------------------
# COMPARISON
# ----------------------------

def format_comparison(sentences, entity1, entity2, max_points=5):
    entity1 = entity1.lower()
    entity2 = entity2.lower()

    e1_points = []
    e2_points = []

    for s in sentences:
        s_l = s.lower()

        if entity1 in s_l and len(e1_points) < max_points:
            e1_points.append(s)

        if entity2 in s_l and len(e2_points) < max_points:
            e2_points.append(s)

    if not e1_points and not e2_points:
        return None

    answer = "Comparison:\n\n"

    if e1_points:
        answer += f"{entity1.capitalize()}:\n"
        for p in e1_points:
            answer += "- " + p + "\n"

    if e2_points:
        answer += f"\n{entity2.capitalize()}:\n"
        for p in e2_points:
            answer += "- " + p + "\n"

    return answer.strip()


# ----------------------------
# QUALITY CHECK
# ----------------------------

def is_weak_answer(answer: str) -> bool:
    if not answer:
        return True

    text = answer.strip().lower()

    if "sorry" in text or "not found" in text:
        return True

    if len(text) < 50:
        return True

    return False
