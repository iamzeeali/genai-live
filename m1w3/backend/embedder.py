from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dims, fast, free


def embed(texts: list[str]) -> list[list[float]]:
    return model.encode(texts, batch_size=32).tolist()
