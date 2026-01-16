def is_follow_up(text):
    follow_up_keywords = [
        "this",
        "that",
        "again",
        "continue",
        "previous",
        "earlier",
        "above"
    ]

    text = text.lower()

    for word in follow_up_keywords:
        if word in text:
            return True

    return False
