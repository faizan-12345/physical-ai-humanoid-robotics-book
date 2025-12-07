import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from rag_backend.app.main import app # Assuming your main FastAPI app instance is here
from rag_backend.app.api.endpoints import QDRANT_COLLECTION_NAME

client = TestClient(app)

# Mock data for testing
MOCK_EMBEDDING = [0.1] * 1536 # Example OpenAI embedding size

@pytest.fixture
def mock_openai_embedding_response():
    """Mock response object for openai.embeddings.create"""
    mock_response = MagicMock()
    mock_data_item = MagicMock()
    mock_data_item.embedding = MOCK_EMBEDDING
    mock_response.data = [mock_data_item]
    return mock_response

@pytest.fixture
def mock_qdrant_client():
    """Mock Qdrant client"""
    mock_client = MagicMock()
    mock_operation_info = MagicMock()
    mock_operation_info.operation_id = 12345
    mock_client.upsert.return_value = mock_operation_info
    return mock_client

def test_embed_endpoint_success(mock_openai_embedding_response, mock_qdrant_client):
    """
    Test the /embed endpoint successfully processes a request and stores the embedding.
    This test mocks the external dependencies (OpenAI, Qdrant).
    """
    test_text = "This is a test sentence for embedding."
    test_metadata = {"source": "test_doc", "chapter": "1"}

    with patch('rag_backend.app.api.endpoints.openai_client') as mock_openai_client, \
         patch('rag_backend.app.api.endpoints.get_qdrant_client', return_value=mock_qdrant_client):

        # Configure the mock OpenAI client
        mock_openai_client.embeddings.create.return_value = mock_openai_embedding_response

        # Make the request
        response = client.post("/embed", json={"text": test_text, "metadata": test_metadata})

        # Assertions
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "Text embedded and stored."
        assert "operation_id" in response_data

        # Verify the mock methods were called as expected
        mock_openai_client.embeddings.create.assert_called_once_with(
            input=test_text,
            model="text-embedding-ada-002"
        )
        mock_qdrant_client.upsert.assert_called_once_with(
            collection_name=QDRANT_COLLECTION_NAME,
            points=[
                {
                    "vector": MOCK_EMBEDDING,
                    "payload": {"text": test_text, **test_metadata}
                }
            ]
        )

def test_embed_endpoint_failure():
    """
    Test the /embed endpoint handles failures gracefully (e.g., if OpenAI call fails).
    This test mocks the OpenAI client to raise an exception.
    """
    test_text = "This will cause an error."

    with patch('rag_backend.app.api.endpoints.openai_client') as mock_openai_client:
        # Configure the mock to raise an exception
        mock_openai_client.embeddings.create.side_effect = Exception("OpenAI API Error")

        # Make the request
        response = client.post("/embed", json={"text": test_text, "metadata": {}})

        # Assertions for failure case
        assert response.status_code == 500
        assert "detail" in response.json()
        assert "Embedding failed" in response.json()["detail"]

# Note: Similar tests can be written for /query and /selected-text-query endpoints,
# mocking the OpenAI chat completions and Qdrant search methods.
# For brevity, I'm adding a placeholder test structure for /query.

def test_query_endpoint_success():
    """
    Test the /query endpoint successfully processes a request and returns an answer.
    This test mocks the external dependencies (OpenAI, Qdrant).
    """
    test_query = "What are ROS 2 nodes?"

    # Mock OpenAI response for the final answer generation
    mock_openai_response = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "ROS 2 nodes are computational processes that perform specific tasks..."
    mock_openai_response.choices = [MagicMock(message=mock_message)]

    # Mock Qdrant search results
    mock_qdrant_result = MagicMock()
    mock_qdrant_result.payload = {"text": "A node is a fundamental unit of computation...", "source": "module1"}
    mock_qdrant_result.id = "qdrant_id_123"
    mock_qdrant_response = [mock_qdrant_result]

    with patch('rag_backend.app.api.endpoints.openai_client') as mock_openai_client, \
         patch('rag_backend.app.api.endpoints.get_qdrant_client') as mock_qdrant_client:

        # Configure the mocks
        mock_openai_client.embeddings.create.return_value = MagicMock(data=[MagicMock(embedding=MOCK_EMBEDDING)]) # Mock embedding generation for the query
        mock_openai_client.chat.completions.create.return_value = mock_openai_response
        mock_qdrant_client.search.return_value = mock_qdrant_response

        # Make the request
        response = client.post("/query", json={"query": test_query})

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "ROS 2 nodes are computational processes that perform specific tasks..."
        assert "sources" in data
        assert len(data["sources"]) == 1
        assert data["sources"][0]["text_snippet"] == "A node is a fundamental unit of computation..."
        assert data["sources"][0]["id"] == "qdrant_id_123"

        # Verify the mock methods were called as expected
        mock_openai_client.embeddings.create.assert_called_once_with(
            input=test_query,
            model="text-embedding-ada-002"
        )
        mock_qdrant_client.search.assert_called_once_with(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=MOCK_EMBEDDING,
            limit=5
        )
        # The prompt sent to OpenAI is harder to assert without more complex mocking of the f-string.
        # We can at least assert that the chat completion method was called.
        mock_openai_client.chat.completions.create.assert_called()


def test_query_endpoint_failure():
    """
    Test the /query endpoint handles failures gracefully (e.g., if Qdrant call fails).
    This test mocks the Qdrant client to raise an exception.
    """
    test_query = "This will cause an error."

    with patch('rag_backend.app.api.endpoints.openai_client') as mock_openai_client, \
         patch('rag_backend.app.api.endpoints.get_qdrant_client') as mock_qdrant_client:

        # Configure the mock OpenAI embedding to succeed, but Qdrant search to fail
        mock_openai_client.embeddings.create.return_value = MagicMock(data=[MagicMock(embedding=MOCK_EMBEDDING)])
        mock_qdrant_client.search.side_effect = Exception("Qdrant Search Error")

        # Make the request
        response = client.post("/query", json={"query": test_query})

        # Assertions for failure case
        assert response.status_code == 500
        assert "detail" in response.json()
        assert "Query failed" in response.json()["detail"]


def test_selected_text_query_endpoint_success():
    """
    Test the /selected-text-query endpoint successfully processes a request using only the provided text.
    This test mocks the external dependency (OpenAI).
    """
    test_query = "What is the main concept here?"
    test_selected_text = "Digital twins are virtual representations of physical objects or systems."

    # Mock OpenAI response for the answer generation based on selected text
    mock_openai_response = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "The main concept is digital twins, which are virtual representations..."
    mock_openai_response.choices = [MagicMock(message=mock_message)]

    with patch('rag_backend.app.api.endpoints.openai_client') as mock_openai_client:

        # Configure the mock
        mock_openai_client.chat.completions.create.return_value = mock_openai_response

        # Make the request
        response = client.post("/selected-text-query", json={"query": test_query, "selected_text": test_selected_text})

        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "The main concept is digital twins, which are virtual representations..."
        assert "sources" in data
        assert len(data["sources"]) == 1
        assert data["sources"][0]["text_snippet"] == test_selected_text

        # Verify the mock method was called as expected
        # We can assert that the chat completion method was called, and check part of the prompt content if needed.
        mock_openai_client.chat.completions.create.assert_called()


def test_selected_text_query_endpoint_failure():
    """
    Test the /selected-text-query endpoint handles failures gracefully (e.g., if OpenAI call fails).
    This test mocks the OpenAI client to raise an exception.
    """
    test_query = "This will cause an error."
    test_selected_text = "Some text..."

    with patch('rag_backend.app.api.endpoints.openai_client') as mock_openai_client:
        # Configure the mock to raise an exception
        mock_openai_client.chat.completions.create.side_effect = Exception("OpenAI Chat API Error")

        # Make the request
        response = client.post("/selected-text-query", json={"query": test_query, "selected_text": test_selected_text})

        # Assertions for failure case
        assert response.status_code == 500
        assert "detail" in response.json()
        assert "Selected text query failed" in response.json()["detail"]
