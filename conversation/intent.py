def detect_intent(user_input: str):
    text = user_input.lower().strip()

    if text.startswith(("what is", "define", "meaning of")):
        return "DEFINE"

    if text.startswith(("explain", "describe", "how does", "how do")):
        return "EXPLAIN"

    if text.startswith(("summarize", "summary")):
        return "SUMMARIZE"

    if text.startswith(("compare", "difference between")):
        return "COMPARE"

    if text in ("continue", "explain again", "again"):
        return "FOLLOW_UP"

    return "GENERAL"

def extract_entities_for_comparison(user_input: str):
    """
    Extracts two entities from comparison-style queries.

    Examples:
    - 'compare paging and segmentation'
    - 'difference between tcp and udp'
    """

    text = user_input.lower().strip()

    # Case 1: "compare X and Y"
    if text.startswith("compare") and "and" in text:
        text = text.replace("compare", "").strip()
        parts = text.split("and")

        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()

    # Case 2: "difference between X and Y"
    if text.startswith("difference between") and "and" in text:
        text = text.replace("difference between", "").strip()
        parts = text.split("and")

        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()

    return None, None

