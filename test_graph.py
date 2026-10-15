import unittest
from src.graph import build_graph


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.graph = build_graph()

    def test_general_question_reaches_final_answer(self):
        result = self.graph.invoke({"question": "What is MMLU?"})
        self.assertEqual(result.get("route"), "general")
        self.assertTrue(result.get("final_answer"))

    def test_coding_question_uses_coding_route(self):
        result = self.graph.invoke({"question": "Write a Python function"})
        self.assertEqual(result.get("route"), "coding")
        self.assertTrue(result.get("final_answer"))

    def test_verification_note_is_present(self):
        result = self.graph.invoke({"question": "Explain photosynthesis"})
        self.assertIn("verification_note", result)


if __name__ == "__main__":
    unittest.main()
