# Quickstart Guide: Physical AI & Humanoid Robotics Technical Book

This guide will help you set up and run the project components locally.

## 1. Project Structure

The project is organized into two main parts:

*   `book-frontend/`: Contains the Docusaurus project for the technical book.
*   `rag-backend/`: Contains the FastAPI application for the RAG chatbot API.

## 2. Setting up the Book Frontend (Docusaurus)

To set up and run the Docusaurus book:

1.  **Navigate to the frontend directory:**
    ```bash
    cd book-frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Start the development server:**
    ```bash
    npm start
    ```
    The book will be accessible at `http://localhost:3000`.

## 3. Setting up the RAG Backend (FastAPI)

To set up and run the FastAPI RAG server:

1.  **Navigate to the backend directory:**
    ```bash
    cd rag-backend
    ```
2.  **Create a Python virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
    *(You will need to create a `requirements.txt` file with FastAPI, uvicorn, qdrant-client, psycopg2-binary, openai, etc. listed.)*

3.  **Configure Environment Variables:**
    Create a `.env` file in the `rag-backend/` directory with the following (replace with your actual credentials):
    ```
    OPENAI_API_KEY="your_openai_api_key"
    QDRANT_CLOUD_URL="your_qdrant_cloud_url"
    QDRANT_API_KEY="your_qdrant_api_key"
    NEON_POSTGRES_URL="your_neon_postgres_connection_string"
    ```

4.  **Run the FastAPI application:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The RAG API will be accessible at `http://localhost:8000`.

## 4. Integrating the Chatbot into Docusaurus

(Instructions for embedding the chatbot UI component into Docusaurus and configuring it to connect to the `rag-backend` will be provided in a later phase.)

## 5. Deployment

*   **Docusaurus to GitHub Pages**: Instructions will be provided.
*   **RAG Backend to Render**: Instructions will be provided.
