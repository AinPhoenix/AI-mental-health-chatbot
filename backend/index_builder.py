import os
from utils.chunker import chunk_text
from utils.embedder import embed_texts
from utils.vector_store import save_index

RESOURCE_DIR = 'data/resources'
VECTOR_DIR = 'data'
os.makedirs(VECTOR_DIR, exist_ok=True)

def load_text_files(resource_dir):
    print(f"Loading files from {resource_dir}\n")
    text = {}
    for filename in os.listdir(resource_dir):
        if filename.endswith('.txt'):
            path = os.path.join(resource_dir, filename)
            with open(path, 'r', encoding='utf-8') as file:
                text[filename] = file.read()
    return text

def main():
    print("Starting knowledge base embedding...\n")

    texts = load_text_files(RESOURCE_DIR)
    if not texts:
        print("No text files found in the resource directory.")
        return
    
    all_chunks = []
    metadata = []

    for filename, content in texts.items():
        chunks = chunk_text(content, max_char=500)
        print(f"{filename}: {len(chunks)} chunks created")

        all_chunks.extend(chunks)
        metadata.extend([{"chunk": chunk, "filename": filename} for chunk in chunks])

    print("\nEmbedding chunks...")
    vectors = embed_texts(all_chunks)

    index_path = os.path.join(VECTOR_DIR, 'index.faiss')
    meta_path = os.path.join(VECTOR_DIR, 'metadata.json')

    save_index(vectors, metadata, index_path, meta_path)

    print(f"Index saved to {index_path}")
    print(f"Metadata saved to {meta_path}")
    print("Knowledge base embedding completed successfully.")

if __name__ == "__main__":
    main()
