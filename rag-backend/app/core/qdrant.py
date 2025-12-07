import os
from qdrant_client import QdrantClient, models

def get_qdrant_client():
    qdrant_url = os.getenv("QDRANT_CLOUD_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_CLOUD_URL and QDRANT_API_KEY must be set in environment variables")

    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
    )
    return client

# Example usage (will be called by other modules)
def create_collection_if_not_exists(client: QdrantClient, collection_name: str):
    try:
        client.get_collection(collection_name=collection_name)
        print(f"Collection '{collection_name}' already exists.")
    except Exception:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE), # Assuming OpenAI embeddings size
        )
        print(f"Collection '{collection_name}' created.")
