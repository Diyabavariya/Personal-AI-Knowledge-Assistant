import re

def clean_text(raw_text: str) -> str:
    """
    Generic text cleaner for TXT, PDF, DOC/DOCX extracted content.
    Does NOT assume any specific document type.
    """

    # 1. Normalize encoding artifacts
    text = raw_text.replace("\ufeff", " ").replace("\xa0", " ")

    # 2. Fix hyphenated line breaks (informa-\n tion -> information)
    text = re.sub(r"-\n\s*", "", text)

    # 3. Normalize newlines
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{2,}", "\n\n", text)

    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            cleaned_lines.append("")
            continue

        # Skip lines with no alphabetic characters (page numbers, symbols)
        if not re.search(r"[a-zA-Z]", line):
            continue

        cleaned_lines.append(line)

    # 4. Reconstruct text with sentence-aware line joining
    final_text = ""
    for line in cleaned_lines:
        if not final_text:
            final_text = line
            continue

        if final_text.endswith((".", "?", "!", ":")):
            final_text += "\n\n" + line
        else:
            final_text += " " + line

    # 5. Final whitespace cleanup
    final_text = re.sub(r"[ \t]+", " ", final_text)
    final_text = re.sub(r"\n{3,}", "\n\n", final_text)

    return final_text.strip()
