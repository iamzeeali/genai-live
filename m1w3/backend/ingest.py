from db import get_conn, init_db
from embedder import embed

documents = [
    {"title": "The Matrix",
        "content": "A hacker discovers reality is a simulation controlled by machines."},
    {"title": "Inception",
        "content": "A thief enters people's dreams to plant ideas in their minds."},
    {"title": "Interstellar",
        "content": "Astronauts travel through a wormhole to find a new home for humanity."},
    {"title": "The Dark Knight",
        "content": "Batman faces the Joker, a criminal mastermind who wants to plunge Gotham into anarchy."},
    {"title": "Parasite", "content": "A poor family schemes to become employed by a wealthy household, with unexpected consequences."},
    {"title": "Spirited Away",
        "content": "A young girl enters a spirit world and must work to free herself and her parents."},
    {"title": "The Godfather",
        "content": "The aging patriarch of a crime dynasty transfers control to his reluctant son."},
    {"title": "Amélie", "content": "A shy Parisian waitress decides to help those around her find happiness while neglecting her own."},
    {"title": "Gladiator", "content": "A Roman general is betrayed and enslaved, then rises as a gladiator to seek revenge."},
    {"title": "The Shawshank Redemption",
        "content": "A banker is wrongfully imprisoned and forms a deep friendship while planning his escape."},
    {"title": "Eternal Sunshine of the Spotless Mind",
        "content": "A couple undergoes a procedure to erase each other from their memories after a painful breakup."},
    {"title": "Mad Max: Fury Road",
        "content": "In a post-apocalyptic wasteland, a woman rebels against a tyrant to free enslaved women."},
    {"title": "Her", "content": "A lonely writer develops a romantic relationship with an AI operating system."},
    {"title": "The Truman Show",
        "content": "A man slowly discovers his entire life is a reality TV show broadcast to the world."},
    {"title": "Schindler's List",
        "content": "A German businessman saves over a thousand Jewish refugees during the Holocaust."},
    {"title": "Pulp Fiction", "content": "Multiple interconnected crime stories unfold in Los Angeles involving hitmen, a boxer, and gangsters."},
    {"title": "WALL-E", "content": "A lonely robot on a deserted Earth falls in love and helps save humanity from ecological collapse."},
    {"title": "The Social Network",
        "content": "The founding of Facebook leads to lawsuits and the betrayal of friendships."},
    {"title": "Gravity", "content": "Two astronauts struggle to survive after debris destroys their shuttle in outer space."},
    {"title": "Whiplash", "content": "A young drummer is pushed to his limits by a ruthless music conservatory instructor."},
]


def ingest():
    init_db()

    contents = [doc["content"] for doc in documents]
    embeddings = embed(contents)  # batched — one call for all docs

    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            for doc, embedding in zip(documents, embeddings):
                cur.execute(
                    "INSERT INTO movies (title, summary, embedding) VALUES (%s, %s, %s)",
                    (doc["title"], doc["content"], embedding)
                )
    conn.close()
    print(f"Ingested {len(documents)} documents.")


if __name__ == "__main__":
    ingest()
