import unittest

from src.index.retriever import Plan, Retriever


class FakeCollection:
    def query(self, **_kwargs):
        return {
            "ids": [["a", "b", "c"]],
            "documents": [["first", "second", "third"]],
            "metadatas": [[
                {"section_number": "2", "section_top": "2", "kind": "body"},
                {"section_number": "2", "section_top": "2", "kind": "body"},
                {"section_number": "3", "section_top": "3", "kind": "caption"},
            ]],
            "distances": [[0.1, 0.2, 0.3]],
        }


class RetrieverTests(unittest.TestCase):
    def setUp(self):
        self.retriever = Retriever(FakeCollection(), {"2", "3"}, {"2", "3"})

    def test_invalid_scope_is_marked_unscoped(self):
        plan = self.retriever.validate_scope(Plan(section_scope=["Section 99"]))
        self.assertTrue(plan.unscoped)
        self.assertIsNone(plan.section_scope)

    def test_results_are_deduplicated_by_section_and_kind(self):
        plan = self.retriever.validate_scope(Plan(section_scope=["2"]))
        documents = self.retriever.retrieve([1.0, 0.0], plan)
        keys = [(doc.metadata["section_number"], doc.metadata["kind"]) for doc in documents]
        self.assertEqual(len(keys), len(set(keys)))


if __name__ == "__main__":
    unittest.main()
