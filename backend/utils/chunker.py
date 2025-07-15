def chunk_text(text: str, max_char: int = 500) -> list[str]:
    chunks = []
    buffer = ""

    for line in text.splitlines():
        if len(buffer) + len(line) + 1 > max_char:
            chunks.append(buffer.strip())
            buffer = line
        else:
            buffer += "\n" + line

    if buffer:
        chunks.append(buffer.strip())
    return chunks