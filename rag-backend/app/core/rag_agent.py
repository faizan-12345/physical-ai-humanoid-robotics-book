import os
from typing import List, Dict, Any
from openai import OpenAI
from app.core.qdrant import get_qdrant_client, query_qdrant
from dotenv import load_dotenv

# Import the agents components
from openai_agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig

load_dotenv()

class RAGAgent:
    def __init__(self):
        # Initialize the external client with Gemini API
        gemini_api_key = os.getenv("GEMINI_API_KEY")

        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable must be set")

        self.external_client = AsyncOpenAI(
            api_key=gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        self.model = OpenAIChatCompletionsModel(
            openai_client=self.external_client,
            model="gemini-2.0-flash"
        )

        self.config = RunConfig(
            model=self.model,
            model_provider=self.external_client,
            tracing_disabled=True,
        )

        self.agent = Agent(
            name="RAG Assistant",
            instructions="You are a helpful assistant for the Humanoid Robotics Book. Use the provided context to answer the user's question. Be concise and accurate."
        )

        # Get Qdrant client for retrieval
        self.qdrant_client = get_qdrant_client()
        self.collection_name = "rag_embeddings"

    def query_with_rag(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Query the RAG system using the agent with Gemini and Qdrant retrieval
        """
        try:
            # 1. Retrieve relevant documents from Qdrant
            search_results = query_qdrant(self.qdrant_client, self.collection_name, query, top_k)

            # 2. Extract context from retrieved documents
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

            # 3. Combine context
            combined_context = "\n\n".join(context_snippets)

            # 4. Create prompt with context
            prompt = f"""
            You are a helpful assistant for the Humanoid Robotics Book.
            Use the following retrieved context to answer the user's question.
            If the context does not contain the information needed to answer, say "I couldn't find the information in the book."
            Be concise and accurate in your response.

            Context:
            {combined_context}

            Question: {query}

            Answer:
            """

            # 5. Run the agent with the prompt
            result = Runner.run_sync(
                self.agent,
                run_config=self.config,
                input=prompt
            )

            return {
                "answer": result.final_output,
                "sources": sources,
                "context_used": combined_context
            }

        except Exception as e:
            raise Exception(f"RAG query failed: {e}")