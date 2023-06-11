from time import monotonic

from fastapi import FastAPI
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from const import QDRANT_COLL_NAME, LOCAL_OBSIDIAN_FILES, QDRANT_LOCAL_PATH
from parse_raw_data import get_obsidian_data, get_obsidian_keywords_notes


obsidian_data = get_obsidian_data(LOCAL_OBSIDIAN_FILES)
keywords = get_obsidian_keywords_notes(obsidian_data)

model = SentenceTransformer('sentence-transformers/stsb-xlm-r-multilingual')
client = QdrantClient(path=QDRANT_LOCAL_PATH)

app = FastAPI()


def search_in_qdrant(text: str, model: SentenceTransformer, client: QdrantClient) -> list[int]:
    tic = monotonic()

    response_search = client.search(
        collection_name=QDRANT_COLL_NAME,
        query_vector=model.encode(text),
        limit=3,
    )
    print(f"query took {monotonic() - tic:.2f}")

    docs_similar = [doc_id for row in response_search for doc_id in row.payload['docs_id']]
    return list(dict.fromkeys(docs_similar))


@app.get("/")
def root():
    return {"message": f"Hello World {QDRANT_COLL_NAME}"}


@app.post("/semantic-search")
def semantic_search(query: str):
    docs_idx = search_in_qdrant(query, model, client)
    return [data for i, data in enumerate(obsidian_data) if i in docs_idx]



