import faiss
import numpy as np
import json

def save_index(vectors, metadata, index_path, meta_path):
    dim = vectors[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(vectors).astype('float32'))
    faiss.write_index(index, index_path)

    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

def load_index(index_path, meta_path):
    index = faiss.read_index(index_path)
    with open(meta_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    return index, metadata
