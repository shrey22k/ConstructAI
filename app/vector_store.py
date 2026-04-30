import chromadb
import os
from chromadb.utils import embedding_functions

class VectorStore:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'chromadb')
        os.makedirs(db_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=db_path)
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="construction_reports",
            embedding_function=self.ef
        )

    def add_document(self, doc_id: str, content: str, metadata: dict = {}):
        self.collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def search_similar(self, query: str, n_results: int = 3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results["documents"][0] if results["documents"] else []
#ChromaDB vector Memory Integrated
