# KahootGen

Want to create engaging quizzes effortlessly?
KahootGen is a Python-based tool that uses OpenAI's GPT model to generate multiple-choice quiz questions.
With a single command, KahootGen allows you to create engaging quizzes for various themes and formats the questions into a Kahoot-compatible Excel file, making it easy to import and use in Kahoot.

## Features

- **Effortless Quiz Creation**: Generate high-quality quiz questions with just one command.
- **Customizable Themes**: Create quizzes tailored to your favorite topics or educational needs.
- **Kahoot-Ready Output**: Automatically formats questions into a Kahoot-compatible Excel file for seamless import.
- **AI-Powered**: Leverages OpenAI's GPT model to ensure engaging and accurate question generation.
- **Multi-Language Support**: Generate quizzes in English or Traditional Chinese to reach a broader audience.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jerry871002/kahootgen.git
   cd kahootgen
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   - Create a `.env` file in the project root (if not already present).
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage

### Arguments

- `--themes` or `-t`: A list of themes for the quiz questions (e.g., `"Harry Potter" "Rocket Science"`).
- `--num-questions` or `-n`: The number of questions to generate for each theme (default: 5).
- `--language` or `-l`: The language for the quiz questions (default: en). Supported options are:
  - `en`: English
  - `zh-tw`: Traditional Chinese (Taiwan translation convention)
- `--output` or `-o`: The output file name for the generated quiz (default: `KahootQuizOutput.xlsx`).

### Example

To generate 10 questions each for "Harry Potter" and "Space Exploration" in English and save the output to `quiz.xlsx`:

```bash
# from the project root directory
python kahootgen/main.py --themes "Harry Potter" "Space Exploration" --num-questions 10 --language en --output quiz.xlsx
```

The generated quiz will be saved as `quiz.xlsx` in the project directory.

Then, you can import the generated Excel file to Kahoot to create your quiz. Have fun and enjoy!
