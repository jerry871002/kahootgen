from dotenv import load_dotenv
from openai import OpenAI
from typing import Any
import openpyxl
import json
import argparse
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main(themes: list[str], num_questions: int) -> None:
    # load OPENAI_API_KEY from .env file
    load_dotenv()
    client = OpenAI()

    questions = []
    for theme in themes:
        prompt = generate_prompt(theme, num_questions)
        response = client.responses.create(model='gpt-4o', input=prompt)
        logger.info(f'Response for theme "{theme}": {response.output_text}')
        questions.extend(json.loads(response.output_text))

    random.shuffle(questions)

    generate_kahoot_quiz_xlsx(questions)

def generate_prompt(theme: str, num_questions: int) -> str:
    with open('prompt.txt', 'r') as file:
        prompt = file.read()

    prompt = prompt.replace('<THEME>', theme)
    prompt = prompt.replace('<NUM_QUESTIONS>', str(num_questions))

    return prompt

def generate_kahoot_quiz_xlsx(questions: list[dict[str, Any]]) -> None:
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

    output_path = 'KahootQuizOutput.xlsx'
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
    args = parser.parse_args()

    main(args.themes, args.num_questions)
