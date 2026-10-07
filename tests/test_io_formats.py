from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from src.io.answers import format_block, write_answers
from src.io.questions import load_questions


class QuestionAndAnswerFormatTests(unittest.TestCase):
    def test_numbered_questions_keep_numbered_answers(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            questions = root / "questions.txt"
            answers = root / "answers.txt"
            questions.write_text("1. First question?\n2) Second question?\n", encoding="utf-8")

            document = load_questions(questions)
            blocks = [format_block(item.idx, "answer", document.fmt) for item in document.items]
            write_answers(answers, blocks, document.fmt)

            self.assertEqual(document.fmt, "numbered")
            self.assertEqual(answers.read_text(encoding="utf-8"), "1. answer\n2. answer\n")

    def test_markdown_questions_keep_markdown_answers(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            questions = root / "questions.txt"
            questions.write_text(
                "## Question 1\nFirst question?\n\n## Question 2\nSecond question?\n",
                encoding="utf-8",
            )

            document = load_questions(questions)

            self.assertEqual(document.fmt, "markdown")
            self.assertEqual(format_block(2, "answer", document.fmt), "## Answer 2\nanswer")


if __name__ == "__main__":
    unittest.main()
