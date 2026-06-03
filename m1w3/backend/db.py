import os

import psycopg2
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector

load_dotenv()

DB_URL = (
    os.getenv("DATABASE_URL")
    or os.getenv("POSTGRES_URL")
    or "postgresql://admin:password@localhost:5432/semantic_search"
)


def get_conn():
    conn = psycopg2.connect(DB_URL)
    register_vector(conn)
    return conn


def init_db():
    conn = psycopg2.connect(DB_URL)
    with conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    conn.close()
    # reconnect so register_vector finds the type
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS movies (
                    id          SERIAL PRIMARY KEY,
                    title       TEXT NOT NULL,
                    summary     TEXT NOT NULL,
                    embedding   vector(384)
                );
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS movies_embedding_idx
                ON movies
                USING hnsw (embedding vector_cosine_ops);
            """)
    conn.close()
    print("DB initialised.")


if __name__ == "__main__":
    init_db()
