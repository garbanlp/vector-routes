from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer

from const  import LOCAL_OBSIDIAN_FILES, QDRANT_LOCAL_PATH, QDRANT_COLL_NAME
from parse_raw_data import get_obsidian_data, get_obsidian_keywords_notes

_EMB_DIM = 768


def _populate_qdrant_db():
    client = QdrantClient(path=QDRANT_LOCAL_PATH)  # Persist changes to disk
    client.recreate_collection(
        collection_name=QDRANT_COLL_NAME,
        vectors_config=VectorParams(size=_EMB_DIM, distance=Distance.COSINE),
    )
    model = SentenceTransformer('sentence-transformers/stsb-xlm-r-multilingual')
    assert model.get_sentence_embedding_dimension() == _EMB_DIM

    obsidian_data = get_obsidian_data(LOCAL_OBSIDIAN_FILES)
    keywords = get_obsidian_keywords_notes(obsidian_data)

    client.upsert(
        collection_name=QDRANT_COLL_NAME,
        points=[
            PointStruct(
                id=idx,
                vector=model.encode(kw).tolist(),
                payload={
                    'docs_id': docs_id,
                    'kw':kw,

                }
            )
            for idx, (kw, docs_id) in enumerate(keywords.items())
        ]
    )


if __name__ == '__main__':
    _populate_qdrant_db()

