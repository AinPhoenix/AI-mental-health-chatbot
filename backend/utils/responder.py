import faiss
import json
from utils.vector_store import load_index
from utils.embedder import embed_texts
import requests

def retrieve_top_chunks(query: str, index_path: str, meta_path: str, top_k: int = 3) -> list[str]:
    index, metadata = load_index(index_path, meta_path)
    query_vector = embed_texts([query])[0].reshape(1, -1)

    D, I = index.search(query_vector, k=top_k)

    matched_chunks = [metadata[i]['chunk'] for i in I[0] if i >= 0]
    return matched_chunks

def generate_response(query: str, retrieved_chunks: list[str]) -> str:

    context = "\n\n".join(retrieved_chunks)
    prompt = f"""
You are a mental health assistant. Use the information below to answer the user's question in a supportive, helpful, and professional tone.

### User Question:
{query}

### Context (Mental Health Docs):
{context}

### Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt},
        stream=False
    )

    if response.status_code == 200:
        lines = response.text.splitlines()
        result = ""
        for line in lines:
            if line.strip().startswith('{'):
                try:
                    data = json.loads(line)
                    result += data.get("response", "")
                except:
                    continue
        return result.strip()
    else:
        return "❌ Failed to connect to Ollama."
    
def stream_response(query: str, retrieved_chunks: list[str]):
    import requests
    import json

    context = "\n\n".join(retrieved_chunks)
    prompt = f"""
You are a mental health assistant. Use the information below to answer the user's question in a supportive, helpful, and professional tone.

### User Question:
{query}

### Context (Mental Health Docs):
{context}

### Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": True},
        stream=True
    )

    for line in response.iter_lines():
        if line:
            try:
                chunk = json.loads(line.decode("utf-8"))
                yield chunk.get("response", "")
            except Exception:
                continue