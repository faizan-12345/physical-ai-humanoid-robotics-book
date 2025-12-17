import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from openai import OpenAI
import cohere
from app.core.qdrant import get_qdrant_client, ensure_collection_exists, query_qdrant
from app.core.rag_agent import RAGAgent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

# Initialize OpenAI client for chat completion (we'll use Cohere for embeddings)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

QDRANT_COLLECTION_NAME = "rag_embeddings"

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
    ensure_collection_exists(client, QDRANT_COLLECTION_NAME)

@router.post("/embed")
async def embed_text(request: EmbedRequest):
    try:
        # This endpoint is now mainly for compatibility, as we'll populate via the script
        # Generate embedding using Cohere
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            raise HTTPException(status_code=500, detail="COHERE_API_KEY not set in environment")

        co = cohere.Client(cohere_api_key)
        response = co.embed(
            texts=[request.text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        embedding = response.embeddings[0]

        # Store embedding in Qdrant with metadata
        qdrant_client = get_qdrant_client()
        import uuid
        point_id = str(uuid.uuid4())

        qdrant_client.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=[
                {
                    "id": point_id,
                    "vector": embedding,
                    "payload": {"text": request.text, "url": request.metadata.get("url", ""), **request.metadata}
                }
            ]
        )

        return {"status": "success", "message": "Text embedded and stored.", "id": point_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {e}")

class SelectedTextQueryRequest(BaseModel):
    query: str
    selected_text: str

@router.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    try:
        # 1. Search Qdrant for similar content using Cohere embeddings
        qdrant_client = get_qdrant_client()
        search_results = query_qdrant(qdrant_client, QDRANT_COLLECTION_NAME, request.query, top_k=5)

        # 2. Extract relevant text snippets and metadata
        context_snippets = []
        sources = []
        for result in search_results:
            text_snippet = result.payload.get("text", "")
            context_snippets.append(text_snippet)
            sources.append({
                "id": str(result.id),
                "text_snippet": text_snippet,
                "url": result.payload.get("url", ""),
                "metadata": {k: v for k, v in result.payload.items() if k not in ['text', 'url']}
            })

        # 3. Combine context snippets
        combined_context = "\n\n".join(context_snippets)

        # 4. Use OpenAI to generate an answer based on the context and query
        prompt = f"""
        You are a helpful assistant for the Humanoid Robotics Book.
        Use the following retrieved context to answer the user's question.
        If the context does not contain the information needed to answer, say "I couldn't find the information in the book."
        Be concise and accurate in your response.

        Context:
        {combined_context}

        Question: {request.query}

        Answer:
        """

        openai_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo", # or gpt-4, depending on preference
            messages=[
                {"role": "system", "content": "You are a helpful assistant for the Humanoid Robotics Book. Use the provided context to answer the user's question. Be concise and accurate."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500, # Adjust as needed
            temperature=0.3 # Lower temperature for more factual responses
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
            temperature=0.3 # Lower temperature for more factual responses
        )

        answer = openai_response.choices[0].message.content

        # Return the answer and the source (the selected text itself)
        return {"answer": answer, "sources": [{"text_snippet": request.selected_text}]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Selected text query failed: {e}")

# New endpoint using the RAG Agent with Gemini
@router.post("/agent-query", response_model=QueryResponse)
async def query_rag_agent(request: QueryRequest):
    try:
        # Initialize the RAG Agent
        rag_agent = RAGAgent()

        # Query using the agent with Gemini and Qdrant retrieval
        result = rag_agent.query_with_rag(request.query, top_k=5)

        return QueryResponse(answer=result["answer"], sources=result["sources"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG Agent query failed: {e}")
