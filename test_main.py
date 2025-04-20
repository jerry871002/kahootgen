import asyncio
import unittest
from unittest.mock import MagicMock, mock_open, patch

import openpyxl

from main import generate_kahoot_quiz_xlsx, generate_prompt, main


class TestMainFunctions(unittest.TestCase):
    def test_generate_prompt(self):
        theme = "Science"
        num_questions = 5
        language = "en"
        prompt_template = "<THEME> <NUM_QUESTIONS> <LANGUAGE>"

        with patch("builtins.open", mock_open(read_data=prompt_template)):
            result = generate_prompt(theme, num_questions, language)

        expected = "Science 5 English"
        self.assertEqual(result, expected)

    def test_generate_kahoot_quiz_xlsx(self):
        questions = [
            {
                "question": "What is the capital of France?",
                "options": ["Paris", "London", "Berlin", "Madrid"],
                "answer": "Paris"
            }
        ]
        output_path = "test_output.xlsx"

        generate_kahoot_quiz_xlsx(questions, output_path)

        workbook = openpyxl.load_workbook(output_path)
        sheet = workbook["Sheet1"]

        self.assertEqual(sheet["B9"].value, "What is the capital of France?")
        self.assertEqual(sheet["C9"].value, "Paris")
        self.assertEqual(sheet["D9"].value, "London")
        self.assertEqual(sheet["E9"].value, "Berlin")
        self.assertEqual(sheet["F9"].value, "Madrid")
        self.assertEqual(sheet["H9"].value, 1)

    @patch("main.fetch_questions")
    @patch("main.generate_kahoot_quiz_xlsx")
    @patch("main.OpenAI")
    def test_main(self, mock_openai, mock_generate_xlsx, mock_fetch_questions):
        mock_fetch_questions.return_value = [
            {"question": "Sample question", "options": ["A", "B", "C", "D"], "answer": "A"}
        ]

        args = MagicMock()
        args.themes = ["Sample Theme"]
        args.num_questions = 1
        args.language = "en"
        args.output_path = "output.xlsx"

        with patch("main.load_dotenv"):
            asyncio.run(main(args))

        mock_fetch_questions.assert_called_once()
        mock_generate_xlsx.assert_called_once()

if __name__ == "__main__":
    unittest.main()
