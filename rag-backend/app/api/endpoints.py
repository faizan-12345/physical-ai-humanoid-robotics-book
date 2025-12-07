import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from openai import OpenAI
from rag_backend.app.core.qdrant import get_qdrant_client, create_collection_if_not_exists
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

QDRANT_COLLECTION_NAME = "book_content_embeddings"

class EmbedRequest(BaseModel):
    text: str
    metadata: Dict[str, Any] = {}

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]

@router.on_event("startup")
async def startup_event():
    # Ensure Qdrant collection exists on startup
    client = get_qdrant_client()
    create_collection_if_not_exists(client, QDRANT_COLLECTION_NAME)

@router.post("/embed")
async def embed_text(request: EmbedRequest):
    try:
        # Generate embedding using OpenAI
        response = openai_client.embeddings.create(
            input=request.text,
            model="text-embedding-ada-002" # or other appropriate model
        )
        embedding = response.data[0].embedding

        # Store embedding in Qdrant
        qdrant_client = get_qdrant_client()
        operation_info = qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=[
                {
                    "vector": embedding,
                    "payload": {"text": request.text, **request.metadata}
                }
            ]
        )
        # Qdrant upsert returns a `UpdateResult` object, it does not directly return the ID of the inserted point
        # For simplicity, we can return a success status. If a specific ID is required, Qdrant allows to set custom IDs
        # when creating points, but it's not done in this simple example.

        return {"status": "success", "message": "Text embedded and stored.", "operation_id": str(operation_info.operation_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {e}")

class SelectedTextQueryRequest(BaseModel):
    query: str
    selected_text: str

@router.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    try:
        # 1. Generate embedding for the query
        query_response = openai_client.embeddings.create(
            input=request.query,
            model="text-embedding-ada-002"
        )
        query_embedding = query_response.data[0].embedding

        # 2. Search Qdrant for similar content
        qdrant_client = get_qdrant_client()
        search_results = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_embedding,
            limit=5 # Retrieve top 5 most similar results
        )

        # 3. Extract relevant text snippets and metadata
        context_snippets = []
        sources = []
        for result in search_results:
            text_snippet = result.payload.get("text", "")
            context_snippets.append(text_snippet)
            sources.append({
                "id": str(result.id),
                "text_snippet": text_snippet,
                "metadata": result.payload # Include all metadata from the payload
            })

        # 4. Combine context snippets
        combined_context = "\n\n".join(context_snippets)

        # 5. Use OpenAI to generate an answer based on the context and query
        prompt = f"""
        You are a helpful assistant for the Humanoid Robotics Book.
        Use the following retrieved context to answer the user's question.
        If the context does not contain the information needed to answer, say "I couldn't find the information in the book."

        Context:
        {combined_context}

        Question: {request.query}

        Answer:
        """

        openai_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo", # or gpt-4, depending on preference
            messages=[
                {"role": "system", "content": "You are a helpful assistant for the Humanoid Robotics Book. Use the provided context to answer the user's question."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500, # Adjust as needed
            temperature=0.7 # Adjust for creativity vs. factual accuracy
        )

        answer = openai_response.choices[0].message.content

        return QueryResponse(answer=answer, sources=sources)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")

@router.post("/selected-text-query")
async def query_selected_text(request: SelectedTextQueryRequest):
    try:
        # Use OpenAI to generate an answer based *only* on the provided selected_text and the query
        prompt = f"""
        You are a helpful assistant for the Humanoid Robotics Book.
        Use *only* the following provided text to answer the user's question.
        Do not use any other knowledge or information beyond what is in the provided text.
        If the provided text does not contain the information needed to answer, say "The selected text does not contain the information needed to answer the question."

        Provided Text:
        {request.selected_text}

        Question: {request.query}

        Answer:
        """

        openai_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo", # or gpt-4, depending on preference
            messages=[
                {"role": "system", "content": "You are a helpful assistant for the Humanoid Robotics Book. Answer the user's question using only the provided text snippet."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500, # Adjust as needed
            temperature=0.7 # Adjust for creativity vs. factual accuracy
        )

        answer = openai_response.choices[0].message.content

        # Return the answer and the source (the selected text itself)
        return {"answer": answer, "sources": [{"text_snippet": request.selected_text}]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Selected text query failed: {e}")

# Include this router in your main FastAPI app:
# from rag_backend.app.api.endpoints import router as api_router
# app.include_router(api_router)
