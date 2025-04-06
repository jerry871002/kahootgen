import argparse
import json
import logging
import random
from typing import Any

import openpyxl  # type: ignore
from dotenv import load_dotenv
from openai import OpenAI  # type: ignore

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

language_mapping = {
    'en': 'English',
    'zh-tw': 'Traditional Chinese, using the translation convention in Taiwan'
}

def main(themes: list[str], num_questions: int, language: str, output_path: str) -> None:
    # load OPENAI_API_KEY from .env file
    load_dotenv()
    client = OpenAI()

    questions = []
    for theme in themes:
        prompt = generate_prompt(theme, num_questions, language)
        while True:
            response = client.responses.create(model='gpt-4o', input=prompt)
            logger.info(f'Response for theme "{theme}": {response.output_text}')
            try:
                questions.extend(json.loads(response.output_text))
                break
            except json.JSONDecodeError as e:
                # sometimes the reasponse contains markdown
                try:
                    # try to remove markdown and parse again
                    cleaned_response = response.output_text.replace('```json', '') \
                                                           .replace('```', '')
                    questions.extend(json.loads(cleaned_response))
                    break
                except json.JSONDecodeError:
                    logger.error(f"Failed to decode JSON: {e}")
                    logger.info("Retrying with the same prompt...")

    random.shuffle(questions)

    generate_kahoot_quiz_xlsx(questions, output_path)

def generate_prompt(theme: str, num_questions: int, language: str) -> str:
    with open('prompt.txt', 'r') as file:
        prompt = file.read()

    prompt = prompt.replace('<THEME>', theme)
    prompt = prompt.replace('<NUM_QUESTIONS>', str(num_questions))
    prompt = prompt.replace('<LANGUAGE>', language_mapping[language])

    return prompt

def generate_kahoot_quiz_xlsx(questions: list[dict[str, Any]], output_path: str) -> None:
    template_path = 'KahootQuizTemplate.xlsx'
    workbook = openpyxl.load_workbook(template_path)
    sheet = workbook['Sheet1']

    QUESTION_COLUMN = 'B'
    OPTIONS_COLUMNS = ('C', 'D', 'E', 'F')
    TIME_LIMIT_COLUMN = 'G'
    ANSWER_COLUMN = 'H'
    START_ROW = 9
    TIME_LIMIT = 10

    for i, question in enumerate(questions):
        row = START_ROW + i
        sheet[f'{QUESTION_COLUMN}{row}'] = question['question']
        for j, option in enumerate(question['options']):
            sheet[f'{OPTIONS_COLUMNS[j]}{row}'] = option
        sheet[f'{TIME_LIMIT_COLUMN}{row}'] = TIME_LIMIT
        # Set the answer column to the index of the correct answer
        # + 1 because Kahoot template uses 1-based indexing for answers
        sheet[f'{ANSWER_COLUMN}{row}'] = question['options'].index(question['answer']) + 1

    workbook.save(output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate themed quiz questions using LLM.")
    parser.add_argument(
        '--themes', '-t',
        nargs='+',
        required=True,
        help='List of themes for quiz questions (e.g., "Harry Potter" "Rocket Science")'
    )
    parser.add_argument(
        '--num_questions', '-n',
        type=int,
        default=5,
        help="Number of questions to generate for each theme"
    )
    parser.add_argument(
        '--language', '-l',
        type=str,
        default='en',
        choices=['en', 'zh-tw'],
        help="Language for the quiz questions (default: English)"
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='KahootQuizOutput.xlsx',
        help="Output file name for the generated quiz"
    )
    args = parser.parse_args()

    main(args.themes, args.num_questions, args.language, args.output)
