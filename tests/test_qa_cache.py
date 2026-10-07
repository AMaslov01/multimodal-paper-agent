from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.cache.qa_cache import QACache, lookup_with_embedding


class FakeEmbeddings:
    def __init__(self, vector):
        self.vector = vector
        self.calls = 0

    def embed_query(self, _question):
        self.calls += 1
        return list(self.vector)


class QACacheLookupTests(unittest.TestCase):
    def test_cache_miss_returns_embedding_for_retrieval_and_save(self):
        with TemporaryDirectory() as tmp:
            cache = QACache(Path(tmp))
            embeddings = FakeEmbeddings([1.0, 0.0])

            entry, vector = lookup_with_embedding(cache, "What is SPSA?", embeddings)

            self.assertIsNone(entry)
            self.assertEqual(vector, [1.0, 0.0])
            self.assertEqual(embeddings.calls, 1)

            cache.save("What is SPSA?", "A gradient estimator.", vector, ["c1"], {})
            saved = cache._entries[-1]
            self.assertEqual(saved.question_embedding, vector)

    def test_exact_hit_returns_entry_and_current_embedding(self):
        with TemporaryDirectory() as tmp:
            cache = QACache(Path(tmp))
            cache.save("What is SPSA?", "A gradient estimator.", [1.0, 0.0], ["c1"], {})
            embeddings = FakeEmbeddings([0.9, 0.1])

            entry, vector = lookup_with_embedding(cache, "What is SPSA?", embeddings)

            self.assertIsNotNone(entry)
            self.assertEqual(entry.answer, "A gradient estimator.")
            self.assertEqual(vector, [0.9, 0.1])
            self.assertEqual(embeddings.calls, 1)


if __name__ == "__main__":
    unittest.main()
