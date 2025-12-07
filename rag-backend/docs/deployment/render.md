# Deploying RAG Backend to Render

This guide explains how to deploy your FastAPI-based RAG backend application to Render.

## Prerequisites

1.  A Render account (sign up at [https://render.com](https://render.com)).
2.  Your `rag-backend` code pushed to a Git repository (e.g., on GitHub, GitLab, or Bitbucket).
3.  A Render **Web Service** plan (free tier is often sufficient for basic testing).
4.  The following environment variables configured in your Render service (set via Render dashboard or `render.yaml`):
    *   `OPENAI_API_KEY`
    *   `QDRANT_CLOUD_URL`
    *   `QDRANT_API_KEY`
    *   `NEON_POSTGRES_URL`

## Steps

### 1. Prepare Your Repository

Ensure your `rag-backend` directory (or the root of your backend project) contains the following essential files:

*   `requirements.txt`: Lists all Python dependencies (e.g., `fastapi`, `uvicorn`, `qdrant-client`, `psycopg2-binary`, `openai`).
*   `main.py` (or your main application file): The entry point for your FastAPI app (e.g., located at `rag-backend/app/main.py`).
*   (Optional but recommended) `Procfile`: A text file in the root of your repository specifying how to start your application. For example:
    ```
    web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    ```
    If you don't have a `Procfile`, Render usually auto-detects a Python/`requirements.txt` project and defaults to `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`. Adjust the command if your main file is different (e.g., `app.main`).

### 2. Create a Web Service on Render

1.  Log in to your Render dashboard.
2.  Click the **New** button (or **+ New**).
3.  Select **Web Service**.
4.  Connect your Git repository provider (e.g., GitHub).
5.  Find and select your repository containing the `rag-backend`.
6.  Configure the build and deployment settings:
    *   **Environment**: Select `Python`.
    *   **Branch**: Select the branch you want to deploy (e.g., `main`).
    *   **Root Directory**: If your `rag-backend` is in a subdirectory of the repository root, specify the path (e.g., `rag-backend`). If it's at the root, leave it as `/`.
    *   **Build Command**: Leave empty or use the default (Render will run `pip install -r requirements.txt`).
    *   **Start Command**: If you have a `Procfile`, Render will use the command from there. Otherwise, enter the command explicitly, for example:
        ```bash
        uvicorn app.main:app --host 0.0.0.0 --port $PORT
        ```
        Ensure `app.main` points to your `main.py` file correctly based on your directory structure.
7.  **Environment Variables**: Click on **Advanced** or find the environment variables section. Add the following variables with their respective values:
    *   `OPENAI_API_KEY`: Your OpenAI API key.
    *   `QDRANT_CLOUD_URL`: Your Qdrant Cloud instance URL.
    *   `QDRANT_API_KEY`: Your Qdrant API key.
    *   `NEON_POSTGRES_URL`: Your Neon Postgres connection string.
8.  Click **Create Web Service**.

### 3. Monitor the Deployment

Render will automatically build and deploy your application. You can monitor the progress in the **Build & Logs** tab of your newly created service. The first build might take a few minutes as it installs dependencies.

### 4. Access Your Deployed API

Once the build is successful, Render will provide a public URL for your service (e.g., `https://your-service-name.onrender.com`). Your RAG backend API will be accessible at this URL.

### 5. Update Your Frontend (Docusaurus Chatbot)

After deployment, you need to update the `BACKEND_API_URL` constant in your Docusaurus chatbot component (`book-frontend/src/components/Chatbot.jsx`) to point to your Render URL (e.g., `https://your-service-name.onrender.com`).

## Troubleshooting

*   **Build fails**: Check the **Build & Logs** tab on Render. Common issues include missing dependencies in `requirements.txt` or incorrect file paths in the start command.
*   **App crashes after startup**: Check the **Logs** tab after deployment. Look for Python errors or issues connecting to external services (Qdrant, Neon, OpenAI) due to incorrect environment variables.
*   **Environment variables not found**: Ensure the variable names in Render exactly match those used in your Python code (case-sensitive) and that they are correctly set in the Render dashboard for the specific service.