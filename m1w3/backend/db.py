import os

import psycopg2
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "semantic_search")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_conn():
    conn = psycopg2.connect(DB_URL)
    register_vector(conn)
    return conn


def init_db():
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
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
