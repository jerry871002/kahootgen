import asyncio
import json
import time
import unittest
from unittest.mock import MagicMock, mock_open, patch

import openpyxl

from kahootgen.main import fetch_questions, generate_kahoot_quiz_xlsx, generate_prompt, main


class TestKahootGen(unittest.TestCase):

    def create_mock_response(self, *args, **kwargs):
        """Mock function that sleeps for 2 seconds and returns a response"""
        # Simulate API delay
        time.sleep(2)

        mock_response = MagicMock()
        mock_response.output_text = json.dumps([
            {
                "question": "Test question 1?",
                "options": ["Test option 1", "Test option 2", "Test option 3", "Test option 4"],
                "answer": "Test answer 1"
            },
            {
                "question": "Test question 2?",
                "options": ["Test option 1", "Test option 2", "Test option 3", "Test option 4"],
                "answer": "Test answer 2"
            }
        ])

        return mock_response

    @patch('kahootgen.main.generate_prompt')
    @patch("kahootgen.main.OpenAI")
    def test_fetch_questions(self, mock_openai, mock_generate_prompt):
        mock_generate_prompt.return_value = "Test prompt"
        client = mock_openai.return_value
        client.responses.create = self.create_mock_response

        themes = [f'Theme {i}' for i in range(5)]
        num_questions = 2
        language = "en"

        async def run_test():
            tasks = [
                fetch_questions(client, theme, num_questions, language) for theme in themes
            ]
            results = await asyncio.gather(*tasks)
            self.assertEqual(len(results), len(themes))

        # Measure the time taken for the test
        start_time = time.time()
        asyncio.run(run_test())
        end_time = time.time()
        duration = end_time - start_time

        # The API calls should run concurrently
        self.assertAlmostEqual(duration, 2, delta=1)

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

    @patch("kahootgen.main.fetch_questions")
    @patch("kahootgen.main.generate_kahoot_quiz_xlsx")
    @patch("kahootgen.main.OpenAI")
    def test_main(self, mock_openai, mock_generate_xlsx, mock_fetch_questions):
        mock_fetch_questions.return_value = [
            {"question": "Sample question", "options": ["A", "B", "C", "D"], "answer": "A"}
        ]

        args = MagicMock()
        args.themes = ["Sample Theme"]
        args.num_questions = 1
        args.language = "en"
        args.output_path = "output.xlsx"

        with patch("kahootgen.main.load_dotenv"):
            asyncio.run(main(args))

        mock_fetch_questions.assert_called_once()
        mock_generate_xlsx.assert_called_once()
