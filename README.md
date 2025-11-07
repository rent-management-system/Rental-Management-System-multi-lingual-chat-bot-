---
title: Multilingual Chatbot
emoji: 💻
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: '1.0'
app_file: app.main:app
pinned: true
short_description: a multilingual chatbot backend using FastAPI, LangGraph
---

# Multilingual Chatbot Backend

This project implements a multilingual chatbot backend using FastAPI, LangGraph, Google Gemini 2.0 Flash, and FAISS. It provides a REST API to answer user queries in English, Amharic, and Afaan Oromo, leveraging a knowledge base derived from various documents.

## Features

*   **Multilingual Support:** Auto-detects query language and responds in the same language (English, Amharic, Afaan Oromo).
*   **Knowledge Base:** Answers based on `translation.json`, `translation copy.json`, `translation copy 2.json`, `Faq.txt`, and `Final project 1-4 final.docx`.
*   **FastAPI:** High-performance web framework.
*   **LangGraph:** For building the RAG (Retrieval-Augmented Generation) pipeline.
*   **Google Gemini 2.0 Flash:** For powerful and multilingual text generation.
*   **FAISS:** Efficient similarity search for retrieving relevant information from the knowledge base.
*   **Render Free Tier Optimized:** Designed for deployment on Render's free tier with in-memory FAISS and minimal resource usage.
*   **Comprehensive Testing:** Includes unit tests with `pytest`.

## Tech Stack

*   **Backend:** Python 3.12.3
*   **Web Framework:** FastAPI
*   **RAG Framework:** LangGraph
*   **LLM:** Google Gemini 2.0 Flash
*   **Vector Store:** FAISS (in-memory, CPU)
*   **Embeddings:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
*   **Dependency Management:** `pip` with `requirements.txt`

## Setup and Local Development

### 1. Clone the Repository

```bash
git clone <repository_url>
cd rent-mag-chatBot
```

### 2. Create a Virtual Environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Google Gemini API Key

Obtain a Google Gemini API key from the [Google AI Studio](https://aistudio.google.com/app/apikey).

Create a `.env` file in the root directory of the project and add your API key:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 5. Run the Application Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. You can access the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

## API Endpoints

### `POST /chat`

Sends a query to the chatbot and receives a multilingual response.

*   **Request Body:**
    ```json
    {
        "query": "What property types can I list?",
        "language": "english"
    }
    ```
    *   `query` (string, required): The user's question.
    *   `language` (string, optional): Forces the response language. Valid values: `"english"`, `"amharic"`, `"afaan_oromo"`. If not provided, Gemini will auto-detect the language.

*   **Response:**
    ```json
    {
        "response": "You can list and search for various property types including apartments, houses, condos, commercial spaces, and land."
    }
    ```

### `GET /health`

Checks the health of the API.

*   **Response:**
    ```json
    {
        "status": "ok"
    }
    ```

## Sample Queries

You can test the chatbot with the following queries:

*   **English:**
    *   `"What is the Rental Management System?"`
    *   `"How do I register as a new user?"`
    *   `"What payment methods are accepted?"`
*   **Amharic:**
    *   `"የኪራይ አስተዳደር ስርዓት ምንድን ነው?"`
    *   `"አዲስ ተጠቃሚ እንዴት እመዘገባለሁ?"`
    *   `"ለኪራይ ምን ዓይነት የክፍያ ዘዴዎች ተቀባይነት አላቸው?"`
*      **Afaan Oromo:**
    *   `"Sirni Bulchiinsa Kiraayii maali?"`
    *   `"Akkanatti fayyadamaa haaraa ta'ee galmaa'a?"`
    *   `"Akka kireeffamuuf malawwan kaffaltii akkamii fudhatama qabu?"`

## Running Tests

```bash
pytest
```

## Deployment on Render (Free Tier)

1.  **Push to Git Repository:** Ensure your code is pushed to a GitHub, GitLab, or Bitbucket repository.
2.  **Create a New Web Service on Render:**
    *   Go to [Render Dashboard](https://dashboard.render.com/).
    *   Click "New Web Service".
    *   Connect your repository.
3.  **Configure Build and Deploy Settings:**
    *   **Root Directory:** `/` (or the directory containing `app/` and `requirements.txt`)
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1` (This will use the `Procfile` automatically if detected, but explicitly setting it is good practice).
    *   **Environment Variables:** Add `GOOGLE_API_KEY` with your actual Gemini API key.
    *   **Python Version:** Render will detect `runtime.txt` and use `python-3.12.3`.
4.  **Deploy:** Click "Create Web Service".

Render will automatically build and deploy your application. The in-memory FAISS index will be rebuilt on each startup, which is fast enough for the free tier's cold starts.

## Important Notes for Render Free Tier

*   **Cold Starts:** The application might experience cold starts (a few seconds delay) due to the free tier's resource limitations and the need to rebuild the FAISS index.
*   **No Persistence:** The FAISS index is in-memory, meaning it will be lost if the service restarts. This is acceptable for the free tier as it rebuilds quickly.
*   **Resource Limits:** The free tier has 512MB RAM. The chosen embedding model and in-memory FAISS are designed to fit within this limit for the given knowledge base size.




