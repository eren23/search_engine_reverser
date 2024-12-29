from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import time
import random
import uvicorn
import logging
import json
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mock Search API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Add startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Mock Search Server starting up...")
    logger.info("CORS configuration enabled")
    logger.info("Endpoints available:")
    logger.info("  - GET /search")


@app.get("/")
async def root():
    """Root endpoint to test if server is running"""
    return {"status": "ok", "message": "Mock Search Server is running"}


# Load mock data
def load_mock_data():
    data_file = Path("mock_data.json")
    if not data_file.exists():
        logger.error("Mock data file not found. Please run data_generator.py first.")
        raise FileNotFoundError("mock_data.json not found")

    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)["books"]


# Update the DOCUMENTS constant
try:
    DOCUMENTS = load_mock_data()
except FileNotFoundError:
    logger.warning("Using fallback data - for better results, run data_generator.py")
    DOCUMENTS = [
        {"id": 1, "title": "Introduction to Python", "content": "Python is a great programming language"},
        {"id": 2, "title": "Python for Beginners", "content": "Learn Python programming basics"},
        {"id": 3, "title": "Advanced Python", "content": "Advanced concepts in Python programming"},
        {"id": 4, "title": "Web Development", "content": "Building web applications with Python"},
        {"id": 5, "title": "Data Science", "content": "Data analysis using Python libraries"},
    ]


def search_documents(query: str) -> List[Dict[str, Any]]:
    """Enhanced search implementation"""
    time.sleep(random.uniform(0.1, 0.3))

    query = query.lower()
    query = "".join(c for c in query if c.isalnum() or c.isspace())

    stop_words = {"the", "is", "at", "which", "on", "a", "an", "and", "or", "but"}
    terms = [term for term in query.split() if term not in stop_words]

    results = []
    for doc in DOCUMENTS:
        score = 0
        title = doc["title"].lower()
        content = doc["content"].lower()
        searchable_text = f"{title} {content}"

        # Exact title matching (highest priority)
        if query in title:
            score += 2.0

        # Exact content matching
        if query in content:
            score += 1.0

        # Term matching
        for term in terms:
            if term in title:
                score += 0.7
            if term in content:
                score += 0.3

        # Fuzzy matching for typos
        if any(term for term in terms if _fuzzy_match(term, searchable_text)):
            score += 0.3

        # Boost score based on popularity
        if score > 0 and "popularity" in doc:
            score += (doc["popularity"]["average_rating"] / 5.0) * 0.5

        if score > 0:
            results.append(
                {
                    "id": doc["id"],
                    "title": doc["title"],
                    "score": round(score, 2),
                    "matched": "fuzzy" if score < 1 else "exact",
                    "publication_date": doc.get("publication_date", ""),
                    "popularity": doc.get("popularity", {}),
                }
            )

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:20]  # Limit to top 20 results


def _fuzzy_match(term: str, content: str) -> bool:
    """Simple fuzzy matching"""
    return any(abs(len(word) - len(term)) <= 1 and sum(a != b for a, b in zip(term, word)) <= 1 for word in content.split())


@app.get("/search", response_model=List[Dict[str, Any]])
async def search(q: Optional[str] = Query(None, description="Search query")):
    """
    Search endpoint that supports:
    - Case-insensitive matching
    - Special character removal
    - Stop word filtering
    - Exact and fuzzy matching
    - Score-based ranking
    """
    logger.info(f"Received search query: {q}")
    if not q:
        return []

    results = search_documents(q)
    logger.info(f"Returning {len(results)} results")
    return results


if __name__ == "__main__":
    logger.info("Starting Mock Search Server...")
    uvicorn.run("mock_search_server:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
