import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorSearch:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.documents = []

    def build_index(self, repo_path):

        texts = []
        CHUNK_SIZE = 600

        SKIP_DIR_KEYWORDS = [
            "tests",
            "test",
            "__pycache__",
            "venv",
            ".git",
            "node_modules",
            "dist",
            "build"
        ]

        for root, dirs, files in os.walk(repo_path):

            # Skip directories that contain unwanted keywords
            if any(skip in root.lower() for skip in SKIP_DIR_KEYWORDS):
                continue

            for file in files:

                if not file.endswith(".py"):
                    continue

                path = os.path.join(root, file)

                try:
                    with open(path, "r", errors="ignore") as f:

                        content = f.read()

                        for i in range(0, len(content), CHUNK_SIZE):

                            chunk = content[i:i + CHUNK_SIZE].strip()

                            if not chunk:
                                continue

                            # Skip import-heavy chunks
                            lines = chunk.split("\n")
                            import_lines = [l for l in lines if l.startswith("import") or l.startswith("from")]

                            if len(import_lines) > len(lines) * 0.5:
                                continue

                            texts.append({
                                "file": path,
                                "content": chunk
                            })

                except Exception:
                    pass

        self.documents = texts

        if not texts:
            return

        embeddings = self.model.encode(
            [doc["content"] for doc in texts],
            convert_to_numpy=True
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def search(self, question, k=10):

        if self.index is None:
            return []

        query_embedding = self.model.encode(
            [question],
            convert_to_numpy=True
        )

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for idx in indices[0]:

            if idx < len(self.documents):

                results.append({
                    "file": self.documents[idx]["file"],
                    "snippet": self.documents[idx]["content"][:800]
                })

        return results