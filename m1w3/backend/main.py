from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db import get_conn
from embedder import embed

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@app.post("/search")
def search(req: SearchRequest):
    embedding = embed([req.query])[0]

    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT title, summary, 1 - (embedding <=> %s::vector) AS score
                FROM movies
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, (embedding, embedding, req.top_k))
            rows = cur.fetchall()
    conn.close()

    return [
        {"title": row[0], "summary": row[1], "score": round(row[2], 4)}
        for row in rows
    ]

# return [
#     {"title": row[0], "summary": row[1], "score": round(row[2], 4)}
#     for row in rows
#     if row[2] >= 0.3  # only return meaningful matches
# ]
