def build_semantic_blocks(text):
    """
    Build complete semantic blocks from PDF/DOC text.
    A block = one complete thought ending with a period.
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    blocks = []
    buffer = ""

    for line in lines:
        # skip headings / junk
        if len(line.split()) < 4:
            continue
        if line.isupper():
            continue

        buffer = buffer + " " + line if buffer else line

        if buffer.endswith("."):
            blocks.append(buffer.strip())
            buffer = ""

    if buffer:
        blocks.append(buffer.strip())

    return blocks


def add_metadata(chunks, source_name):
    """
    Attaches metadata to each chunk.
    """
    chunk_objects = []

    for idx, chunk in enumerate(chunks):
        chunk_objects.append({
            "chunk_id": idx,
            "text": chunk,
            "source": source_name
        })

    return chunk_objects
