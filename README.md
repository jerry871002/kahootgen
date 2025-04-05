# KahootGen

KahootGen is a Python-based tool that uses OpenAI's GPT model to generate multiple-choice quiz questions based on user-defined themes. The generated questions are formatted into a Kahoot-compatible Excel file, making it easy to create engaging quizzes.

## Features

- Generate quiz questions for multiple themes.
- Customize the number of questions per theme.
- Automatically formats questions into a Kahoot-compatible Excel template.
- Supports OpenAI's GPT model for high-quality question generation.

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

Run the script using the following command:

```bash
python main.py --themes "Theme1" "Theme2" --num_questions 5
```

### Arguments

- `--themes` or `-t`: A list of themes for the quiz questions (e.g., `"Harry Potter" "Rocket Science"`).
- `--num_questions` or `-n`: The number of questions to generate for each theme (default: 5).

### Example

To generate 10 questions each for "Harry Potter" and "Space Exploration":

```bash
python main.py --themes "Harry Potter" "Space Exploration" --num_questions 10
```

The generated quiz will be saved as `KahootQuizOutput.xlsx` in the project directory.

Then, you can import the generated Excel file to Kahoot to create your quiz. Have fun and enjoy!
