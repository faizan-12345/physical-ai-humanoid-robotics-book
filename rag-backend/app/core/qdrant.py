from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from typing import List, Optional
import cohere

def get_qdrant_client():
    """Get Qdrant client instance"""
    qdrant_url = os.getenv("QDRANT_CLOUD_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url or not qdrant_api_key:
        raise ValueError("QDRANT_CLOUD_URL and QDRANT_API_KEY environment variables must be set")

    client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=True
    )
    return client

def ensure_collection_exists(client: QdrantClient, collection_name: str, vector_size: int = 1024):
    """Ensure the collection exists, create if it doesn't"""
    try:
        client.get_collection(collection_name=collection_name)
        print(f"Collection '{collection_name}' already exists")
    except:
        print(f"Creating collection '{collection_name}'")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE
            )
        )
        print(f"Collection '{collection_name}' created successfully")

def embed_text(text: str) -> List[float]:
    """Generate embeddings for text using Cohere"""
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable must be set")

    co = cohere.Client(cohere_api_key)
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    return response.embeddings[0]

def save_chunk_to_qdrant(client: QdrantClient, collection_name: str, text: str, url: str, chunk_id: str):
    """Save a text chunk to Qdrant with metadata"""
    embedding = embed_text(text)

    client.upsert(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=hash(chunk_id) % (10**18),  # Convert to a valid integer ID
                vector=embedding,
                payload={
                    "text": text,
                    "url": url,
                    "chunk_id": chunk_id
                }
            )
        ]
    )

def query_qdrant(client: QdrantClient, collection_name: str, query_text: str, top_k: int = 5):
    """Query Qdrant for similar text chunks"""
    query_embedding = embed_text(query_text)

    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k,
        with_payload=True
    )

    return search_result
