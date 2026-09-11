import numpy as np
from rag.vector_store import VectorStore, ChunkRecord

def test_vector_search():
    store = VectorStore()
    embeddings = np.asarray([[1,0],[0,1]], dtype="float32")
    records = [
        ChunkRecord("python skill", "cv.pdf", "PDF", 0),
        ChunkRecord("biology degree", "edu.pdf", "PDF", 0),
    ]
    store.build(embeddings, records)
    result = store.search(np.asarray([[1,0]], dtype="float32"), top_k=1)
    assert len(result) == 1
    assert result[0]["source"] == "cv.pdf"
