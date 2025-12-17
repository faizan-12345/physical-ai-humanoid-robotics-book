import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import re
from urllib.parse import urljoin, urlparse

def get_all_urls(base_url: str) -> List[str]:
    """
    Fetch all URLs from the sitemap
    """
    sitemap_url = urljoin(base_url, 'sitemap.xml')
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'xml')
        urls = []
        for loc in soup.find_all('loc'):
            url = loc.text.strip()
            if url.startswith(base_url):
                urls.append(url)

        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        # Fallback: try to get URLs from the main site
        try:
            response = requests.get(base_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            urls = []
            for link in links:
                href = link['href']
                full_url = urljoin(base_url, href)
                if full_url.startswith(base_url):
                    urls.append(full_url)

            return list(set(urls))  # Remove duplicates
        except Exception as e2:
            print(f"Error fetching URLs from main site: {e2}")
            return [base_url]

def extract_text_from_url(url: str) -> str:
    """
    Extract text content from a given URL
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text
    except Exception as e:
        print(f"Error extracting text from {url}: {e}")
        return ""

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks