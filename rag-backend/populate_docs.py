import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.qdrant import get_qdrant_client, ensure_collection_exists, save_chunk_to_qdrant
from app.core.document_processor import get_all_urls, extract_text_from_url, chunk_text

async def populate_qdrant_with_docs():
    """
    Fetch all URLs from the Vercel site, extract text, chunk it, and save to Qdrant
    """
    print("Starting to populate Qdrant with documentation...")

    # Get Qdrant client
    client = get_qdrant_client()

    # Ensure collection exists
    collection_name = "rag_embeddings"
    ensure_collection_exists(client, collection_name)

    # Get all URLs from the Vercel site
    base_url = "https://physical-ai-humanoid-robotics-book-nu.vercel.app"
    urls = get_all_urls(base_url)

    print(f"Found {len(urls)} URLs to process")

    chunk_id_counter = 0

    for i, url in enumerate(urls):
        print(f"Processing URL {i+1}/{len(urls)}: {url}")

        # Extract text from the URL
        text = extract_text_from_url(url)

        if not text.strip():
            print(f"No text found at {url}, skipping...")
            continue

        # Chunk the text
        chunks = chunk_text(text, chunk_size=1000, overlap=100)

        print(f"Found {len(chunks)} chunks for {url}")

        # Save each chunk to Qdrant
        for j, chunk in enumerate(chunks):
            chunk_id = f"{url.replace('https://', '').replace('/', '_')}_{j}"
            chunk_id = chunk_id.replace('.', '_').replace(':', '_')
            chunk_id = f"chunk_{chunk_id_counter}"
            chunk_id_counter += 1

            try:
                save_chunk_to_qdrant(client, collection_name, chunk, url, chunk_id)
                print(f"Saved chunk {j+1}/{len(chunks)} for {url}")
            except Exception as e:
                print(f"Error saving chunk for {url}: {e}")

    print("Finished populating Qdrant with documentation!")

if __name__ == "__main__":
    asyncio.run(populate_qdrant_with_docs())