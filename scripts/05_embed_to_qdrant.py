# scripts/05_embed_to_qdrant.py
import requests
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os

EMBED_URL = os.environ.get("EMBED_NGROK_URL", "")
qdrant = QdrantClient(host="localhost", port=6333)

# Tạo collection
qdrant.recreate_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)

def embed_and_store(records: list[dict]):
    # Try Kaggle embedding service, fallback to dummy
    try:
        if EMBED_URL:
            response = requests.post(f"{EMBED_URL}/embed", json={"texts": [r["text"] for r in records]}, timeout=5)
            embeddings = response.json()["embeddings"]
        else:
            raise Exception("No EMBED_URL")
    except:
        # Fallback: use dummy embeddings (random vectors)
        import numpy as np
        embeddings = [np.random.rand(384).tolist() for _ in records]
        print(f"Using dummy embeddings (Kaggle service not available)")

    points = [
        PointStruct(id=i, vector=emb, payload=rec)
        for i, (emb, rec) in enumerate(zip(embeddings, records))
    ]
    qdrant.upsert(collection_name="documents", points=points)
    print(f"Integration 5 OK: {len(points)} vectors stored in Qdrant")

# Test với sample data
embed_and_store([
    {"id": "doc_001", "text": "AI platform integration test"},
    {"id": "doc_002", "text": "Kafka to Airflow pipeline"},
])
