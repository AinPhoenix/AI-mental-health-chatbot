from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_texts(text):
    return model.encode(text, convert_to_tensor=False)