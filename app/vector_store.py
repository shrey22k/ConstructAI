import chromadb
from chromadb.utils import embedding_functions

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./data/chromadb")
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